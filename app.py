
from crypt import methods
import pdb
from tarfile import LENGTH_LINK
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

import surveys

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'abcdef'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

#as user ansewers questions answers will be stored here
responses = []
results = {}

@app.route('/')
def surveyHome():
  return render_template(
    'satisfaction.html', 
    survey = surveys.satisfaction_survey)

@app.route('/thanks')
def completedSurvey():
  return render_template('thanks.html', results = results, title = surveys.satisfaction_survey.title, len=surveys.satisfaction_survey.getLen())

@app.route('/questions/<id>')
def getQuestion(id):
  id = int(id) + 1
  formData = request.form.get(f'{id}', 0);
  responses.append(formData)

  if int(id) >= surveys.satisfaction_survey.getLen():
    results = dict(zip(surveys.satisfaction_survey.questions, responses))
    return render_template('thanks.html', results = results, title = surveys.satisfaction_survey.title, len=surveys.satisfaction_survey.getLen())

  else:
    try:
      return render_template(
    'question.html',
    responses = responses,
    id=int(id), 
    questions = surveys.satisfaction_survey.questions, 
    survey = surveys.satisfaction_survey)
    except IndexError:
      return render_template('thanks.html', results = results, title = surveys.satisfaction_survey.title, len=surveys.satisfaction_survey.getLen())

