##movie_service

### Description

Whole idea of project is based on fetching movies by title from OBDb API 
and save them into local database. There is an additional filters for movies that already in database:
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


 
 There is few ways to do it:
* #####Docker:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; docker-compose up -d

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You can run tests with:  docker-compose exec web python /app/manage.py test


* ##### Install from source

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1. git clone git@github.com:darencorp/movie_service.git

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Make new virtualenv for python3.7 via pyenv, conda or virtualenv

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Activate your virtualenv

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Run: pip install -r requirements.txt

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. Start app with: gunicorn movie_service.wsgi

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6. Open your browser on http://localhost:8000



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You can run tests with: python manage.py test



