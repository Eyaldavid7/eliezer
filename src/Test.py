import Gptebnedding
while True:
    print("Press 1 to save an embedding or press 2 to ask a question.")
    user_input = input()
    if user_input == '1':
        Gptebnedding.Embooks()
    if user_input == '2':
        #Get the question from the user 
        print("Please provide a question")
        user_input = input()
        answer =  Gptebnedding.AnswerQuestion(user_input)
        print(answer)
    else: 
        print("Invalid input. Please try again.")