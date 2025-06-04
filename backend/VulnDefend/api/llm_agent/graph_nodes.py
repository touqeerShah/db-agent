from .helper import AgentState, IntentResponse, SQLResponse
from typing import List
import json
from langchain_core.messages import HumanMessage, AIMessage
import time
from pydantic import BaseModel, Field

from .llm_manager import get_llm_object
import json
import re
from typing import Optional, Dict, Any
from .db import execute_query, get_role_permissions
from .analyze_sql_query import analyze_sql_query
from api.utils.chat_utils import (
    get_last_chat_message,
    update_chat_summary,
    get_chat_summary,
)


def extract_valid_json(raw_response: str) -> Optional[Dict[str, Any]]:
    import re

    # Step 1: Try direct parse
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        pass

    # Step 2: Try to extract JSON block
    json_match = re.search(r"{[\s\S]+?}", raw_response)
    if json_match:
        json_string = json_match.group(0)

        # ✅ Clean up common model formatting issues
        # Remove trailing commas
        json_string = re.sub(r",(\s*})", r"\1", json_string)
        json_string = re.sub(r",(\s*])", r"\1", json_string)

        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print("❌ JSON decode failed after cleaning:", e)
            print("Cleaned string:", json_string)
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
    table_schema = """CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT
);

-- Table: customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT
);

-- Table: products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    vendor_id INTEGER REFERENCES vendors(id),
    purchase_price DECIMAL(10, 2),
    selling_price DECIMAL(10, 2),
    stock_quantity INTEGER DEFAULT 0,
    warranty_period_months INTEGER DEFAULT 0  -- Warranty duration
);

-- Table: bills (represents customer bills/invoices)
CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    bill_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(12, 2),
    payment_status VARCHAR(50) DEFAULT 'Pending'  -- Paid, Pending, Overdue, etc.
);

-- Table: sales (sales made to customers)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bills(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_sale DECIMAL(10, 2),
    sale_date DATE DEFAULT CURRENT_DATE
);

-- Table: product_warranty_status (tracks warranty per product sold)
CREATE TABLE product_warranty_status (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id) ON DELETE CASCADE,
    warranty_start_date DATE NOT NULL,
    warranty_end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Active'  -- Active, Expired, Claimed
);

-- Table: vendor_purchases (records purchases from vendors)
CREATE TABLE vendor_purchases (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id),
    product_id INTEGER REFERENCES products(id),
    purchase_date DATE NOT NULL DEFAULT CURRENT_DATE,
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * purchase_price) STORED,
    payment_status VARCHAR(50) DEFAULT 'Unpaid'  -- Unpaid, Partial, Paid
);

-- Table: vendor_payments (records payments made to vendors)
CREATE TABLE vendor_payments (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id),
    purchase_id INTEGER REFERENCES vendor_purchases(id) ON DELETE SET NULL,
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount_paid DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50),  -- e.g., Bank Transfer, Cash, Cheque
    note TEXT
);


CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,                      -- e.g., 'admin', 'employee', 'customer'
    table_name VARCHAR(100) NOT NULL,               -- e.g., 'vendors', 'customers', 'inventory'
    can_select BOOLEAN DEFAULT FALSE,
    can_insert BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE
);
"""  # use your existing schema block

    # Ask LLM to generate the SQL query
    message = f"""
        You are a SQL expert. Based on the following table schema and the user request, generate ONLY the SQL query.

        Schema:
        {table_schema}

        User question:
        "{query_text}"
        - Rule not ```sql 
        - or no need to wrap with anything
        Only output a valid PostgreSQL SQL query. Do not explain or wrap in JSON.
        """

    try:
        response = llm.invoke([HumanMessage(content=message)])
        raw_sql = response
        print("\nRaw SQL:", raw_sql)
        print("\n Raw role_perms:", role_perms, "\n")

        # Step 1: Extract all table names from SQL (basic method)
        table_names = role_perms
        operation, table_names = analyze_sql_query(raw_sql)
        print(f"🔍 Operation: {operation}, Tables: {table_names}")

        # not_allowed = []
        # for table in table_names:
        #     match = next((r for r in role_perms if r["table_name"] == table), None)
        #     if not match:
        #         not_allowed.append(table)
        #         continue

        #     allowed = {
        #         "select": match.get("can_select", False),
        #         "insert": match.get("can_insert", False),
        #         "update": match.get("can_update", False),
        #         "delete": match.get("can_delete", False),
        #     }.get(operation, False)

        #     if not allowed:
        #         not_allowed.append(table)

        # if not_allowed:
        #     print(
        #         f"🚫 Access denied for operation '{operation}' on tables: {not_allowed}"
        #     )
        #     state["response"] = SQLResponse(is_allow=False, query=[])
        #     return state
        # Step 2: Verify all tables in query are allowed for SELECT by role

        # Step 3: If allowed, execute query
        results = execute_query(raw_sql)
        print("results : ",results,"\n\n")
        state["db_result"] = results
        print("\nstate : ",state)
        return state
    except Exception as e:
        print("Query generation or execution failed:", e)
        state["db_result"] = None

    return state


