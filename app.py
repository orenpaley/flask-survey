
from crypt import methods
import pdb
from tarfile import LENGTH_LINK
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

#holds the survey and question classes
import surveys

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'abcdef'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False




toolbar = DebugToolbarExtension(app)

surveys = surveys.surveys
surveySelected = False

#as user answers questions, answers will be stored here
responses = {}
for survey in surveys:
  responses[survey] = []



@app.route('/', methods=['GET', 'POST'])
def surveyHome():
  "pick survey"
  return render_template('home.html', surveys = surveys)
    

@app.route('/initialize')
def initSurvey():
  session['responseDict'] = responses
  curSurvey = request.args.get('survey')
  # responseDict[survey].clear()
  return redirect(f'/questions/{curSurvey}/0')

@app.route('/thanks/<survey>')
def completedSurvey(survey):
  'when user completes survey they will be redirected here to view res'
  print('#######')
  print('SURVEY COMPLETED')
  print(survey)
  print('###########')
  return render_template(
    'thanks.html',
  results = dict(zip(surveys[survey].questions,session['responseDict'][survey])), 
  title = surveys[survey].title, 
  len=surveys[survey].getLen(),
  survey = survey)

@app.route('/questions/<survey>/<id>', methods=['GET', 'POST'])
def getQuestion(survey,id):
  'gets question based on responses then redirects to answer'

  
  # print("***RESPONSE DICT AND LEN***")
  # print(session['responseDict'], len(session['responseDict'][survey]))



  if len(session['responseDict'][survey]) == 0 :
    #protects user from not starting survey on 1st question
    flash('Get ready to take a survey!')
    return render_template(
      'question.html', 
      id=0,
      questions=surveys[survey].questions,
      title=surveys[survey].title,
      survey = survey
  )
  elif int(id)!= len(session['responseDict'][survey]):
    #forces user to stay on current question while taking survey
    flash('question out of index or order')
    return render_template(
      'question.html', 
      survey = survey,
      id=len(session['responseDict'][survey]),
      questions=surveys[survey].questions,
      title=surveys[survey].title
  )

  elif len(session['responseDict'][survey]) >= surveys[survey].getLen():
    #check if survey is complete then redirects
    return redirect(f'/thanks/{survey}')

  else:
    #provides active question once all other protections pass
    return render_template(
      'question.html', 
      id=int(id),
      questions=surveys[survey].questions,
      title=surveys[survey].title,
      survey=survey
  )

@app.route('/answer/<survey>/<id>', methods=['GET', 'POST'])
def getAnswer(survey, id):
  'appends user response from url params and increments id to +1'
  choice = request.args.get('choice', 'not submitted')

  print('&&&& ANSWER SECTION &&&&&')
  print('******CHOICE*****')
  print(choice)
  #append to session using a temp variable and swap method
  temp = session['responseDict']
  temp[survey].append(choice)
  session['responseDict'] = temp


  print('***** RESPONSE DICT ******')
  print(session['responseDict'])
  
  
  print('************responseDictSurvey******')
  print(session['responseDict'][survey], type(session['responseDict'][survey]))

  print('*****SURVEY******')
  print(survey)
   
  print('*****ID*****')
  print(id)
  return redirect(f'/questions/{survey}/{int(id) + 1}')


