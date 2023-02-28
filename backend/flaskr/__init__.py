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
    Set up CORS. Allow '*' for origins. 
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
                abort(422)
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
            abort(422)

    @app.route('/questions/add', methods=['POST'])
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

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if search_term:
   
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = paginate_questions(request, questions)
            categories = Category.query.all()
            if questions is None:
                abort(404)
            return jsonify({'questions': formatted_questions,
            'total_questions': len(Question.query.all()),
            'categories': {category.id: category.type for category in categories},
            'current_category': ""})
        else:
            selection = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, selection)
            categories = Category.query.all()

            return jsonify({'questions': questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': ""})


    # endpoint to get questions baded on categories
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        
        try:
            selection = Question.query.filter_by(category=category_id).order_by(Question.id).all()
            if selection is None:
                abort(404)
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
            print(e, e.args)
            abort(422)
     

 
    # post endpoint to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        body = request.get_json()
        
        try:
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')['id']
            # if user presses on "all" it is read as category id == 0
            if quiz_category == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category == quiz_category).all()
            random_idx = random.randrange(0, len(questions))
            current_question = questions[random_idx].format()
            # when we run out of questions
            if len(questions) == 0:
                current_question = None

            return jsonify({
              'success':True,
              'question':current_question,
              'total_questions' : len(questions),
              })
        except Exception as e:
            abort(400)
            
            
    # error handlers        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success":False,
        "error": 404,
        "message": "Not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success":False,
        "error": 422,
        "message": "Unprocessable"
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message":"Bad Request"
        }), 400
    

    return app

