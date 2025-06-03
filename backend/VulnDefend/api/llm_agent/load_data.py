from llm_manager import load_chroma_gpt


# memory = SqliteSaver.from_conn_string(":memory:")
# Loading Data
load_chroma_gpt(filename="./pdf/store_info.pdf",collection_name="store_info")


