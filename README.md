## movie_service

### Description

Whole idea of project is based on fetching movies by title from OBDb API 
and save them into local database. There is additional filters and ordering for movies and comments:
#### Filters:
* Movie (/movies/):
    * title
    * year
    * genre
    * writer
    * actors
    * language
    * country
    * type
    * deleted
    
* Comment (/comments/):
    * movie__id
    
* Top (/top/):
    * start_date
    * end_date
    
#### Orders:
* Movie:
    * title
    * year
    * imdbrating

### Heroku:

The project is deployed on Heroku and could be accessed by: https://warm-reef-91851.herokuapp.com/

### Install:
 
 There are few ways to do it:
* ##### Docker:

    * git clone git@github.com:darencorp/movie_service.git
    
    * docker-compose up -d
    
    * Open your browser on http://localhost:8000

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You can run tests with:  docker-compose exec web python /app/manage.py test


* ##### Install from source

    * git clone git@github.com:darencorp/movie_service.git

    * Make new virtualenv for python3.7 via pyenv, anaconda or virtualenv
    
    * Activate your virtualenv
    
    * Run: pip install -r requirements.txt
    
    * Start app with: gunicorn movie_service.wsgi

    * Open your browser on http://localhost:8000



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You can run tests with: python manage.py test



