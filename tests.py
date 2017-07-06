from django.test import TestCase, Client

from rest_framework.test import APIClient

from pugorugh import models

DOG_DATA = [
    {
        "name": "Tom",
        "image_filename": "photo.jpg",
        "breed": "Pug",
        "age": 14,
        "gender": "m",
        "size": "s"
    },
    {
        "name": "Jim",
        "image_filename": "photo2.jpg",
        "breed": "Pitbull",
        "age": 60,
        "gender": "m",
        "size": "l"
    }
]
USER_DATA = {'username': 'user', 'password': 'password'}


class PugorughAPITest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.api_client = APIClient()
        models.User.objects.create_user(
            username='user',
            email='test@example.com',
            password='password'
        )
        for item in DOG_DATA:
            models.Dog.objects.create(**item)

    def setUp(self):
        auth = self.api_client.post('/api-token-auth/', USER_DATA)
        token = auth.data['token']
        # Use Token Auth for APIClient for each test
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def tearDown(self):
        self.api_client.credentials()

    def test_api_dogs_list(self):
        resp = self.api_client.get('/api/dog/')

        assert resp.status_code == 200
        assert len(resp.data) == 2

    def test_api_token_undecided_dogs(self):
        resp = self.api_client.get('/api/dog/-1/undecided/next/')

        assert resp.status_code == 200
        assert 'Tom' in resp.data['name']

    def test_api_dog_undecided_unauth(self):
        self.api_client.credentials()
        resp = self.api_client.get('/api/dog/-1/undecided/next/')

        assert resp.status_code == 401

    def test_api_dog_liked_dogs(self):
        resp = self.api_client.get('/api/dog/-1/liked/next/')

        assert resp.status_code == 404

