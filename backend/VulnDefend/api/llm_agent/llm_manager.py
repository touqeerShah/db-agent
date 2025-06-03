import re
import json

# import asyncio
import websockets
from langchain.chains import RetrievalQA
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

## for run local
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.schema import Document

### Multiple Query
from typing import List
import time
from pydantic import BaseModel, Field
from langchain_community.document_transformers.embeddings_redundant_filter import (
    EmbeddingsRedundantFilter,
)
from langchain_chroma import Chroma
from pypdf import PdfReader



from langchain.retrievers import (
    MergerRetriever,
)

# from app.src.llm.utils.ppt_title import get_title


import os

# import nest_asyncio

# # Apply nest_asyncio
# nest_asyncio.apply()
from dotenv import load_dotenv


load_dotenv()

# Your JWT secret key
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "")
AWS_MODEL_ID = os.getenv("AWS_MODEL_ID", "")
AWS_SECRET_TOKEN = os.getenv("AWS_SECRET_TOKEN", "")
WEB_SOCKET_URL = os.getenv("WEB_SOCKET_URL", "ws://localhost:4000/ws/llm_message")


AWS_DEFAULT_REGION = "eu-central-1"
AWS_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
###
current_file_dir = os.path.dirname(os.path.abspath(__file__))
# AWS
# DB_PATH="/root/ao-llm-celery/app/data/processed"
# local
DB_PATH = "./vectorstores/db"
PPT_PATH = os.path.abspath(os.path.join("/root", "/data/ppt"))


async def send_websocket_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)


def get_bed_rock_object():

    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name="eu-central-1",
        aws_access_key_id="",  # those are not need on Deployment time
        aws_secret_access_key="",
        aws_session_token="",
    )
    return bedrock_client


def get_bed_rock_embedding():
    bedrock_client = get_bed_rock_object()
    embeddings = BedrockEmbeddings(
        client=bedrock_client, model_id="amazon.titan-embed-text-v2:0"
    )
    return embeddings


def get_local_embedding():
    # embeddings = GPT4AllEmbeddings()
    model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
    gpt4all_kwargs = {"allow_download": False}
    embeddings = GPT4AllEmbeddings(model_name=model_name, gpt4all_kwargs=gpt4all_kwargs)
    # embeddings = GPT4AllEmbeddings()

    return embeddings


class Document:
    def __init__(self, text, source):
        self.page_content = text
        self.metadata = {"source": source}


# Output parser will split the LLM result into a list of queries
class LineList(BaseModel):
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")


def get_llm_object(collections_name, model="llama-pro:8b-instruct-q5_K_M"):
    #  uncommenr when deployed on AWS
    # bedrock_client = get_bed_rock_object()
    # llm = ChatBedrock(
    #     region_name=AWS_DEFAULT_REGION,
    #     client=bedrock_client,
    #     model_id=AWS_MODEL_ID,
    #     streaming=True,
    #     # callbacks=[StreamingStdOutCallbackHandler()],
    # )

    # for test local with lama and  model
    llm = Ollama(
        model=model,
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    print("Load with LLM with Document ")
    qa_advanced = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_multiple_retriever(collections_name),
        return_source_documents=True,
    )

    return qa_advanced, llm


def get_vector_store(collections_name):
    # get/create a chroma client
    #  for AWS deployment
    embeddings = get_bed_rock_embedding()
    #  to run local
    # embeddings = get_local_embedding()
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_PATH,
        collection_name=collections_name,
    )

    return vectorstore



def _read_pdf(filename):
    reader = PdfReader(filename)

    pdf_texts = [p.extract_text().strip() for p in reader.pages]

    # Filter the empty strings
    pdf_texts = [text for text in pdf_texts if text]
    return pdf_texts


def load_chroma_gpt(filename, collection_name):
    texts = _read_pdf(filename)
    print("texts", (texts[0]))
    # chunks = _chunk_texts(texts)
    # AWS
    # embeddings = get_bed_rock_embedding()
    embeddings = get_local_embedding()

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_PATH,
        collection_name=collection_name,
    )
    all_split_docs = []  # To collect all split documents for the BM25Retriever
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1250,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    #
    for text in texts:
        # Create an instance of Document with the text
        doc_obj = Document(text, collection_name)
        # Now pass a list of these Document instances

        split_docs = text_splitter.split_documents([doc_obj])
        # print(split_docs)
        vectorstore.add_documents(split_docs)
        all_split_docs.extend(split_docs)



    return vectorstore


def get_multiple_retriever(collections_name):
    retrievers = []
    # embeddings = get_local_embedding()
    for collection_name in collections_name:
        vectorstore = get_vector_store(collection_name)
        retrievers.append(
            vectorstore.as_retriever(search_kwargs={"k": 10}, search_type="mmr")
        )

    ensemble_retriever = MergerRetriever(retrievers=retrievers, weight=[0.5, 0.5])
    return ensemble_retriever


def extract_json(text):
    pattern = r"\{(?:[^{}]|(?:\{.*?\}))*\}"
    text = text.replace("\n", " ")
    match = re.search(pattern, text)
    if match:
        json_text = match.group(0)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No valid JSON object found in the text.")
    return None


def sanitize_name(name):
    return re.sub(r"\W+", "_", name).strip("_")
