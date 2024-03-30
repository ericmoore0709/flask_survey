from flask import Flask, render_template, request, redirect, session, flash
from surveys import satisfaction_survey
from uuid import uuid4

app = Flask(__name__)

# session key
app.secret_key = str(uuid4())


@app.get('/')
def index():
    session.pop('errors', default=None)
    session.pop('responses', default=None)
    return render_template('index.html', title='Index', survey=satisfaction_survey)


@app.post('/start')
def start():
    session['responses'] = []
    return redirect('/questions/0')


@app.get('/questions/<int:id>')
def question(id: int):

    responses = session.get('responses', default=[])

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')

    question = satisfaction_survey.questions[len(responses)]

    if id != len(responses):
        flash('Invalid data access detected.', 'danger')
        return redirect('/questions/' + str(len(responses)))

    return render_template('question.html', title='Question ' + str(id), question=question)


@app.post('/answer')
def answer():
    answer = request.form.get('answer', None)

    if not answer:
        session['errors'] = ["An answer is required."]
        return redirect('/questions/' + str(len(responses)))

    session.pop('errors', default=None)

    responses = session.get('responses', default=[])

    responses.append(answer.replace('_', ' '))
    session['responses'] = responses
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect('/questions/' + str(len(responses)))


@app.get('/thanks')
def thanks():
    session.pop('errors', default=None)
    return render_template('thanks.html')
