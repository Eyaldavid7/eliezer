# Project Name: Eliezer

## Project Description

Eliezer is a text embedding and question-answering application built using Flask and OpenAI's Gptebnedding model. The project aims to provide a user-friendly interface for embedding new texts and answering questions based on the pre-embedded text database.

The core features of the project include:

1. **Text Embedding:** Users can input new texts into the application, and the system will perform text embedding using the Gptebnedding model. The embedded texts are stored in a Google Cloud Storage bucket for efficient retrieval and processing.

2. **Question Answering:** Users can ask questions based on the pre-embedded texts, and the system will provide answers by leveraging the embedded text database. The application uses OpenAI's Completion API to generate detailed and accurate responses.

The project consists of the following files:
## File Descriptions

- **app.py**: This file contains the main Flask application code. It imports the necessary modules, including Flask and Gptebnedding, and creates a Flask web application instance. It defines a route for the home page ("/") that handles both GET and POST requests. For GET requests, it renders the home.html template, which is responsible for displaying the form to submit a question. For POST requests, it retrieves the question from the submitted form data, passes it to the Gptebnedding.AnswerQuestion() function from the Gptebnedding module to get the answer, and renders the answer.html template, which displays the original question and the corresponding answer.

- **google_bucket_dbaccess.py**: This file defines a class `GoogleBucketDbAccess` that provides methods to interact with a Google Cloud Storage bucket. The bucket holds the embeddings of the different texts.

- **app.py**: This file encompasses the functionality for text embedding and answering questions based on the pre-embedded text. The main features of app.py include:

  - Text Embedding: The `InsertEmbdings(text)` function performs text embedding by saving the provided text into the embedding database. It retrieves the existing database using the `db.get()` method, generates embeddings for the text using the ChatGPT API, appends the text and its corresponding embedding to the database, and updates the database using `db.save()`.

  - Question Answering: The `AnswerQuestion(question)` function handles answering questions based on the pre-embedded text. It constructs a prompt for the OpenAI Completion API by combining the question with relevant context from the embedding database and retrieves an answer by calling the API. The answer is then returned for further processing.

- **test.py**: This file serves as a convenient tool for testing the functionality of the application without the need to run a web server. The main purpose of test.py is to provide an easy way to test the functions and methods implemented in the application. It allows you to directly invoke and verify the behavior of specific functions without the overhead of setting up a web server.

This README provides an overview of the project's files and their respective functionalities, enabling users to understand the purpose and usage of each file.
