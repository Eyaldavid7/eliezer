from flask import Flask, request
from google.cloud import storage, bigquery
from google.auth import compute_engine
import openai
from google.cloud import secretmanager
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
import pandas as pd
import db_dtypes
import json
import ast
import google_blob_dbaccess
import TranslateBook
from PyPDF2 import PdfReader
import re
import io






app = Flask(__name__)

# Set the project ID and dataset ID
project_id = 'quickstart-1602611748801'
dataset_id = 'CheckCode'
BUCKET_NAME = 'bookembdding'
TABLE_NAME = 'BookEmbding'
 # Get the big quary client
bigquery_client = bigquery.Client(project='quickstart-1602611748801')

# Get the storage client
storage_client = storage.Client(project='quickstart-1602611748801')

COMPLETIONS_MODEL = "text-davinci-003"
QUESTION_COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 200,
    "model": COMPLETIONS_MODEL,
}

def get_api_key():

    # Authenticate to the Secret Manager API
    client = secretmanager.SecretManagerServiceClient()
    # Define the name of the API key
    name = "ChatGPTKey"

    # Retrieve the secret
    api_key = os.getenv("ChatGPTKey")

    return api_key
def InsertEmbdings2(text):
        
    # Loop through each text file and perform GPT embedding using ChatGPT API
    embeddings = []
    df=db.get()

    if text != '':
        text_embedding = get_embedding(text, engine='text-embedding-ada-002')
        df = df.append({"message":text, "ada_search": text_embedding},ignore_index=True)
        db.save(df)
        print('Row inserted successfully')

def InsertEmbdings():

    # Retrieve all the text files from the specified bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob_list = bucket.list_blobs()
    text_files = [blob for blob in blob_list if blob.name.endswith('.pdf')]

        
    # Loop through each text file and perform GPT embedding using ChatGPT API
    embeddings = []
    for text_file in text_files:
        text = text_file.download_as_text()
        text_embedding = get_embedding(text, engine='text-embedding-ada-002')
        if  text_embedding:
             df = df.append({"message":text, "ada_search": text_embedding},ignore_index=True)
    db.save(df)
    print('Row inserted successfully')
def AnswerQuestion(question):
    prompt = construct_prompt(question)
    response = openai.Completion.create(prompt=prompt, **QUESTION_COMPLETIONS_API_PARAMS)
    print(response["choices"][0]["text"])
    return response["choices"][0]["text"]

def construct_prompt(question, top_n=3):
    
    # Get the context
    question = question
    context = generate_context(question, top_n)
    header =  header = """Answer the question in details, based only on the provided context and nothing else, and if the answer is not contained within the text below, say "I don't know.", do not invent or deduce!\n\nContext:\n"""
    return header + "".join(context) + "Q: " + question + "\n A:"

def generate_context(question, top_n=3):
    
    most_similiar = return_most_similiar(question, top_n)
    # Get the top 3 most similar messages
    top_messages = most_similiar["message"].values
    # Concatenate the top 3 messages into a single string
    context = '\n '.join(top_messages)
    return context

def return_most_similiar(question, top_n=3):

    df=db.get()

     # Get the embedding for the question
    question_embedding = get_embedding(question, engine='text-embedding-ada-002')
    # Get the embedding for the messages in the database
    df["ada_search"] = df["ada_search"].apply(eval).apply(np.array)
    # Get the similarity between the question and the messages in the database
    df['similarity'] = df.ada_search.apply(lambda x: cosine_similarity(x, question_embedding))
    # Get the index of the top 3 most similar message
    most_similiar = df.sort_values('similarity', ascending=False).head(top_n)

    return most_similiar

def Embooks2():
    
    
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Define regex pattern to split text into sentences
    sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    
    # Get the blob containing the PDF file
    blob_name = 'vication.pdf'
    blob = bucket.blob(blob_name)

    # Download the PDF file to memory
    pdf_bytes = blob.download_as_bytes()

    # Open the pdf file
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_file = PdfReader(pdf_file)

    # Insert all the pages into one tex string
    text = ''
    for page in range(len(pdf_file.pages)):
        extracted_text  =    pdf_file.pages[page].extract_text()
        text += extracted_text

    # Split text into groups of 5 sentences
    sentences = sentence_pattern.split(text)
    group_size = 10
    groups = [sentences[i:i+group_size] for i in range(0, len(sentences), group_size)]

    # Saveing each pargrph after translation to the blob    
    for i, group in enumerate(groups):
        text = " ".join(group)
        text = text.replace('\n', ' ')
        translated_text = InsertEmbdings2(text)

def Embooks():
    
    
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Define regex pattern to split text into sentences
    sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    
    # Get the blob containing the PDF file
    blob_name = 'vication.pdf'
    blob = bucket.blob(blob_name)

    # Download the PDF file to memory
    pdf_bytes = blob.download_as_bytes()

    # Open the pdf file
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_file = PdfReader(pdf_file)

    # Insert all the pages into one tex string
    text = ''
    for page in range(len(pdf_file.pages)):
        extracted_text  =    pdf_file.pages[page].extract_text()
        text += extracted_text

    # Split text into groups of 5 sentences
    sentences = sentence_pattern.split(text)
    group_size = 10
    groups = [sentences[i:i+group_size] for i in range(0, len(sentences), group_size)]

    # Saveing each pargrph after translation to the blob    
    for i, group in enumerate(groups):
        text = " ".join(group)
        text = text.replace('\n', ' ')
        translated_text = InsertEmbdings2(text)

# Setup the open AI api key
openai.api_key = get_api_key()
db = google_blob_dbaccess.GoogleBucketDbAccess()
db.ensureExists()


