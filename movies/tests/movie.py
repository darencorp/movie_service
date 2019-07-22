import datetime

from django.conf import settings

import responses
from django.test import TestCase
from rest_framework import status

from movies.models.comment import Comment
from movies.models.movie import Movie


class TestMovieAPI(TestCase):
    response = responses.RequestsMock()

    @response.activate
    def test_should_fetch_and_create_new_movie(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        response = self.client.post('/movies/', data={'title': 'test'})

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.values().first()['title'], movie_api_response['Title'])

    @response.activate
    def test_should_not_create_existing_movie(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        self.client.post('/movies/', data={'title': 'test'})
        response = self.client.post('/movies/', data={'title': 'test'})

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.values().first()['title'], movie_api_response['Title'])

    @response.activate
    def test_should_return_info_if_movie_not_found(self):
        movie_api_response = {
            "Error": "Movie not found.",
            "Response": "False"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=404)

        expected = f'Movie not found, test'

        response = self.client.post('/movies/', data={'title': 'test'})

        self.assertEqual(Movie.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    @response.activate
    def test_should_return_info_if_movie_cannot_be_processed(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "INCORRECT INTEGER",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "INCORRECT URL",
            "Response": "True"
        }

        expected = 'Server cannot fetch valid data from the API'

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        response = self.client.post('/movies/', data={'title': 'test'})

        self.assertEqual(Movie.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, expected)

    @response.activate
    def test_should_return_info_if_data_is_not_valid(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "32 Aug 2017",  # not valid
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "32 Aug 2017",  # not valid
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        expected = 'Server cannot fetch valid data from the API'

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        response = self.client.post('/movies/', data={'title': 'test'})

        self.assertEqual(Movie.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, expected)

    @response.activate
    def test_should_return_list_of_existing_movies(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        expected = [{'id': 1,
                     'title': 'test',
                     'year': 2000,
                     'rated': 'PG-13',
                     'released': '2017-05-05',
                     'runtime': '100 min',
                     'genre': 'Test',
                     'director': 'Test Test',
                     'writer': 'Test Writers',
                     'actors': 'Test Test',
                     'plot': 'Test',
                     'language': 'Test',
                     'country': 'Test',
                     'awards': 'Test',
                     'poster': 'http://test.test',
                     'metascore': 67,
                     'imdbrating': 7.7,
                     'imdbvotes': '489,848',
                     'imdbid': 'tt1234567',
                     'type': 'movie',
                     'dvd': '2017-08-22',
                     'boxoffice': '$389,804,217',
                     'production': 'Walt Disney Pictures',
                     'deleted': False
                     }]

        self.client.post('/movies/', data={'title': 'test'})
        response = self.client.get('/movies/')

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), expected)

    @response.activate
    def test_should_return_single_movie_instance(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        expected = {'id': 1,
                    'title': 'test',
                    'year': 2000,
                    'rated': 'PG-13',
                    'released': '2017-05-05',
                    'runtime': '100 min',
                    'genre': 'Test',
                    'director': 'Test Test',
                    'writer': 'Test Writers',
                    'actors': 'Test Test',
                    'plot': 'Test',
                    'language': 'Test',
                    'country': 'Test',
                    'awards': 'Test',
                    'poster': 'http://test.test',
                    'metascore': 67,
                    'imdbrating': 7.7,
                    'imdbvotes': '489,848',
                    'imdbid': 'tt1234567',
                    'type': 'movie',
                    'dvd': '2017-08-22',
                    'boxoffice': '$389,804,217',
                    'production': 'Walt Disney Pictures',
                    'deleted': False
                    }

        self.client.post('/movies/', data={'title': 'test'})
        response = self.client.get('/movies/1/')

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected)

    @response.activate
    def test_movie_year_should_be_updated(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        expected = {'id': 1,
                    'title': 'test',
                    'year': 2001,
                    'rated': 'PG-13',
                    'released': '2017-05-05',
                    'runtime': '100 min',
                    'genre': 'Test',
                    'director': 'Test Test',
                    'writer': 'Test Writers',
                    'actors': 'Test Test',
                    'plot': 'Test',
                    'language': 'Test',
                    'country': 'Test',
                    'awards': 'Test',
                    'poster': 'http://test.test',
                    'metascore': 67,
                    'imdbrating': 7.7,
                    'imdbvotes': '489,848',
                    'imdbid': 'tt1234567',
                    'type': 'movie',
                    'dvd': '2017-08-22',
                    'boxoffice': '$389,804,217',
                    'production': 'Walt Disney Pictures',
                    'deleted': False
                    }

        self.client.post('/movies/', data={'title': 'test'})
        self.client.patch('/movies/1/', data={'year': 2001}, content_type='application/json')
        response = self.client.get('/movies/1/')

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected)

    @response.activate
    def test_movie_should_not_be_deleted(self):
        movie_api_response = {
            "Title": "test",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test',
                          json=movie_api_response, status=200)

        self.client.post('/movies/', data={'title': 'test'})
        self.client.delete('/movies/1/')
        response = self.client.get('/movies/1/')
        response_data = response.json()

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['deleted'], True)


