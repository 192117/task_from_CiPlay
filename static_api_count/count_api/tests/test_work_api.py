from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from count_api.models import Event


class EventTestClass(APITestCase):

    def setUp(self):
        event1 = {
            'date': '1999-01-01',
            'views': 1,
            'clicks': 1,
            'cost': '10.00'
        }
        event2 = {
            'date': '1999-01-02',
            'views': 2,
            'clicks': 2,
            'cost': '10.00'
        }
        event3 = {
            'date': '1999-01-03',
            'views': 5,
            'clicks': 5,
            'cost': '10.00'
        }
        Event.objects.create(**event1)
        Event.objects.create(**event2)
        Event.objects.create(**event3)

    def test_save(self):
        self.assertEqual(3, Event.objects.all().count(), 'Событий в БД при старте.')
        url = reverse('save')
        event4 = {
            'date': '1999-01-04',
            'views': 10,
            'clicks': 10,
            'cost': '10.00'
        }
        response = self.client.post(url, data=event4)
        self.assertEqual(4, Event.objects.all().count(), 'Количество событий неверное после save.')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, 'Неверный статус ответа')
        event1_from_date = Event.objects.all().last()
        self.assertEqual(1, event1_from_date.views, 'Неверное количество views')
        self.assertEqual(1, event1_from_date.clicks, 'Неверное количество clicks')
        self.assertEqual(10.00, event1_from_date.cost, 'Неверное количество cost')
        self.assertEqual(10.00, event1_from_date.cpc, 'Неверное количество cpc')
        self.assertEqual(10000.00, event1_from_date.cpm, 'Неверное количество cpm')

    def test_get(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/show/1998-01-01/2000-01-01/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = [
            {
                "date": "1999-01-03",
                "views": 5,
                "clicks": 5,
                "cost": "10.00",
                "cpc": "2.00",
                "cpm": "2000.00"
            },
            {
                "date": "1999-01-02",
                "views": 2,
                "clicks": 2,
                "cost": "10.00",
                "cpc": "5.00",
                "cpm": "5000.00"
            },
            {
                "date": "1999-01-01",
                "views": 1,
                "clicks": 1,
                "cost": "10.00",
                "cpc": "10.00",
                "cpm": "10000.00"
            }
        ]
        self.assertEqual(data, response.data)

    def test_get_ordering_cost(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/show/1998-01-01/2000-01-01/?ordering=cost')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = [
            {
                "date": "1999-01-01",
                "views": 1,
                "clicks": 1,
                "cost": "10.00",
                "cpc": "10.00",
                "cpm": "10000.00"
            },
            {
                "date": "1999-01-02",
                "views": 2,
                "clicks": 2,
                "cost": "10.00",
                "cpc": "5.00",
                "cpm": "5000.00"
            },
            {
                "date": "1999-01-03",
                "views": 5,
                "clicks": 5,
                "cost": "10.00",
                "cpc": "2.00",
                "cpm": "2000.00"
            }
        ]
        self.assertEqual(data, response.data)

    def test_get_ordering_cost_des(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/show/1998-01-01/2000-01-01/?ordering=-cost')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = [
            {
                "date": "1999-01-01",
                "views": 1,
                "clicks": 1,
                "cost": "10.00",
                "cpc": "10.00",
                "cpm": "10000.00"
            },
            {
                "date": "1999-01-02",
                "views": 2,
                "clicks": 2,
                "cost": "10.00",
                "cpc": "5.00",
                "cpm": "5000.00"
            },
            {
                "date": "1999-01-03",
                "views": 5,
                "clicks": 5,
                "cost": "10.00",
                "cpc": "2.00",
                "cpm": "2000.00"
            }
        ]
        self.assertEqual(data, response.data)

    def test_get_big_from(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/show/2000-01-01/2001-01-01/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = []
        self.assertEqual(data, response.data)

    def test_clear(self):
        self.assertEqual(3, Event.objects.all().count(), 'Событий в БД при старте.')
        url = reverse('clear')
        response = self.client.get(url)
        data = []
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)
        self.assertEqual(0, Event.objects.all().count(), 'Неверное количество событий после удаления.')
