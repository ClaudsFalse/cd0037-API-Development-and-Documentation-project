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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    
    # test normal behaviour to get questions
    # endpoint: '/questions', methods=['GET']
    def test_get_questions(self):
       
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # test failure behaviour to get questions
    # endpoint: '/questions', methods=['POST']
    # error: 405
    def test_get_questions405(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')
    
    # test normal behaviour to get categories
    # endpoint: '/categories', methods=['GET']
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # test failure behaviour to get categories
    # endpoint: '/categories', methods=['POST']
    # error: 405
    def test_get_categories405(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    # test normal behaviour for deleting a question
    # endpoint: '/questions/<int:question_id>', methods=['DELETE']
    def test_delete_question(self):
        test_existing_question = Question.query.first()
        test_question_id = test_existing_question.id
        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_question_id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'],"")
    
    # test failure behaviour for deleting a question
    # endpoint: '/questions/<int:question_id>', methods=['DELETE']
    # error: 422
    def test_delete_question422(self):
        test_question_id = 9999999
        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
    # test normal behaviour for adding a question
    # endpoint: '/questions/add', methods=['POST']
    def test_add_question(self):
        # create a mock new question to test the route
        new_question = {
            'question': 'Is this a sample question?',
            'answer': 'Yes',
            'difficulty': 1,
            'category': '1'
        }
        questions_prior = Question.query.all()
        res = self.client().post(f'/questions/add', json=new_question)
        questions_after = Question.query.all()
        data = json.loads(res.data)
        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # check that our question count in the database has increased by 1
        self.assertTrue(len(questions_prior) - len(questions_after) == -1)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'],"")

    # test failure behaviour for adding a question
    # endpoint: '/questions/add', methods=['POST']
    # error: 422
    def test_add_question422(self):
        # test a case when the question is empty
        res = self.client().post('/questions/add', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unprocessable')
    
    # test normal behaviour for searching a question 
    # endpoint: '/questions/search', methods=['POST']
    def test_search_question(self):
        # get a word from an existing question in the db 
        question = Question.query.first()
        question_words = (question.question.split())
        search_term = question_words[1]

        res = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'],"")

    # test failing behaviour for searching a question 
    # endpoint: '/questions/search', methods=['POST']
    # error: 404
    def test_search_question404(self):
        # use a searchterm we know is not in the db
        res = self.client().post('/questions/search', json={'searchTerm': '345fdrt'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # test normal behaviour for getting questions by category
    # endpoint: /categories/<int:category_id>/questions, methods=['GET']
    # error: 404
    def test_get_questions_by_category(self):
        # get existing category id
        category = Category.query.first()
        res = self.client().get(f'/categories/{category.id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'],"")

    # test failing behaviour for getting questions by category
    # endpoint: /categories/<int:category_id>/questions, methods=['GET']
    def test_get_questions_by_category404(self):
        # get existing category id
        category_id = 12345678
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not found')

    # test normal behaviour for playing quiz
    # endpoint: /quizzes, methods=['POST']
    def test_start_quiz(self):
        body = {
            'previous_questions': [9],
            'quiz_category': {
                'type': 'History',
                'id': '4'
            }
        }
        res = self.client().post('/quizzes',
                                      json=body)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 4)

    # test failing behaviour for playing quiz
    # endpoint: /quizzes, methods=['POST']
    # error: 404 
    def test_start_quiz400(self):
        quiz = {
            'previous_questions': [6],
            'quiz': {
                'type': 'Music',
                'id': '78'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

        '''
        
test_get_categories failure scenario ✅
test_get_questions_no_page failure scenario ✅
test_delete_question success scenario ✅
test_add_question success and failure scenario ✅
test_search_questions success and failure scenario ✅
test_get_questions_by_category success and failure scenario ✅
test_play_quiz success and failure scenario
        
        
        
        '''



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()