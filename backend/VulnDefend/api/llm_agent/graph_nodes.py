from .helper import AgentState,  IntentResponse, SQLResponse
from typing import List
import json
from langchain_core.messages import HumanMessage, AIMessage
import time

from .llm_manager import get_llm_object
import json
import re
from typing import Optional, Dict, Any
from .db import execute_query, get_role_permissions
from .analyze_sql_query import analyze_sql_query
from api.utils.chat_utils import (
    update_chat_intent,
    update_chat_sql_response,
    update_chat_answer,
    get_last_chat_message,
)


def extract_valid_json(raw_response: str) -> Optional[Dict[str, Any]]:
    """
    Attempts to extract and parse a valid JSON object from a raw string.

    Args:
        raw_response (str): The full response string from the model.

    Returns:
        Optional[Dict[str, Any]]: Parsed JSON object if successful, otherwise None.
    """
    # Step 1: Try direct parse
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        pass

    # Step 2: Try to extract the first JSON object using regex
    json_match = re.search(r"{[\s\S]+}", raw_response)
    if json_match:
        json_string = json_match.group(0)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print("❌ JSON decode failed after regex:", e)
            return None

    print("❌ No valid JSON found in response.")
    return None






def query_database_function(state: AgentState) -> AgentState:

    query_text = state["query"]
    role = state["role"]
    qa_advanced, llm = get_llm_object(state["collection_names"])
    role_perms = get_role_permissions(role)

    if not qa_advanced or not llm:
        raise ValueError("Missing LLM or QA object")

    # Provide table schema to help LLM
    table_schema = """..."""  # use your existing schema block

    # Ask LLM to generate the SQL query
    message = f"""
        You are a SQL expert. Based on the following table schema and the user request, generate ONLY the SQL query.

        Schema:
        {table_schema}

        User question:
        "{query_text}"

        Only output a valid PostgreSQL SQL query. Do not explain or wrap in JSON.
        """

    try:
        response = llm.invoke([HumanMessage(content=message)])
        raw_sql = response.content.strip()
        print("🧠 Raw SQL:", raw_sql)

        # Step 1: Extract all table names from SQL (basic method)
        table_names = get_role_permissions(role)
        operation, table_names = analyze_sql_query(raw_sql)
        print(f"🔍 Operation: {operation}, Tables: {table_names}")

        not_allowed = []
        for table in table_names:
            match = next((r for r in role_perms if r["table_name"] == table), None)
            if not match:
                not_allowed.append(table)
                continue

            allowed = {
                "select": match.get("can_select", False),
                "insert": match.get("can_insert", False),
                "update": match.get("can_update", False),
                "delete": match.get("can_delete", False),
            }.get(operation, False)

            if not allowed:
                not_allowed.append(table)

        if not_allowed:
            print(
                f"🚫 Access denied for operation '{operation}' on tables: {not_allowed}"
            )
            state["response"] = SQLResponse(is_allow=False, query=[])
            return state
        # Step 2: Verify all tables in query are allowed for SELECT by role

        # Step 3: If allowed, execute query
        results = execute_query(raw_sql)
        state["response"] = SQLResponse(is_allow=True, query=results)
        update_chat_sql_response(state["chat_id"], state["response"])
    except Exception as e:
        print("Query generation or execution failed:", e)
        state["response"] = SQLResponse(is_allow=True, query=[])

    return state


