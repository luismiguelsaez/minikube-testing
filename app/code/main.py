from flask import Flask
from flask_restful import Resource, Api
from os import environ
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class Message(Resource):
    def get(self):

        containerName = environ['HOSTNAME']
        timestamp = datetime.now()

        if 'APPNAME' in environ.keys():
            appName = environ['APPNAME']
        else:
            appName = "default"
        
        return "Hello World, I'm application " + appName + " and my container is: " + containerName + " " + str(timestamp)

api.add_resource(Message, '/')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5000')
