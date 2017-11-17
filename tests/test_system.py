# test_system.py
import pytest
import unittest
import requests
import requests
import json

import logging
import threading

import tornado.autoreload
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options


import src.aswwu.base_handlers as base
import src.aswwu.route_handlers.ask_anything as ask_anything
import src.aswwu.route_handlers.elections as elections
import src.aswwu.route_handlers.forms as forms
import src.aswwu.route_handlers.instagram as instagram
import src.aswwu.route_handlers.mask as mask
import src.aswwu.route_handlers.saml as saml
import src.aswwu.route_handlers.volunteers as volunteers
# import our super secret keys
from settings import keys

# import handlers as needed - here we import all of them

# define some initial options that can be passed in at run time
# e.g. `python server.py --port=8881` would run the server on port 8881
define("port", default=8888, help="run on the given port", type=int)
define("log_name", default="aswwu", help="name of the logfile")
define("current_year", default="1718")

# the main class that wraps everything up nice and neat
class Application(tornado.web.Application):
    def __init__(self):
        # define some global settings
        settings = {
            "login_url": "/login",
            "secret_key": keys["hmac"]
        }

        # list out the routes (as regex) and their corresponding handlers
        handlers = [
            (r"/login", base.BaseLoginHandler),
            (r"/profile/(.*)/(.*)", mask.ProfileHandler),
            (r"/profile_photo/(.*)/(.*)", mask.ProfilePhotoHandler),
            (r"/role/administrator", mask.AdministratorRoleHandler),
            (r"/role/volunteer", volunteers.VolunteerRoleHandler),
            (r"/search/all", mask.SearchAllHandler),
            (r"/search/(.*)/(.*)", mask.SearchHandler),
            (r"/update/(.*)", mask.ProfileUpdateHandler),
            (r"/volunteer", volunteers.VolunteerHandler),
            (r"/volunteer/(.*)", volunteers.VolunteerHandler),
            (r"/feed", instagram.FeedHandler),
            (r"/verify", base.BaseVerifyLoginHandler),
            (r"/", base.BaseIndexHandler),
            (r"/senate_election/showall", elections.AllElectionVoteHandler),
            (r"/senate_election/vote/(.*)", elections.ElectionVoteHandler),
            (r"/senate_election/livefeed", elections.ElectionLiveFeedHandler),
            (r"/saml/account/", saml.SamlHandler),
            (r"/matcher", mask.MatcherHandler),
            (r"/forms/job/new", forms.NewFormHandler),
            (r"/forms/job/view/(.*)", forms.ViewFormHandler),
            (r"/forms/job/delete", forms.DeleteFormHandler),
            (r"/forms/application/submit", forms.SubmitApplicationHandler),
            (r"/forms/application/view/(.*)/(.*)", forms.ViewApplicationHandler),
            (r"/forms/application/status", forms.ApplicationStatusHandler),
            (r"/forms/resume/upload", forms.ResumeUploadHandler),
            (r"/forms/resume/download/(.*)/(.*)", forms.ViewResumeHandler),
            (r"/askanything/add", ask_anything.AskAnythingAddHandler),
            (r"/askanything/view", ask_anything.AskAnythingViewAllHandler),
            (r"/askanything/view/rejected", ask_anything.AskAnythingRejectedHandler),
            (r"/askanything/(.*)/vote", ask_anything.AskAnythingVoteHandler),
            (r"/askanything/authorize", ask_anything.AskAnythingAuthorizeHandler),
            (r"/askanything/(.*)/authorize", ask_anything.AskAnythingAuthorizeHandler),
        ]

        # a bunch of setup stuff
        # mostly for logging and telling Tornado to start with the given settings
        self.options = options
        logger = logging.getLogger(options.log_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("src/aswwu/"+options.log_name+".log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("{'timestamp': %(asctime)s, 'loglevel' : %(levelname)s %(message)s }")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        tornado.web.Application.__init__(self, handlers, **settings)
        logger.info("Application started on port " + str(options.port))

def run_server():
    # create a new instance of our Application
    application = Application()
    application.listen(options.port)
    # tell it to autoreload if anything changes
    tornado.autoreload.start()
    io_loop.start()

def start_server():
    # pass in the conf default name
    conf_name = "default"

    # initiate the IO loop for Tornado
    global io_loop
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.options.parse_config_file("src/aswwu/"+conf_name+".conf")

    # create thread for running the server
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()

    # allow server to start before running tests
    import time
    time.sleep(1)
    print('starting services...')

def stop_server():
    print('stopping services...')
    io_loop.stop()

class test_system(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        start_server()
        print("setup_class()")

    @classmethod
    def teardown_class(cls):
        stop_server()
        print("teardown_class()")

    def test_root(self):
        expected_data = {
                "username": "ryan.rabello",
                "wwuid": "919428746",
                "roles": "",
                "photo": "profiles/1718/00958-2019687.jpg",
                "status": None,
                "full_name": "Ryan Rabello"
            }

        url = 'http://127.0.0.1:8888/'
        resp = requests.get(url)
        assert(resp.status_code == 200)
        assert(json.loads(resp.text) == expected_data)

    def test_search_all(self):
        expected_data = {
                "results": [
                        {"username": "john.doe", "photo": "profiles/1718/00958-2019687.jpg", "email": "", "full_name": "John Doe", "views": "6"},
                        {"username": "ryan.rabello", "photo": "profiles/1718/00958-2019687.jpg", "email": "ryan.rabello@wallawalla.edu", "full_name": "Ryan Rabello", "views": "9"},
                        {"username": "jane.anderson", "photo": "profiles/1718/00958-2019687.jpg", "email": "", "full_name": "Jane Anderson", "views": "8"},
                        {"username": "michael.scott", "photo": "None", "email": "None", "full_name": "Michael Scott", "views": "0"},
                        {"username": "mary.johnson", "photo": "profiles/1718/00958-2019687.jpg", "email": "", "full_name": "Mary Johnson", "views": "6"},
                        {"username": "susan.brown", "photo": "profiles/1718/00958-2019687.jpg", "email": "", "full_name": "Susan Brown", "views": "18"}
                ]
        };

        url = 'http://127.0.0.1:8888/search/all'
        resp = requests.get(url)
        assert(resp.status_code == 200)
        assert(json.loads(resp.text) == expected_data)