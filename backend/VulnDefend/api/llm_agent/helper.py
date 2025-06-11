import operator
from typing import Dict, Any

from typing import TypedDict, Annotated, List, Union
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class IntentResponse(BaseModel):
    intent: str = Field(..., description="Must be 'search_db' or 'store_info'")


class SQLResponse(BaseModel):
    is_allow: bool = Field(..., description="Must be 'search_db' or 'store_info'")
    query: List[Dict[str, Any]] = Field(
        ..., description="SQL query response or empty if not allowed"
    )


class AgentState(TypedDict):
    chat_id: str
    query: str
    answer:str
    db_result:str
    sql_response: SQLResponse
    intent_classification: IntentResponse
    role: str
    collection_names: List[str]
    lnode:str
    summary: str
    error:bool
    error_message:str