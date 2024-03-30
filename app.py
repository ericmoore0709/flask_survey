from flask import Flask, render_template, request, redirect, session
from surveys import satisfaction_survey
from uuid import uuid4

app = Flask(__name__)

# session key
app.secret_key = str(uuid4())

# initialize response list
responses = []


@app.get('/')
def index():
    responses.clear()
    return render_template('index.html', title='Index', survey=satisfaction_survey)


@app.get('/questions/<int:id>')
def question(id: int):
    question = satisfaction_survey.questions[len(responses)]

    if id != len(responses):
        return redirect('/questions/' + str(len(responses)))

    return render_template('question.html', title='Question ' + str(id), question=question)


@app.post('/answer')
def answer():
    answer = request.form.get('answer')

    if not answer:
        session['errors'] = ["An answer is required."]
        return redirect('/questions/' + str(len(responses)))

    session.pop('errors', default=None)
    responses.append(answer)
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect('/questions/' + str(len(responses)))


@app.get('/thanks')
def thanks():
    return render_template('thanks.html')
