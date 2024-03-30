from flask import Flask, render_template, request
from surveys import satisfaction_survey

app = Flask(__name__)

# initialize response list
responses = list[str]


@app.get('/')
def index():
    return render_template('index.html', title='Index', survey=satisfaction_survey)


@app.get('/questions/<int:id>')
def question(id: int):
    question = satisfaction_survey.questions[id]
    return render_template('question.html', title='Question ' + str(id), question=question)


@app.post('/answer')
def answer():
    answer = request.form
