import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.chains import RetrievalQA
from openai.embeddings_utils import get_embedding
import google_blob_dbaccess
from google.cloud import storage
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
import io
import openai
import aspose.words as aw


def load_environment_variables():
    dotenv.load_dotenv()


def split_documents_into_chunks(documents, chunk_size=800, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)


def prepare_model_embedding(texts):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    doc_search = Chroma.from_documents(texts, embeddings)
    return RetrievalQA.from_chain_type(llm=OpenAI(), retriever=doc_search.as_retriever())


def answer_question(query):
    #update local db
    db.get()
    loader = PyPDFLoader("local_db.pdf")
    pages = loader.load_and_split()
    texts = split_documents_into_chunks(pages)
    chain = prepare_model_embedding(texts)
    return chain.run(query)

def concatenate_pdfs(files):
    output = aw.Document()
    # Remove all content from the destination document before appending.
    output.remove_all_children()
    for file in files:
        input = aw.Document(file)
        # Append the source document to the end of the destination document.
        output.append_document(input, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)
    output.save("local_db.pdf")


def insert_embedding(blob_name):
    #update local db
    db.get()
    #create new information file
    db.read_blob(blob_name, "current_file.pdf")
    #concatenate pdfs
    files = [ "local_db.pdf", "current_file.pdf" ]
    concatenate_pdfs(files)
    db.save()
    print('Data inserted successfully')

load_environment_variables()
db = google_blob_dbaccess.GoogleBucketDbAccess()
db.ensureExists()