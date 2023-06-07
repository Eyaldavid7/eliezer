import ImprovedGptembedding

while True:
    print("Press 1 to save an embedding or press 2 to ask a question.")
    user_input = input()
    if user_input == '1':
        print("Please provide a blob name (pdf file)")
        blob_name = input()
        ImprovedGptembedding.insert_embedding(blob_name)
    if user_input == '2':
        #Get the question from the user 
        print("Please provide a question")
        query = input()
        ImprovedGptembedding.answer_question(query)
    else: 
        print("Invalid input. Please try again.")