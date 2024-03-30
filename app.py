from flask import Flask, render_template, request, redirect
from surveys import satisfaction_survey

app = Flask(__name__)

# initialize response list
responses = []


@app.get('/')
def index():
    responses.clear()
    return render_template('index.html', title='Index', survey=satisfaction_survey)


@app.get('/questions/<int:id>')
def question(id: int):
    question = satisfaction_survey.questions[id]
    return render_template('question.html', title='Question ' + str(id), question=question)


@app.post('/answer')
def answer():
    answer = request.form['answer']
    responses.append(answer)
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect('/questions/' + str(len(responses)))


@app.get('/thanks')
def thanks():
    return render_template('thanks.html')
