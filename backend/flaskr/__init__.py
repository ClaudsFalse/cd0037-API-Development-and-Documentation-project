import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # resources is an object where keys are uris for a given resource. 
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/categories')
    def get_all_categories():
        # query the database for all category objects 
        categories = Category.query.all()
        # create and populate a categories dictionary as required by the frontend
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict
            })

    @app.route('/questions')
    def get_questions():
        '''
        At this url, the frontend requires:
         * questions (paginated)
         * total_questions 
         * categories
         * current_category
        '''
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)
        categories = Category.query.all()

        # handle the case where there are no questions
        if len(questions) == 0:
            abort(404)
       
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category' : ""

        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
                abort(404)
            question.delete()
            print("deleted")
            selection = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, selection)
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': questions,
                'total_questions': len(selection),
                'categories': {category.id: category.type for category in categories},
                'current_category' : ""
            })
        except:
            abort(404)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, selection)
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(selection),
                'categories': {category.id: category.type for category in categories},
                'current_category' : ""
            })
        except Exception as e:
            print(e.message, e.args)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

