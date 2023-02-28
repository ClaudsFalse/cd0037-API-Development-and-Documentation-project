# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Endpoints Documentation

`GET '/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding name of the category
- Request Arguments: None
- Returns: a json object with the success key, and another key: `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/categories/<int:category_id>/questions'`
- Fetches questions filtered by a chosen category
- Request Arguments: Category id of the category chosen
- Returns: a json object with the success key, and 4 more keys:

    1. questions: paginated questions, in this case 10 per page. 
    2. total_questions: total amount of questions in the database. 
    3. categories: a dictionary of all categories with key-value pairs being the category unique id and its name. 
    4. current_category: set as an empty string.  



`GET '/questions'`
- Fetches a list of all question objects present in the database.
- Request Arguments: None
- Returns: a json object with the success value and 4 more keys:

    1. questions: paginated questions, in this case 10 per page. 
    2. total_questions: total amount of questions in the database. 
    3. categories: a dictionary of all categories with key-value pairs being the category unique id and its name. 
    4. current_category: set as an empty string. 

`DELETE '/questions/<int:question_id>'`
- Deletes a question from the database based on its id.
- Request Arguments: question id.
- Returns: a json object with the success value and 5 more keys:
    1. questions: paginated questions, in this case 10 per page. 
    2. total_questions: total amount of questions in the database. 
    3. categories: a dictionary of all categories with key-value pairs being the category unique id and its name. 
    4. current_category: set as an empty string. 
    5. deleted: the question id of the deleted question 

`POST '/questions/add'`
- Adds a question on the database based on user inputted data. 
- Request Arguments: 
    * question: the question text
    * answer: the answer to the question
    * difficulty: the question's difficulty
    * category: which category the question belongs to

- Returns: a json object with the success value and 4 more keys:
    1. questions: paginated questions, in this case 10 per page. 
    2. total_questions: total amount of questions in the database. 
    3. categories: a dictionary of all categories with key-value pairs being the category unique id and its name. 
    4. current_category: set as an empty string. 

`POST '/questions/search'`
- Fetches questions based on partial matches with a given search term. 
- Request Arguments: the search term ('searchTerm')
- Returns: a json object with 4 keys:
    1. questions: paginated questions, in this case 10 per page. 
    2. total_questions: total amount of questions in the database. 
    3. categories: a dictionary of all categories with key-value pairs being the category unique id and its name. 
    4. current_category: set as an empty string. 

`GET '/quizzes'`
- Fetches a question at a time to let the user play the game.
- Request Arguments: 
    * previous_questions = ids of previously shown questions so that user doesn't see repeats. 
    * quiz_category = if they chose it, users will only see questions of a chosen category. 
- Returns: a json object with the success value and 2 more keys:

    1. question: the current question
    2. total_questions: total amount of questions in the database. 

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
