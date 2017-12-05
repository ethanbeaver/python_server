import requests
import json
from tests.utils import job_posting, job_question, job_application, job_answer


def test_view_job(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None):
        expected_data = {"form": {"department": None, "job_description": "Doesn't Really Matter", "questions": [{"question": "First Name", "id": 1}, {"question": "Last Name", "id": 2}, {"question": "WWU ID#", "id": 3}, {"question": "Phone Number", "id": 4}, {"question": "E-mail", "id": 5}, {"question": "On-Campus Address", "id": 6}, {"question": "High-School Attended", "id": 7}, {"question": "Current SM/ ACA?", "id": 10}, {"question": "If so, where?", "id": 11}, {"question": "On average, how many credits will you be taking?", "id": 12}, {"question": "How many hours do you hope to work?", "id": 13}, {"question": "Have you worked for ASWWU before? If so, what job?", "id": 14}, {"question": "What other jobs or responsibilities will require your attention/ time?", "id": 15}, {"question": "Why do you want to work for ASWWU?", "id": 16}, {"question": "If there was one thing you could change about ASWWU, what would it be?", "id": 17}], "owner": "ryan.rabello", "image": "", "job_name": "ASWWU Generic", "visibility": False, "jobID": 1}}

        url = "http://127.0.0.1:8888/forms/job/view/1"
        resp = requests.get(url)
        assert (resp.status_code == 200)
        assert (json.loads(resp.text) == expected_data)


def test_view_all_jobs(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None):
        expected_data = {"image": "", "visibility": False, "jobID": 1, "job_description": "Doesn't Really Matter", "department": None, "job_name": "ASWWU Generic"}

        url = "http://127.0.0.1:8888/forms/job/view/all"
        resp = requests.get(url)
        assert resp.status_code == 200
        assert (json.loads(resp.text)['forms'][0] == expected_data)
        assert(len(json.loads(resp.text)['forms']) > 5)


def test_view_all_applications(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None), job_application(jobsdb_conn, None), job_answer(jobsdb_conn, None):
        url = "http://127.0.0.1:8888/forms/job/all/all"
        resp = requests.get(url)
        assert (resp.status_code == 200)
        assert (json.loads(resp.text).length > 1)


def test_view_application_one_job(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None), job_application(jobsdb_conn, None), job_answer(jobsdb_conn, None):
        url = "http://127.0.0.1:8888/forms/job/1/all"
        resp = requests.get(url)
        assert (resp.status_code == 200)
        assert (json.loads(resp.text).length > 1)


def test_view_application_one_user(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None), job_application(jobsdb_conn, None), job_answer(jobsdb_conn, None):
        url = "http://127.0.0.1:8888/forms/job/all/1"
        resp = requests.get(url)
        assert (resp.status_code == 200)
        assert (json.loads(resp.text).length > 1)


def test_view_individual_application(testing_server, jobsdb_conn):
    with job_posting(jobsdb_conn, None), job_question(jobsdb_conn, None), job_application(jobsdb_conn, None), job_answer(jobsdb_conn, None):
        url = "http://127.0.0.1:8888/forms/job/1/1"
        resp = requests.get(url)
        assert (resp.status_code == 200)
        assert (json.loads(resp.text).length > 1)