def respond_general_function(state: AgentState) -> AgentState:
    # Flatten query into a single string
    query_text = state["query"]
    intent_classification = state["intent_classification"]
    intent = intent_classification["intent"]
    qa_advanced, llm = get_llm_object(state["collection_names"])
    summary_history = get_chat_summary(state["chat_id"])
    print("\n\n\nintent : = == = = = == == >>>>> ", summary_history)

    # Shared Markdown rules message prefix
    markdown_rules = """
        You are Alise, a helpful assistant for a store. Answer questions in a friendly, helpful tone. Be concise and avoid unnecessary explanations.
     
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
            state["answer"] = raw_result
        except Exception as e:
            print("Error while generating outline:", e)
            raw_result = "⚠️ Error generating response."

        # Save chat history

    elif intent == "search_db":
        response_data = state.get("db_result", None)
        if not response_data:
            markdown_response = "⚠️ No data found or access denied."
            state["answer"] = markdown_response
        else:
            message = f"""{markdown_rules}
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
            ### User Query:
            {query_text}

            ### Raw Data to Format:
            {response_data}
            ### User History / Context:
            {summary_history}
            """
            try:
                response = llm.invoke([HumanMessage(content=message)])
                markdown_response = response
                state["answer"] = markdown_response
            except Exception as e:
                print("Error formatting DB result:", e)
                markdown_response = "⚠️ Failed to format result."
                state["error"] = True
                state["error_message"] = "Server Error Try again"
    print("state : = == = = = == == >>>>> ", state)
    return state


def classify_user_intent(state: AgentState) -> AgentState:
    print("state : ", state)
    query = state["query"]
    qa_advanced, llm = get_llm_object(state["collection_names"])
    if not qa_advanced or not llm:
        return state

    class IntentResponse(BaseModel):
        intent: str = Field(..., description="Must be 'search_db' or 'store_info'")

    schema = json.dumps(IntentResponse.model_json_schema())

    message = f"""
You are a classification assistant. Your task is to identify the **intent** of the user's query.

### Intents:
- "search_db": When the query is about structured data such as tables or records (e.g., product_warranty_status, vendor_purchases, vendor_payments, sales, bills, products, customers, vendors).
- "store_info": When the query is about store-related operations, usage, policies, or is a general natural-language question.

### Instructions:
- Carefully read the user query.
- Choose **only one** intent from the list above.
- Return a **strictly valid JSON** object, with no trailing commas, no code fences, and no extra text.

### User Query:
"{query}"

### Required Format:
Return **exactly**:
{{
  "intent": "search_db"
}}

OR

{{
  "intent": "store_info"
}}

Nothing else. Do NOT include markdown, commentary, or schema again.
"""

    print("message:", message)
    try:
        response = llm.invoke([HumanMessage(content=message)])
        raw_result = response
        print("Raw classification response:", raw_result)

        parsed = extract_valid_json(raw_result)
        if parsed:
            validated = IntentResponse.model_validate(parsed)
            state["intent_classification"] = validated.model_dump()
        else:
            print("Failed to parse classification response.")
            state["intent_classification"] = IntentResponse(
                intent="search_db"
            ).model_dump()

    except Exception as e:
        print("Intent classification error:", e)
        state["intent_classification"] = IntentResponse(
            intent="search_db"
        ).model_dump()

    print("= = = = = >", state["intent_classification"])
    return state


def stream_node(state: AgentState):
    print("stream_node")
    return state


def summary(state: AgentState):
    print("summary_node")
    try:
        qa_advanced, llm = get_llm_object(state["collection_names"])

        if not qa_advanced or not llm:
            return state
        chain = qa_advanced
        chat_history = get_last_chat_message(state.get("chat_id", ""))
        summary_history = state.get("summary", "")
        print(summary_history)
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
                state["summary"] = response

                update_chat_summary(state["chat_id"], state["summary"])
                return state
            except Exception as e:
                print(f"Error during chain.invoke (attempt {attempt + 1}):", repr(e))
                import traceback

                traceback.print_exc()
                print("Error during get_llm_object:", repr(e))
            time.sleep(3)

        # If both attempts fail
        return state
    except Exception as e:
        print("[Error in summary generation]", str(e))
        # state["summary"] = "An error occurred while generating the summary."
        return state["summary"]
