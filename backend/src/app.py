from flask import Flask
from flask import request
from flask_cors import CORS
import ImprovedGptembedding

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['POST'])
def get_answer():
    query = request.data.decode("utf-8")[1:-1] 
    print(query)
    answer = ImprovedGptembedding.answer_question(query)
    return answer

if __name__ == '__main__':
    app.run()