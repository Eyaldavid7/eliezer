from flask import Flask
from flask import request
from flask_cors import CORS
import ImprovedGptembedding
<<<<<<< HEAD
import Gptebnedding
=======
>>>>>>> d2543108c91ff17679fc63203b87ca598e16bf98

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['POST'])
def get_answer():
    query = request.data.decode("utf-8")[1:-1] 
    answer = ImprovedGptembedding.answer_question(query)
<<<<<<< HEAD
    #answer = Gptebnedding.AnswerQuestion(query)
=======
>>>>>>> d2543108c91ff17679fc63203b87ca598e16bf98
    return answer

if __name__ == '__main__':
    app.run()