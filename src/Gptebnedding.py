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
from PyPDF2 import PdfReader
import re
import io
import dotenv



app = Flask(__name__)

# Set the project ID and dataset ID
project_id = 'quickstart-1602611748801'
dataset_id = 'CheckCode'
BUCKET_NAME = 'tals-openai-bucket'
 # Get the big quary client
bigquery_client = bigquery.Client(project='quickstart-1602611748801')

# Get the storage client
storage_client = storage.Client(project='quickstart-1602611748801')

COMPLETIONS_MODEL = "gpt-3.5-turbo-16k"
QUESTION_COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 200,
    "model": COMPLETIONS_MODEL,
}

# Retrive the open AI api key
def get_api_key():

    # Authenticate to the Secret Manager API
    client = secretmanager.SecretManagerServiceClient()
    # Define the name of the API key
    name = "ChatGPTKey"

    # Retrieve the secret
    api_key = os.getenv("ChatGPTKey")

    return api_key

# Gets a text and insert its embdings to local file and cloud blob
def InsertEmbdings(text):
        
    # Loop through each text file and perform GPT embedding using ChatGPT API
    embeddings = []
    df=db.get()

    if text != '':
        text_embedding = get_embedding(text, engine='text-embedding-ada-002')
        df = df._append({"message":text, "ada_search": text_embedding},ignore_index=True)
        db.save(df)
        print('Row inserted successfully')

# gets a question and provide the answer to the question
def AnswerQuestion(question):
    #db.get()
    with open('360401.pdf', 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    print(text)
    chunk_length = 15000
    chunks = [text[i:i+chunk_length] for i in range(0, len(text), chunk_length)]
    answer = ""
    for chunk in chunks:
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Please determine whether an answer was found. The output should only contain the short answer yes or no."},
            {"role": "user", "content": f"הנה פקודה: {chunk}"},
            {"role": "user", "content": f"האם התשובה לשאלה {question} נמצאת בפקודה?"},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000
        )

        res = response['choices'][0]['message']['content']

        if res == "כן" or res == "yes":
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"הנה פקודה: {chunk}"},
                {"role": "user", "content": f"{question} לפי הפקודה?"},
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                max_tokens=1000
            )
            res = response['choices'][0]['message']['content']
            if len(res) > len(answer):
                answer = res
    
    if answer == "":
        answer = "לא מצאתי תשובה מתאימה לשאלה שלך"
    print(answer)

    """
    print(response["choices"][0]["text"])
    return response["choices"][0]["text"]"""

# Constructing  the prompt for the question based on the question and three most similler massages
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

# Retrieve the question and return the most similar message from the stored message database
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


# Process a file that has been saved in the bucket by embedding each group of five sentences together. 
# The function combines the five sentences into a single text and performs embedding using a pre-trained model. 
# The resulting vector is then saved to both the local file and the cloud file for further use.
def Embooks():
    
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'tals-openai-bucket'
    bucket = storage_client.bucket(bucket_name)

    # Define regex pattern to split text into sentences
    sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    
    # Get the blob containing the PDF file
    blob_name = '360406.pdf'
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
        translated_text = InsertEmbdings(text)

# Setup the open AI api key
dotenv.load_dotenv()
openai.api_key = get_api_key()

# Loading the embedding DB
db = google_blob_dbaccess.GoogleBucketDbAccess()
db.ensureExists()


