from pydantic import BaseModel, Field
from .helper import AgentState
from langgraph.graph import END, StateGraph, START
from django.core.serializers.json import DjangoJSONEncoder
from langgraph.checkpoint.memory import MemorySaver
import time
import json
from datetime import datetime

# from langgraph.checkpoint.sqlite import SqliteSaver
from asgiref.sync import sync_to_async

from .graph_nodes import (
    stream_node,
    classify_user_intent,
    query_database_function,
    respond_general_function,
    summary,
)

from api.utils.chat_utils import (
    create_chat_message,
)


def classify_user_intent_check(state):
    intent_obj = state.get("intent_classification")

    if not intent_obj:
        return "__end"

    print("intent:", intent_obj)

    # Route based on intent directly
    if intent_obj.get("intent") == "search_db":
        return "query_database"
    elif intent_obj.get("intent") == "store_info":
        return "respond_general"

    return "__end"


class Agent:
    def __init__(self, collection_name, model):
        self.collections = []  # Initialize collections as an empty list
        builder = StateGraph(AgentState)

        builder.add_node("classify_user_intent", classify_user_intent)
        builder.add_node("query_database", query_database_function)
        builder.add_node("respond_general", respond_general_function)
        builder.add_node("stream", stream_node)
        builder.add_node("summary_node", summary)

        builder.set_entry_point("classify_user_intent")

        # Outline branching (start or end)
        builder.add_conditional_edges(
            "classify_user_intent",
            classify_user_intent_check,
            {
                "__end": END,
                "query_database": "query_database",
                "respond_general": "respond_general",
            },
        )

        # formate_answer → verifier → stream
        builder.add_edge("query_database", "respond_general")
        builder.add_edge("respond_general", "stream")

        # summary_node also goes to stream (optional if both need merging)
        # (can skip if only verifier triggers stream)

        # stream decides: loop or end

        builder.add_edge("stream", "summary_node")
        builder.add_edge("summary_node", END)

        #
        memory = MemorySaver()

        self.graph = builder.compile(
            checkpointer=memory,
            # interrupt_after=[
            #     "classify_user_intent",
            #     "query_database",
            #     "index",
            #     "scrape_data",
            #     "transform_code_instruction",
            #     "supervisor",
            # ],
            # debug=True,
        )

        self.graph = builder.compile()
        self.model = model
        # self.collections.append(collection_name)

    async def report_stream(self, state: AgentState, chat_id: str):
        try:
            self.message = {
                "chat_id": chat_id,
                "response": "",
                "status": "pending",
                "source": [],
            }

            # state["collection_names"] = self.collections  # Replace as needed

            thread = {"configurable": {"thread_id": chat_id}, "recursion_limit": 250}

            def make_json_serializable(obj):
                if isinstance(obj, BaseModel):  # Pydantic model
                    return obj.model_dump()
                elif isinstance(obj, dict):
                    return {k: make_json_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [make_json_serializable(item) for item in obj]
                elif isinstance(obj, tuple):
                    return tuple(make_json_serializable(item) for item in obj)
                return obj

            async for event, chunk in self.graph.astream(
                state, thread, stream_mode=["updates"]
            ):
                # print(f">>>>>>>>>>>>>>>>{chunk}<<<<<<<<<<<<<<<<<<")
                serializable_chunk = make_json_serializable(chunk)
                s_serializable = DjangoJSONEncoder().encode(serializable_chunk)
                # Parse back into a JSON object to access fields
                json_s_serializable = json.loads(s_serializable)

                # Extract the first key and corresponding data from chunk (assuming there’s always one key)
                key, query_data = next(iter(json_s_serializable.items()))

                # Extract only the desired fields from query_data
                response_data = {
                    "query": query_data["query"],
                    "created_at": datetime.utcnow().isoformat()
                    + "Z",  # UTC timestamp in ISO format
                    "intent_classification": query_data["intent_classification"],
                    "sql_response": query_data["sql_response"],
                    "answer": query_data.get("answer", "No answer provided."),
                    "lnode": query_data.get("lnode", "Processing."),
                }
                print("response_data:", response_data)

                self.message["response"] = response_data
                self.message["status"] = "processing"
                yield f"{ json.dumps(self.message)}\n"

            self.message["status"] = "done"
            yield f"{ json.dumps(self.message)}\n"
        except KeyError as e:
            print(f"Caught exception: {e}")
            self.message["status"] = "done"
            yield f'{{"message": {json.dumps(self.message)}}}\n'
        finally:
            timestamp = datetime.fromtimestamp(time.time()).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            async_create_chat_message = sync_to_async(create_chat_message)

            try:
                response = self.message.get("response", {})
                await async_create_chat_message(
                    chat_id=chat_id,
                    question=response.get("query", ""),
                    answer=response.get("answer", ""),
                    intent_classification=response.get("intent_classification", {}),
                    sql_response=response.get("sql_response", {}),
                )
            except Exception as e:
                print("[create_chat_message error]", e)

            print(f"Done at {timestamp}")


# from typing import List
# from langchain.schema import BaseMessage
# from your_module import QueryResponse, IntentResponse  # Adjust import paths

# empty_agent_state: AgentState = {
#     "query": "",
#     "response": QueryResponse(is_allow="store_info", query=[]),
#     "intent_classification": IntentResponse(intent="store_info", reason=""),
#     "chat_history": [],
#     "role": "customer",  # or "admin", "employee"
#     "collection_names": [],
#     "summary": ""
# }
