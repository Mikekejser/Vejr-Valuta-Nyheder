import unittest
from app import app, db
from app.models import Bruger
import requests


class BrugerModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        bruger = Bruger(brugernavn='bob')
        bruger.set_password('bobby')
        self.assertFalse(bruger.check_password('blabla'))
        self.assertTrue(bruger.check_password('bobby'))


class TestAPIS(unittest.TestCase):
    def test_vejr_api(self):
        VEJR_APPID = app.config['VEJR_APPID']
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q=london&units=metric&appid={VEJR_APPID}')
        self.assertEqual(r.status_code, 200)

    def test_valuta_api(self):
        VALUTA_API_KEY = app.config['VALUTA_API_KEY']
        r = requests.get(f'http://data.fixer.io/api/latest?access_key={VALUTA_API_KEY}')
        self.assertEqual(r.status_code, 200)


class TestNyheder(unittest.TestCase):
    def test_tv2(self):
        r = requests.get('http://tv2.dk')
        self.assertEqual(r.status_code, 200)

    def test_jp(self):
        r = requests.get('https://jyllands-posten.dk')
        self.assertEqual(r.status_code, 200)

    def test_borsen(self):
        r = requests.get('https://borsen.dk')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()