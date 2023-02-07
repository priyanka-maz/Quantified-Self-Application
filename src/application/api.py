from flask import session, request
from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from flask_security.decorators import auth_required
import secrets, bcrypt

from .database import db
from .models import *
from .validation import *
from .plot import *

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("email")
create_user_parser.add_argument("password")

tracker_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "name": fields.String,
    "desc": fields.String,
    "type": fields.String,
    "mcq": fields.String,
    "timestamp": fields.String,
    "bstr": fields.String
}

create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument("user_id")
create_tracker_parser.add_argument("name")
create_tracker_parser.add_argument("desc")
create_tracker_parser.add_argument("type")
create_tracker_parser.add_argument("mcq")

change_tracker_parser = reqparse.RequestParser()
change_tracker_parser.add_argument("name")
change_tracker_parser.add_argument("desc")

log_fields = {
    "id": fields.Integer,
    "tracker_id": fields.Integer,
    "timestamp": fields.String,
    "value": fields.String,
    "note": fields.String
}

create_log_parser = reqparse.RequestParser()
create_log_parser.add_argument("tracker_id")
create_log_parser.add_argument("timestamp")
create_log_parser.add_argument("value")
create_log_parser.add_argument("note")

change_log_parser = reqparse.RequestParser()
change_log_parser.add_argument("timestamp")
change_log_parser.add_argument("value")
change_log_parser.add_argument("note")

class UserAPI(Resource):
    @auth_required("session", "token")
    @marshal_with(user_fields)
    def get(self):
        user_fs_uniq = session["_user_id"]
        user = db.session.query(User).filter(User.fs_uniquifier == user_fs_uniq).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(user_fields)
    def delete(self):
        user_fs_uniq = session["_user_id"]
        user = db.session.query(User).filter(User.fs_uniquifier == user_fs_uniq).first()
        if user:
            trackers = db.session.query(Tracker).filter(Tracker.user_id == user.id).all()
            for tracker in trackers:
                logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
                for log in logs:
                    db.session.delete(log)
                db.session.delete(tracker)
            db.session.delete(user)
            db.session.commit()
            return "", 200
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(user_fields)
    def post(self):
        args = create_user_parser.parse_args()
        email: str = args.get("email", None)
        password: str = args.get("password", None)
        if not email:
            raise BusinessValidationError(400, "ERB", "Empty request body.")
        else:
            user = db.session.query(User).filter(User.email == email).first()
            if user:
                return "", 409
            else:
                user = User(email=email, password=password, fs_uniquifier=secrets.token_hex(16), active=0)
                #password=bcrypt.hashpw(password.encode('utf-8'), bytes("16e29a5d1e2662833e87cceb242c0e8c").encode('utf-8'))
                db.session.add(user)
                db.session.commit()
                return user

