# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

-  [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

-  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches an object with key categories containing a list of dictionaries of categories in which the keys are the ids and the type which is the string of the category
- Request Arguments: None
- Returns: an object with key categories containing a list of dictionaries of the form
id: id int
type:category_string
key:value pairs.
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    .
    .
    .
  ],
  "message": "",
  "success": true
}

GET '/questions'
- Fetches an object with key questions
containing a list of dictionaries of questions in which the keys are the id , question,difficulty , answer and the category
and key total_questions
- Request Arguments: page  1,2,...
- Returns: an object with key questions containing a list of dictionaries of questions in the form
id: id int
answer:answer_string
category: category_string
question: question_string
difficulty: difficulty_int 0<4
key:value pairs.
"questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
   .
   .
   .

GET '/categories/<int:category_id>/questions'
- Fetches questions based on category id
- Request Arguments:None
- Returns: json object in th form
    {
      'questions':list_of_formatted_questions,
      'totalQuestions':totalQuestions_int,
      'currentCategory': Category_int
    }


DELETE '/questions/{id}'
- deletes the question with id=id
- Request Arguments:None
- Returns: object with keys success (True or False), and message of the process

key:value pairs.
{
      'success': True/False,
      'message':'question was deleted',
    }


POST '/questions'
- inserts a new question record to the database or searches for question by a substring of it
- Request Arguments:None
- Request payload:
    -for adding aqusetion : JSON object data with keys
    ['question','difficulty','answer','category'] and thier values
    -for search: JSON object  with key searchTerm :searchTerm_string
    --search is tested if no category provided--
- Response :
    -for successful question insertation
    {
      'success':True ,
      'message':'question inserted',
    }
    -for successful search
    {
        'questions':questions_list,
        'totalQuestions':totalQuestions_int ,
        'currentCategory': 1,
        'success':True ,
        'message':'search result fetched'}


POST '/quizzes'
-Gets questions to play the quiz.
  This endpoint takes category and previous question parameters from JSON object data
  and return a random questions within the given category,
  and not one of previous_questions
  and if category value is -1 it retruns question of any category

- Request Arguments:None
- Request payload:JSON object in the form
    {
        previous_questions:previous_questions_id_int,
        quiz_category:quiz_category_id_int
    }
- Returns :JSON response

    {
        'question': question_dict,
        'quiz_category':questions_category_id_int ,
    }
question_dict with key:value pairs.
id: id int
answer:answer_string
category: category_string
question: question_string
difficulty: difficulty_int 0<4



```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
