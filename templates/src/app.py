from flask import Flask, render_template, request
import Gptebnedding

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form['question']
        answer = Gptebnedding.AnswerQuestion(question)
        return render_template('answer.html', question=question, answer=answer)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)