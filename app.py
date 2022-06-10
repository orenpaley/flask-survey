
from crypt import methods
import pdb
from tarfile import LENGTH_LINK
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

#holds the survey and question classes
import surveys

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'abcdef'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

survey = surveys.satisfaction_survey


toolbar = DebugToolbarExtension(app)

#as user ansewers questions answers will be stored here
responses = []


@app.route('/')
def surveyHome():
  'clears responses and allows user to start survey'
  responses.clear()
  return render_template(
  'satisfaction.html', 
  survey = survey)

@app.route('/thanks')
def completedSurvey():
  'when user completes survey they will be redirected here to view res'
  return render_template(
    'thanks.html',
  results = dict(zip(survey.questions,responses)), 
  title = survey.title, 
  len=survey.getLen())

@app.route('/questions/<id>', methods=['GET', 'POST'])
def getQuestion(id):
  return render_template('question.html', 
  id=int(id),
  questions=survey.questions,
  title=survey.title
  )



@app.route('/answer/<id>',)
def getAnswer(id):
  choice = request.args.get('choice', 'not submitted')
  responses.append(choice)
  print('*****CHOICE ID*****')
  print('************')
  print(choice, id)
  if int(id) >= 3:
    return redirect('/thanks')
  else:
    return redirect(f'/questions/{int(id) + 1}')








  # if id >= surveys.satisfaction_survey.getLen():
  #   results = dict(zip(surveys.satisfaction_survey.questions, responses))
  #   return render_template('thanks.html', results = results, title = surveys.satisfaction_survey.title, len=surveys.satisfaction_survey.getLen())

  # else:
  #   try:
  #     return render_template(
  #   'question.html',
  #   responses = responses,
  #   id=int(id), 
  #   questions = surveys.satisfaction_survey.questions, 
  #   survey = surveys.satisfaction_survey)
  #   except IndexError:
  #     return render_template('thanks.html', results = results, title = surveys.satisfaction_survey.title, len=surveys.satisfaction_survey.getLen())

