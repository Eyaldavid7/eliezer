from flask import Flask
from flask_cors import CORS
import ImprovedGptembedding

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def get_answer():
    #answer = ImprovedGptembedding.AnswerQuestion(question)
    return "wow"

if __name__ == '__main__':
    app.run()