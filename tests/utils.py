#!/usr/bin/python2
"""This module contains convenience functions for creating data and inserting it into the databases
   for testing
"""
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, MetaData, String, Table, Integer, ForeignKey

from names import get_first_name, get_last_name

METADATA = MetaData()
ASKANYTHING_TABLE = Table('askanythings', METADATA,
                          Column('id', String(50), nullable=False),
                          Column('updated_at', DateTime),
                          Column('question', String(500), nullable=False),
                          Column('reviewed', Boolean),
                          Column('authorized', Boolean))

ASKANYTHING_VOTE_TABLE = Table('askanythingvotes', METADATA,
                               Column('id', String(50), nullable=False),
                               Column(
                                   'question_id', String(50), nullable=False),
                               Column('voter', String(75)))

JOB_POSTING_TABLE = Table('jobforms', METADATA,
    Column('id', Integer(), nullable=False),
    Column('job_name', String(100), nullable=False),
    Column('job_description', String(10000)),
    Column('department', String(150)),
    Column('visibility', Boolean, default=False),
    Column('owner', String(100), nullable=False),
    Column('image', String(100), nullable=False)
)

JOB_QUESTION_TABLE = Table('jobquestions', METADATA,
    Column('id', Integer(), nullable=False),
    Column('question', String(5000)),
    Column('jobID',String(50), ForeignKey('jobforms.id'))
)

JOB_APPLICATION_TABLE = Table('jobapplications', METADATA,
    Column('id', Integer(), nullable=False),
    Column('jobID', String(50), ForeignKey('jobforms.id')),
    Column('username', String(100), nullable=False),
    Column('status', String(50))
)

JOB_ANSWER_TABLE = Table('jobanswers', METADATA,
    Column('id', Integer(), nullable=False),
    Column('questionID', String(50), ForeignKey('jobquestions.id')),
    Column('answer', String(10000)),
    Column('applicationID', String(50), ForeignKey('jobapplications.id'))
)


def gen_askanythings(number=5):
    """Generate askanythings

    Keyword Arguments:
    number(int) -- The upper limit of generated records (default 5)

    Yields:
    dict        -- Record information

    """
    for i in xrange(number):
        yield {
            "id": i,
            "updated_at": datetime.now(),
            "question": "Something_{}".format(i),
            "reviewed": True,
            "authorized": True
        }


def gen_askanythingvotes(number=5):
    """Generate askanthing votes

    Keyword Arguments:
    number(int) -- The upper limit of generated records (default 5)

    Yields:
    dict        -- Record information

    """
    for i in xrange(number):
        yield {
            "id": i,
            "updated_at": datetime.now(),
            "question_id": 1,
            "voter": get_first_name() + '.' + get_last_name()
        }


def edit(generator, changes):
    """Edit the records produced by a generator and yield result

    Keyword Arguments:
    generator(generator(dict)) -- A generator which yields dicts
    changes(dict)              -- A dictionary of chages to be made

    Yields
    dict                       -- Modified records

    """
    for i, record in enumerate(generator):
        if i in changes.iterkeys():
            record.update(changes[i])

        yield record


@contextmanager
def askanything(conn, askanythings=None):
    """Insert list of records into askanything table

    Keyword Arguments:
    conn(conn)               -- A connection object to the database
    askanythings(list(dict)) -- Records to be inserted into the db (default None)

    """
    if askanythings is None:
        askanythings = list(gen_askanythings())

    conn.execute(ASKANYTHING_TABLE.insert(), askanythings)
    yield askanythings
    conn.execute(ASKANYTHING_TABLE.delete())


@contextmanager
def askanthingvote(conn, askanythingvotes=None):
    """Insert list of records into askanything table

    Keyword Arguments:
    conn(conn)                   -- A connection object to the database
    askanythingvotes(list(dict)) -- Records to be inserted into the db (default None)

    """
    if askanythingvotes is None:
        askanythingvotes = list(gen_askanythingvotes())

    conn.execute(ASKANYTHING_VOTE_TABLE.insert(), askanythingvotes)
    yield askanythingvotes
    conn.execute(ASKANYTHING_VOTE_TABLE.delete())


def gen_job_app(number=5):
    for i in xrange(2,number+2):
        yield {
            "id": i,
            "job_name": "Job number {}".format(i),
            "job_description": "A description for the job",
            "department": "department {}".format(i),
            "visibility": 0,
            "owner": get_first_name() + '.' + get_last_name(),
            "image": "/images/{}".format(i)
        }

def gen_job_answer(number_answers_per_app=5, num_apps=5):
    for i in xrange(1, number_answers_per_app*num_apps+2):
        yield {
            "id": i,
            "question": "Question Number {}".format(i),
            "jobID": i%(num_apps)+1
        }

def gen_job_posting(number=5):
    for i in xrange(2,number+2):
        yield {
            "id": i,
            "jobID": "Job number {}".format(i),
            "username": get_first_name() + '.' + get_last_name(),
            "status": ["new", "reviewed", "hire", "no"][i%4]
        }

def gen_job_question(number_questions_per_posting=5, num_postings=5):
    for i in xrange(1, number_questions_per_posting*num_postings+2):
        yield {
            "id": i,
            "question": "Question Number {}".format(i),
            "jobID": i%(num_postings)+1
        }

@contextmanager
def job_application(conn, job_apps=None):
    job_apps = job_apps or list(gen_job_app())

    conn.execute(JOB_APPLICATION_TABLE.insert(), job_apps)
    yield job_apps
    conn.execute(JOB_APPLICATION_TABLE.delete())

@contextmanager
def job_answer(conn, job_answers=None):
    job_answers = job_answers or list(gen_job_answer())

    conn.execute(JOB_ANSWER_TABLE.insert(), job_answers)
    yield job_answers
    conn.execute(JOB_ANSWER_TABLE.delete())

@contextmanager
def job_posting(conn, job_postings=None):
    job_postings = job_postings or list(gen_job_posting())

    conn.execute(JOB_POSTING_TABLE.insert(), job_postings)
    yield job_postings
    conn.execute(JOB_POSTING_TABLE.delete())

@contextmanager
def job_question(conn, job_questions=None):
    job_questions = job_questions or list(gen_job_question())

    conn.execute(JOB_QUESTION_TABLE.insert(), job_questions)
    yield job_questions
    conn.execute(JOB_QUESTION_TABLE.delete())
