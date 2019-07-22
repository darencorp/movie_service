import responses
from django.test import TestCase
from django.conf import settings
from rest_framework import status

from movies.models.comment import Comment


class TestCommentsApi(TestCase):
    response = responses.RequestsMock()

    @response.activate
    def setUp(self):
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

    def test_should_create_new_comment(self):
        data = {
            'body': 'test',
            'movie': 1
        }

        response = self.client.post('/comments/', data=data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response_data['body'], data['body'])

    def test_should_update_comment(self):
        data = {
            'body': 'test',
            'movie': 1
        }

        self.client.post('/comments/', data=data)

        expected_body = 'new'

        response = self.client.patch('/comments/1/', data={'body': expected_body}, content_type='application/json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response_data['body'], expected_body)

    def test_should_return_single_comment_instance(self):
        data = {
            'body': 'test',
            'movie': 1
        }

        self.client.post('/comments/', data=data)
        response = self.client.get('/comments/1/')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['body'], data['body'])

    def test_should_return_list_of_comments(self):
        data = {
            'body': 'test',
            'movie': 1
        }

        self.client.post('/comments/', data=data)
        response = self.client.get('/comments/')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)

    def test_should_not_delete_comment(self):
        data = {
            'body': 'test',
            'movie': 1
        }

        self.client.post('/comments/', data=data)

        response = self.client.delete('/comments/1/')
        comment = Comment.objects.values().first()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment['deleted'], True)