class TestTopEndpoint(TestCase):
    response = responses.RequestsMock()

    def setUp(self):
        self.movie1_api_response = {
            "Title": "test1",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.movie2_api_response = {
            "Title": "test2",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.movie3_api_response = {
            "Title": "test3",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

        self.movie4_api_response = {
            "Title": "test4",
            "Year": "2000",
            "Rated": "PG-13",
            "Released": "05 May 2017",
            "Runtime": "100 min",
            "Genre": "Test",
            "Director": "Test Test",
            "Writer": "Test Writers",
            "Actors": "Test Test",
            "Plot": "Test",
            "Language": "Test",
            "Country": "Test",
            "Awards": "Test",
            "Poster": "http://test.test",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.7/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "67/100"
                }
            ],
            "Metascore": "67",
            "imdbRating": "7.7",
            "imdbVotes": "489,848",
            "imdbID": "tt1234567",
            "Type": "movie",
            "DVD": "22 Aug 2017",
            "BoxOffice": "$389,804,217",
            "Production": "Walt Disney Pictures",
            "Website": "https://test.test/test",
            "Response": "True"
        }

    @response.activate
    def test_should_return_one_movie_with_rank_1(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        
        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        
        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        self.assertEqual(response_data[0]['rank'], 1)

    @response.activate
    def test_should_return_two_movie_with_rank_1(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        
        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})

        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        
        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 2)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 1)
        self.assertEqual(response_data[1]['movie_id'], 2)

    @response.activate
    def test_should_return_two_movie_with_rank_1_and_2(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        
        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        
        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 1})
        
        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 2)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 2)
        self.assertEqual(response_data[1]['movie_id'], 2)

    @response.activate
    def test_should_return_three_movie_with_rank_1(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test3',
                          json=self.movie3_api_response, status=200)
        
        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        self.client.post('/movies/', data={'title': 'test3'})
        
        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        
        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})
        
        # comments for the third movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 3})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 3)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 1)
        self.assertEqual(response_data[1]['movie_id'], 2)
        
        self.assertEqual(response_data[2]['rank'], 1)
        self.assertEqual(response_data[2]['movie_id'], 3)

    @response.activate
    def test_should_return_three_movie_with_rank_1_and_2(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test3',
                          json=self.movie3_api_response, status=200)

        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        self.client.post('/movies/', data={'title': 'test3'})
        
        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 1})
        
        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})
        
        # comments for the third movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 3})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 3)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 2)
        self.assertEqual(response_data[1]['movie_id'], 2)
        
        self.assertEqual(response_data[2]['rank'], 2)
        self.assertEqual(response_data[2]['movie_id'], 3)

    @response.activate
    def test_should_return_three_movie_with_rank_1_and_2_and_3(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test3',
                          json=self.movie3_api_response, status=200)

        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        self.client.post('/movies/', data={'title': 'test3'})

        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test3', 'movie': 1})

        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 2})
        
        # comments for the third movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 3})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 3)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 2)
        self.assertEqual(response_data[1]['movie_id'], 2)
        
        self.assertEqual(response_data[2]['rank'], 3)
        self.assertEqual(response_data[2]['movie_id'], 3)

    @response.activate
    def test_should_return_three_movie_with_rank_1_and_2_and_3_without_forth_movie(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test3',
                          json=self.movie3_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test4',
                          json=self.movie4_api_response, status=200)

        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        self.client.post('/movies/', data={'title': 'test3'})
        self.client.post('/movies/', data={'title': 'test4'})

        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test3', 'movie': 1})
        self.client.post('/comments/', data={'body': 'test3', 'movie': 1})

        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 2})
        self.client.post('/comments/', data={'body': 'test3', 'movie': 2})

        # comments for the third movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 3})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 3})

        # comments for the fourth movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 4})

        response = self.client.get('/top/')
        response_data = response.json()

        self.assertEqual(len(response_data), 3)
        
        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)
        
        self.assertEqual(response_data[1]['rank'], 2)
        self.assertEqual(response_data[1]['movie_id'], 2)
        
        self.assertEqual(response_data[2]['rank'], 3)
        self.assertEqual(response_data[2]['movie_id'], 3)

    @response.activate
    def test_should_filter_comments_and_return_ranks_1(self):
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test1',
                          json=self.movie1_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test2',
                          json=self.movie2_api_response, status=200)
        self.response.add('GET', f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test3',
                          json=self.movie3_api_response, status=200)

        # movies
        self.client.post('/movies/', data={'title': 'test1'})
        self.client.post('/movies/', data={'title': 'test2'})
        self.client.post('/movies/', data={'title': 'test3'})

        # comments for the first movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 1, 'created': '2017-01-01'})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 1, 'created': '2016-01-01'})
        self.client.post('/comments/', data={'body': 'test3', 'movie': 1, 'created': '2015-01-01'})
        self.client.post('/comments/', data={'body': 'test4', 'movie': 1, 'created': '2014-02-02'})

        # comments for the second movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 2, 'created': '2017-01-01'})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 2, 'created': '2016-01-01'})
        # self.client.post('/comments/', data={'body': 'test3', 'movie': 2, 'created': '2015-01-01'})

        # comments for the third movie
        self.client.post('/comments/', data={'body': 'test', 'movie': 3, 'created': '2013-01-01'})
        self.client.post('/comments/', data={'body': 'test2', 'movie': 3, 'created': '2012-01-01'})

        response = self.client.get('/top/?start_date=2014-01-01&end_date=2017-02-02')
        response_data = response.json()

        self.assertEqual(len(response_data), 3)

        self.assertEqual(response_data[0]['rank'], 1)
        self.assertEqual(response_data[0]['movie_id'], 1)

        self.assertEqual(response_data[1]['rank'], 1)
        self.assertEqual(response_data[1]['movie_id'], 2)

        self.assertEqual(response_data[2]['rank'], 1)
        self.assertEqual(response_data[2]['movie_id'], 3)
