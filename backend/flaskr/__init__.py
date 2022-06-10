from flask import Flask, request, abort, jsonify, redirect, url_for
from .models import setup_db, Question, Category
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import random


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    current_question = questions[start:end]
    
    return current_question

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Method', 'GET, POST, DELETE, PATCH, PUT')
        return response


    @app.route('/')
    def home():
        
        return jsonify({
            'success': True,
            "Code": 200,
            "message": "Trivia Game Restful API. Please read the README.md file for how to start"
        })
   
    # Create an endpoint to handle GET requests for all available categories.
  
    @app.route('/categories', methods=['GET'])
    def get_categories():
        
        all_categories = Category.query.order_by(Category.type).all()
        
        if len(all_categories) < 1:
            abort(404)
            
        data =  {category.id: category.type for category in all_categories}

        return jsonify({
            'success': True,
            'code': 200,
            'categories': data
        }), 200
        
    
    #  endpoint to get all questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_question = paginate_questions(request, selection)
        total_question = Question.query.count()
        data =  {category.id: category.type for category in Category.query.all()}

        
        
        if len(current_question) < 1:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_question,
            'total_question': total_question,
            'current_category': [],
            'category': data
        }), 200

    
        # his endpoint gets question by Id 

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def del_question(question_id):
        try:
            questions = Question.query.filter(Question.id == question_id).one_or_none()
            
            if questions:
                questions.delete()
            elif question is None:
                abort(404)
            
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)
            
            return jsonify({
                'success': True,
                'deleted_question': question_id,
                'question': current_question,
                'total_questions': Question.query.count()
            }), 200
                
        except:
            abort(422)

    
    #  this endpoint handles creating new questions
    
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        
        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get('difficulty', None)
        
        try:
            new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)
            
            return jsonify({
                'success': True,
                'new_question': new_question.id,
                'current_question': current_question,
                'total_question': question.query.count()
            })

        except:
            abort(422)
            

    # this endpoiny handles search request for questions
    @app.route('/questions/search', methods=['POST'])
    def searched():
        try:
            
            body = request.get_json()
            search = body.get("searchTerm", None)
            queries = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
            current_query = (query.format() for query in queries)
            
            return jsonify({
                'success': True,
                'questions': current_query,
                'total_questions': len(queries),
                'current_category': None
            }),200
            
        except:
            abort(404)
        
        


    # this endpoint retrive questions by their categories
    
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        
        catrgory_id = category_id + 1
        
        try:
            category = Category.query.filter(Category.id == category_id).first()
            
            required_categories = [category.type for category in Category.query.all()]

            selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
            
            current_questions = paginate_questions(request, selection)
            
        

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': required_categories,
                'current_category': category.format()
            })
        
        except:
            abort(404)
    
    
    
    # the get quizzes function create the quizzes for the game
    
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        try:
            body = request.get_json()
            
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter( Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(422)

    
   
    # error handlers
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not Processable"
        }), 422


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app

