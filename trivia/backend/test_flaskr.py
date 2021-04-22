import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:00202@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        '''testing fetching categories'''
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        
    def test_get_paginated_questions(self):
        '''testing fetching paginated questions'''
        res = self.client().get('/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])


    def test_delete_question_by_id(self):
        '''testing deleting question by id'''
        res = self.client().delete('/questions/6')
        data=json.loads(res.data)
        testq=Question.query.filter(Question.id==5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(testq, None)

    def test_422_delete_question_by_id(self):
        '''testing 422 deleting question by id'''
        
        res = self.client().delete('/questions/{}'.format(100))
        self.assertEqual(res.status_code, 422)
       


    
    def test_get_questions_by_category(self):
        '''testing fetching questions by category'''
        res = self.client().post('/categories/4/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

        
    
    
    def test_post_new_question(self):
        '''testing posting a question'''
        res = self.client().post('/questions', json={
            'question': 'test question',
            'category':4,
            'answer': 'test answer',
            'difficulty':1
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'question inserted')



    def test_post_search_term(self):
        '''testing posting a search term'''
        res = self.client().post('/questions', json={
            'searchTerm': 'eg',
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'search result fetched')
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])
    
    def test_422_post_to_questions(self):    
        '''testing 422 for post to questions '''
        res = self.client().post('/questions', json={
            'test': 'none',
        })
        self.assertEqual(res.status_code,422)
       



    def test_post_to_start_quizzes(self):
        '''testing starting quizzes'''
        res = self.client().post('/quizzes', json={
            'previous_questions':[],
            'quiz_category':4
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['question'])




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()