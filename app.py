from flask import Flask, render_template
from surveys import satisfaction_survey

app = Flask(__name__)

# initialize response list
responses = list[str]

@app.get('/')
def index():
    return render_template('index.html', title='Index', survey=satisfaction_survey)