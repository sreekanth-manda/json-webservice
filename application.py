from flask import Flask, jsonify, abort, make_response, request
import logging
from endpoints.nine import webservice

application = Flask(__name__)
application.register_blueprint(webservice)
application.debug = True


if __name__ == '__main__':
	application.run()
