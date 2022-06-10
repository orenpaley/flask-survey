
from crypt import methods
import pdb
from tarfile import LENGTH_LINK
from flask import Flask, request, render_template, redirect, flash
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
  "view home/button to start survey"
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
  'gets question based on responses then redirects to answer'
  if len(responses) == 0:
    #protects user from not starting survey on 1st question
    flash('Get ready to take a survey!')
    return render_template(
      'question.html', 
      id=0,
      questions=survey.questions,
      title=survey.title
  )
  elif int(id)!= len(responses):
    #forces user to stay on current question while taking survey
    flash('question out of index or order')
    return render_template(
      'question.html', 
      id=len(responses),
      questions=survey.questions,
      title=survey.title
  )

  elif int(id) >= survey.getLen():
    #check if survey is complete then redirects
    return redirect('/thanks')

  else:
    #provides active question once all other protections pass
    return render_template(
      'question.html', 
      id=int(id),
      questions=survey.questions,
      title=survey.title
  )

@app.route('/answer/<id>',)
def getAnswer(id):
  'appends user response from url params and increments id to +1'
  choice = request.args.get('choice', 'not submitted')
  responses.append(choice)
  return redirect(f'/questions/{int(id) + 1}')


