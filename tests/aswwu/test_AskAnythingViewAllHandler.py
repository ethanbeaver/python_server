import pytest
import requests
import json

import threading

import tornado.ioloop
from tornado.options import define
import sqlite3



@pytest.fixture()
def test_db():
    data = [(1, "2016-01-01 10:20:05.123", "Somthing", True, True),
            (2, "2016-01-01 10:20:05.124", "Somthing Else", True, True),
            (3, "2016-01-01 10:20:05.125", "Somthing More", True, True)]

    conn = sqlite3.connect(
        '/home/charlie/School/Fall_2017/Software_Testing/labs/python_server/databases/people.db'
    )
    with conn:
        conn.executemany('INSERT INTO askanythings VALUES (?,?,?,?,?)', data)
    yield
    with conn:
        conn.execute('DElETE FROM askanythings')
    conn.close()


@pytest.fixture()
def test_db_with_votes():
    data = [(1, "2016-01-01 10:20:05.123", "Somthing", True, True),
            (2, "2016-01-01 10:20:05.124", "Somthing Else", True, True),
            (3, "2016-01-01 10:20:05.125", "Somthing More", True, True)]

    data2 = [(1, "2016-01-01 10:20:05.126", 1, "ryan.rabello"),
             (2, "2016-01-01 10:20:05.127", 2, "ryan.rabello"),
             (3, "2016-01-01 10:20:05.128", 3, "ryan.rabello")]

    conn = sqlite3.connect(
        '/home/charlie/School/Fall_2017/Software_Testing/labs/python_server/databases/people.db'
    )
    with conn:
        conn.executemany('INSERT INTO askanythings VALUES (?,?,?,?,?)', data)

    with conn:
        conn.executemany('INSERT INTO askanythingvotes VALUES (?,?,?,?)', data2)

    yield
    with conn:
        conn.execute('DElETE FROM askanythings')

    with conn:
        conn.execute('DELETE FROM askanythingvotes')
    conn.close()


def test_No_Data(testing_server):

    expected_data = []

    url = "http://127.0.0.1:8888/askanything/view"
    resp = requests.get(url)
    assert (resp.status_code == 200)
    assert (json.loads(resp.text) == expected_data)


def test_Data(testing_server, test_db):
    expected_data = [{
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"1",
    }, {
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing Else",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"2",
    }, {
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing More",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"3",
    }]

    url = "http://127.0.0.1:8888/askanything/view"
    resp = requests.get(url)
    assert (resp.status_code == 200)
    assert (json.loads(resp.text) == expected_data)


def test_Data_with_votes(testing_server, test_db_with_votes):
    expected_data = [{
        u"votes": 1,
        u"reviewed": True,
        u"question": u"Somthing",
        u"authorized": True,
        u"has_voted": True,
        u"question_id": u"1",
    }, {
        u"votes": 1,
        u"reviewed": True,
        u"question": u"Somthing Else",
        u"authorized": True,
        u"has_voted": True,
        u"question_id": u"2",
    }, {
        u"votes": 1,
        u"reviewed": True,
        u"question": u"Somthing More",
        u"authorized": True,
        u"has_voted": True,
        u"question_id": u"3",
    }]

    url = "http://127.0.0.1:8888/askanything/view"
    resp = requests.get(url)
    assert (resp.status_code == 200)
    assert (json.loads(resp.text) == expected_data)