class TrackerAPI(Resource):
    @auth_required("session", "token")
    @marshal_with(tracker_fields)
    def get(self):
        user_fs_uniq = session["_user_id"]
        user = db.session.query(User).filter(User.fs_uniquifier == user_fs_uniq).first()
        tracker_id = request.args.get("tracker_id")
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
        if tracker and tracker_id:
            logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()

            if tracker.type == 'num':
                tracker.bstr = plot_numTracker(tracker_id, logs)
                db.session.commit()
            if tracker.type == 'bool':
                tracker.bstr = plot_boolTracker(tracker_id, logs)
                db.session.commit()
            if tracker.type == 'mcq':
                tracker.bstr = plot_mcqTracker(tracker_id, logs, tracker.mcq)
                db.session.commit()
            if tracker.type == 'time':
                tracker.bstr = plot_timeTracker(tracker_id, logs)
                db.session.commit()
            return tracker
        elif not(tracker) and tracker_id:
        	raise NotFoundError(status_code=404)
        else:
            if user:
                trackers = db.session.query(Tracker).filter(Tracker.user_id == user.id).all()
                for tracker in trackers:
                    logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
                    logs = sorted(logs, key=lambda k: k.timestamp, reverse=True)
                    if len(logs) == 0:
                    	tracker.timestamp = "Not reviewed yet."
                    else:
                    	tracker.timestamp = logs[0].timestamp
                return trackers
            else:
                raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(tracker_fields)
    def put(self):
        tracker_id = request.args.get("tracker_id")
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
        if tracker:
            args = change_tracker_parser.parse_args()
            name: str = args.get("name", None)
            desc: str = args.get("desc", None)
            if not (desc or name or desc ==""):
                raise BusinessValidationError(400, "ERB", "Empty request body.")
            else:
                if name:
                    tracker.name = name
                if desc or desc == "":
                    tracker.desc = desc
                db.session.commit()
                return tracker
        else:
            raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(tracker_fields)
    def delete(self):
        tracker_id = request.args.get("tracker_id")
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
        if tracker:
            logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
            for log in logs:
                db.session.delete(log)
            db.session.delete(tracker)
            db.session.commit()
            return tracker
        else:
            raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(tracker_fields)
    def post(self):
        args = create_tracker_parser.parse_args()
        user_fs_uniq = session["_user_id"]
        user = db.session.query(User).filter(User.fs_uniquifier == user_fs_uniq).first()
        user_id = user.id;
        name: str = args.get("name", None)
        desc: str = args.get("desc", None)
        type: str = args.get("type", None)
        mcq: str = args.get("mcq", None)
        if not (user_id and name and desc and type):
            raise BusinessValidationError(400, "ERB", "Empty request body.")
        else:
            try:
                user_id = int(user_id)
            except TypeError:
                raise BusinessValidationError(400, "TE", "Type Error.")
            tracker = Tracker(user_id=user_id, name=name, desc=desc, type=type, mcq=mcq)
            db.session.add(tracker)
            db.session.commit()
            return tracker

class LogAPI(Resource):
    @auth_required("session", "token")
    @marshal_with(log_fields)
    def get(self):
        tracker_id = request.args.get("tracker_id")
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
        log_id = request.args.get("log_id")
        log = db.session.query(Log).filter(Log.id == log_id).first()
        if log and log_id:
            return log
        elif not (log) and log_id:
            raise NotFoundError(status_code=404)
        else:
            if tracker:
                logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
                logs = sorted(logs, key=lambda k: k.value, reverse=True)
                return logs
            else:
                raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(log_fields)
    def put(self):
        log_id = request.args.get("log_id")
        log = db.session.query(Log).filter(Log.id == log_id).first()
        if log:
            args = change_log_parser.parse_args()
            timestamp: str = args.get("timestamp", None)
            value: str = args.get("value", None)
            note: str = args.get("note", None)
            if not (timestamp or value or note or note==""):
                raise BusinessValidationError(400, "ERB", "Empty request body.")
            else:
                if timestamp:
                    log.timestamp = timestamp
                if value:
                    log.value = value
                if note or note=="":
                    log.note = note
                db.session.commit()
                return log
        else:
            raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(log_fields)
    def delete(self):
        log_id = request.args.get("log_id")
        log = db.session.query(Log).filter(Log.id == log_id).first()
        if log:
            db.session.delete(log)
            db.session.commit()
            return log
        else:
            raise NotFoundError(status_code=404)

    @auth_required("session", "token")
    @marshal_with(log_fields)
    def post(self):
        args = create_log_parser.parse_args()
        tracker_id: int = args.get("tracker_id", None)
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
        value: str = args.get("value", None)
        note: str = args.get("note", None)
        timestamp: str = args.get("timestamp", None)
        if not(tracker_id and value and note):
            raise BusinessValidationError(400, "ERB", "Empty request body.")
        elif tracker.mcq and (value not in tracker.mcq):
            raise BusinessValidationError(400, "TE", "Type Error.")
        else:
            try:
                tracker_id = int(tracker_id)
            except TypeError:
                raise BusinessValidationError(400, "TE", "Type Error.")
            log = Log(tracker_id=tracker_id, value=value, note=note, timestamp=timestamp)
            db.session.add(log)
            db.session.commit()
            return log