def respond_general_function(state: AgentState) -> AgentState:
    # Flatten query into a single string
    query_text = state["query"]
    intent = state["intent_classification"].intent
    qa_advanced, llm = get_llm_object(state["collection_names"])
    summary_history = state.get("summary", "")

    # Shared Markdown rules message prefix
    markdown_rules = """
        You are a professional **Markdown report writer**.

        Your task:
        - Return only valid Markdown content.
        - Do NOT include code fences, explanations, or extra commentary.
        - Format data cleanly using:
        - `#`, `##`, `###` for headings
        - Bullet points, numbered lists
        - Tables (with | and ---)
        - Paragraphs and blockquotes (optional)

        Respond strictly in Markdown format.
        """

    if intent == "store_info":
        message = f"""{markdown_rules}

        ### User Query:
            {query_text}
        ### User History / Context:
            {summary_history}
        """
        try:
            response = qa_advanced.invoke(message)
            raw_result = response["result"]
        except Exception as e:
            print("Error while generating outline:", e)
            raw_result = "⚠️ Error generating response."

        # Save chat history
        state["chat_history"].append(HumanMessage(content=[query_text]))
        state["chat_history"].append(AIMessage(content=raw_result))

    elif intent == "search_db":
        response_data = state.get("response", [])
        if not response_data:
            markdown_response = "⚠️ No data found or access denied."
        else:
            message = f"""{markdown_rules}

            ### User Query:
            {query_text}

            ### Raw Data to Format:
            {response_data}
            ### User History / Context:
            {summary_history}
            """
            try:
                response = llm.invoke([HumanMessage(content=message)])
                markdown_response = response.content
                state["answer"] = markdown_response
                update_chat_answer(state["chat_id"], state["answer"])
            except Exception as e:
                print("Error formatting DB result:", e)
                markdown_response = "⚠️ Failed to format result."
                state["error"] = True
                state["error_message"] = "Server Error Try again"

    return state


def classify_user_intent(state: AgentState) -> AgentState:
    query = state["query"]
    qa_advanced, llm = get_llm_object(state["collection_names"])
    if not qa_advanced or not llm:
        return state

    schema = json.dumps(IntentResponse.model_json_schema())

    message = f"""
            You are an assistant tasked with determining the intent of a user's query.

            Categories:
            - "search_db": if the user is trying to retrieve structured data from a database.
            - "store_info": if the user is asking about store processes, policies, or general info.

            Instructions:
            1. Carefully read the user's query.
            2. Choose only one intent from the list above.
            3. Provide a short reason for your choice.

            User Query:
            "{query}"

            Return a JSON object like this:
            {{
            "intent": "search_db",
            "reason": "Because the user is asking for customer data."
            }}

            Strictly return only the JSON object.
            {schema}
            """

    try:
        response = llm.invoke([HumanMessage(content=message)])
        raw_result = response.content
        print("Raw classification response:", raw_result)

        parsed = extract_valid_json(raw_result)
        if parsed:
            validated = IntentResponse.model_validate(parsed)
            state["intent_classification"] = validated

        else:
            print("Failed to parse classification response.")
            state["intent_classification"] = IntentResponse(
                intent="store_info", reason="fallback due to invalid JSON"
            )

    except Exception as e:
        print("Intent classification error:", e)
        state["intent_classification"] = IntentResponse(
            intent="store_info", reason="exception fallback"
        )
    update_chat_intent(state["chat_id"], state["intent_classification"])
    return state


def stream_node(state: AgentState):
    print("stream_node")
    return state


async def summary(state: AgentState):
    print("summary_node")
    try:
        qa_advanced, llm = get_llm_object(state["collection_names"])

        if not qa_advanced or not llm:
            return state
        chain = qa_advanced
        chat_history = get_last_chat_message(state.get("chat_id", ""))
        summary_history = state.get("summary", "")
        if chat_history:
            question = chat_history.get("question", "")
            answer = chat_history.get("answer", "")
            last_message_combined = f"**Q:** {question}\n\n**A:** {answer}"
        else:
            last_message_combined = "No previous chat message found."

        if not last_message_combined:
            state["summary"] = "No message found to summarize."
            return {"result": state["summary"]}

        message = f"""
            You are a report assistant. Summarize the following message into a **professional, clear, and concise report-style summary**.

            ### Instructions:
            - Extract the key points from the message.
            - Rephrase them clearly and formally.
            - Ensure the summary is well-structured and easy to understand.
            - Avoid adding new information or personal commentary.
            
            ### User History / Context:
            {summary_history}

            ### Message to Summarize:
            {last_message_combined}

            ### Final Output:
            Provide a single paragraph or short section that captures the essence of the message.
        """
        for attempt in range(2):
            try:
                response = llm.invoke([HumanMessage(content=message)])
                return response.content
            except Exception as e:
                print(f"Error during chain.invoke (attempt {attempt + 1}):", repr(e))
                import traceback

                traceback.print_exc()
                print("Error during get_llm_object:", repr(e))
            time.sleep(3)

        # If both attempts fail
        return state["summary"]
    except Exception as e:
        print("[Error in summary generation]", str(e))
        # state["summary"] = "An error occurred while generating the summary."
        return state["summary"]
