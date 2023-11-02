# !/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return ''

class Campers(Resource):

    def get(self):
        campers = [camper.to_dict(rules=('-signups', '-activities'))
                      for camper in Camper.query.all()]

        return make_response(campers, 200)

    def post(self):

        fields = request.get_json()
        try:
            camper = Camper(
                name=fields['name'],
                age=fields['age']
            )
            db.session.add(camper)
            db.session.commit()
            return make_response(camper.to_dict(rules=('-signups',)), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
api.add_resource(Campers, "/campers")


class CamperById(Resource):

    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).one_or_none()

        if camper is None:
            return make_response({'error': 'Camper not found'}, 404)

        return make_response(camper.to_dict(), 200)

    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).one_or_none()

        if camper is None:
            return make_response({'error': 'Camper not found'}, 404)

        fields = request.get_json()

        try:
            for field in fields:
                setattr(camper, field, fields[field])
            db.session.add(camper)
            db.session.commit()

            return make_response(camper.to_dict(rules=('-activities', '-signups')), 202)

        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)


api.add_resource(CamperById, "/campers/<int:id>")


class Activities(Resource):

    def get(self):
        activities = [activity.to_dict(rules=('-signups', '-campers',))
                   for activity in Activity.query.all()]

        return make_response(activities, 200)


api.add_resource(Activities, "/activities")


class ActivityById(Resource):

    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).one_or_none()

        if activity is None:
            return make_response({'error': 'Activity not found'}, 404)

        db.session.delete(activity)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(ActivityById, "/activities/<int:id>")


class Signups(Resource):
    def post(self):

        fields = request.get_json()
        try:
            signup = Signup(
                time=fields['time'],
                camper_id=fields['camper_id'],
                activity_id=fields['activity_id'])
            db.session.add(signup)
            db.session.commit()
            return make_response(signup.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(Signups, "/signups")

    

if __name__ == '__main__':
    app.run(port=5555, debug=True)






























# #!/usr/bin/env python3

# from models import db, Activity, Camper, Signup
# from flask_restful import Api, Resource
# from flask_migrate import Migrate
# from flask import Flask, make_response, jsonify, request
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)
# api = Api(app)

# @app.route('/')
# def home():
#     return ''


# class Campers(Resource):

#     def get(self):
#         campers = [camper.to_dict(rules=('-signups', '-activities',))
#                       for camper in Camper.query.all()]

#         return make_response(campers, 200)

#     def post(self):

#         fields = request.get_json()
#         try:
#             camper = Camper(
#                 name=fields['name'],
#                 age=fields['age']
#             )
#             db.session.add(camper)
#             db.session.commit()
#             return make_response(camper.to_dict(rules=('-signups',)), 201)
#         except ValueError:
#             return make_response({"errors": ["validation errors"]}, 400)


# api.add_resource(Campers, "/campers")


# class CamperById(Resource):

#     def get(self, id):
#         camper = Camper.query.filter(Camper.id == id).one_or_none()

#         if camper is None:
#             return make_response({'error': 'Camper not found'}, 404)

#         return make_response(camper.to_dict(), 200)

#     def patch(self, id):
#         camper = Camper.query.filter(Camper.id == id).one_or_none()

#         if camper is None:
#             return make_response({'error': 'Camper not found'}, 404)

#         fields = request.get_json()

#         try:
#             for field in fields:
#                 setattr(camper, field, fields[field])
#             db.session.add(camper)
#             db.session.commit()

#             return make_response(camper.to_dict(rules=('-activities', '-signups')), 202)

#         except ValueError:
#             return make_response({"errors": ["validation errors"]}, 400)



# api.add_resource(CamperById, "/campers/<int:id>")



# class Activities(Resource):

#     def get(self):
#         activities = [activity.to_dict(rules=('-signups', '-campers',))
#                       for activity in Activity.query.all()]

#         return make_response(activities, 200)

# api.add_resource(Activities, "/activities")



# class ActivityById(Resource):

#     def delete(self, id):
#         activity = Activity.query.filter(Activity.id == id).one_or_none()

#         if activity is None:
#             return make_response({'error': 'Activity not found'}, 404)

#         db.session.delete(activity)
#         db.session.commit()
#         return make_response({}, 204)


# api.add_resource(ActivityById, "/activities/<int:id>")

# class Signups(Resource):
#     def post(self):

#         fields = request.json
#         print(fields)
#         try:
#             signup = Signup(
#                 time=fields['time'],
#                 camper_id=fields['camper_id'],
#                 activity_id=fields['activity_id'])
            
#             db.session.add(signup)
#             db.session.commit()
            
#             return make_response(signup.to_dict(), 201)
#         except ValueError:
#             return make_response({"errors": ["validation errors"]}, 400)


# api.add_resource(Signups, "/signups")



# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
