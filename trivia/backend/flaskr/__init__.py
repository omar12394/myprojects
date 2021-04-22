import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  app.config.from_mapping(
  SECRET_KEY='dev',
  DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
  )
  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
    all_categories = Category.query.all()
    formatted_categories = [i.format() for i in all_categories]
    
    return jsonify({
      'success': True,
      'message':'',
      'categories':formatted_categories})
    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions',methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    formatted_questions=[i.format() for i in Question.query.all()]
    startq=(page-1)*QUESTIONS_PER_PAGE
    endq = startq + QUESTIONS_PER_PAGE
    all_categories = Category.query.all()
    formatted_categories = [i.format() for i in all_categories]

    return jsonify({
      'success': True,
      'message':'',
      'questions': formatted_questions[startq:endq],
      'total_questions': len(formatted_questions),
      'categories': formatted_categories,
      'current_category':formatted_questions[0]['category']})  


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_quistion(question_id):
    try:
      q=Question.query.get(question_id)
      q.delete()
    except:
      abort(422)
    return jsonify({
      'success': True,
      'message':'question was deleted',
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def add_new_question():
    newq = Question('', '', 1, 1)
    data = request.get_json(force=True)
    print(data)
    s={}
    for i in data.keys():#['question','difficulty','answer','category','searchTerm']
      setattr(newq, i, data[i])
      
    try:
      i=data['category']
      newq.insert()
      s={
      'success':True ,
      'message':'question inserted',
      }
    except:
      try:
        i=data['searchTerm']
        questions=Question.query.filter(Question.question.ilike('%'+data['searchTerm']+'%')).all()
        formatted_questions = [i.format() for i in questions]

        s = {
        'questions':formatted_questions,
        'totalQuestions': len(formatted_questions),
        'currentCategory': 1,
        'success':True ,
        'message':'search result fetched'}
      except:
        abort(422)
    return jsonify(s)



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  #handeld in the previous POST '/question'  endpoint
  

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  #GET replaced by POST
  @app.route('/categories/<int:category_id>/questions', methods = ['POST'])
  def search_questions(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [i.format() for i in questions]
    return jsonify({
      'questions':formatted_questions,
      'totalQuestions':len(formatted_questions),
      'currentCategory': Category.query.get(category_id).id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes',methods=['POST'])
  def quiz():
    r = request.get_json(force=True)
    newqs=[]  #new questions
    if r['quiz_category']!=-1:
      questions = Question.query.filter(Question.category==r['quiz_category'],(Question.id not in r['previous_questions'])).all()
    else:
      questions = Question.query.all()
    formatted_questions = [i.format() for i in questions]
    #filtering questions
    for i in formatted_questions:
      if i['id'] not in r['previous_questions']:
        newqs.append(i)
    print(r['previous_questions'])
    try:
      q = newqs[random.randint(0, len(newqs) - 1)]  #getteing random question
    except:
      q={
      'id':-1,
      'question': "no more questions in this category",
      'answer': "001",
      'category':r['quiz_category'],
      'difficulty': r['quiz_category']
    }
    return jsonify({
               'question': q,
               'quiz_category':q['category'] ,
            })
    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message":"Bad Request"
    }), 400
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":"Not Found"
    }),404
  
  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message":"Unprocessable Entity"
    }), 422
  @app.errorhandler(500)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message":"internal server error "
    }), 500
    
  return app

    