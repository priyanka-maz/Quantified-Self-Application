from flask import Flask, request, redirect, session
from flask import render_template
from flask import current_app as app
from flask.wrappers import Response
from flask_login import login_required
from flask_weasyprint import HTML, render_pdf
from io import StringIO
from datetime import datetime
import csv
from .database import db
from .models import *
from .email import *
from application.jobs import tasks
from flask_sse import sse
from main import cache


@app.route("/", methods=["GET"])
@cache.cached(timeout=5)
@login_required
def home():
    return render_template("index.html")


@app.route("/no_cache")
def no_cache():
    cache.clear()
    return redirect("/logout")


@app.route("/report", methods=["GET"])
@login_required
def report():
    user_fs_uniq = session["_user_id"]
    user = db.session.query(User).filter(
        User.fs_uniquifier == user_fs_uniq).first()
    email = user.email
    trackers = db.session.query(Tracker).filter(
        Tracker.user_id == user.id).all()
    timestamp = []
    for tracker in trackers:
        logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
        logs = sorted(logs, key=lambda k: k.timestamp, reverse=True)
        if len(logs) == 0:
            timestamp.append("Not reviewed yet.")
        else:
            timestamp.append(logs[0].timestamp)
    print(timestamp)
    report_html = render_template(
        "report.html", email=email, trackers=trackers, timestamp=timestamp)
    if (request.args.get("format") == "pdf"):
        report_pdf = render_pdf(HTML(string=report_html))
        send_email(email, "Quantified Self App: Progress Report",
                   "<a href=http://localhost:8080/report>Here</a> is your progress report.", "html")
        return report_pdf
    return report_html


@app.route("/export", methods=["GET"])
@login_required
def export_trackers():
    user_fs_uniq = session["_user_id"]
    user = db.session.query(User).filter(
        User.fs_uniquifier == user_fs_uniq).first()
    trackers = db.session.query(Tracker).filter(
        Tracker.user_id == user.id).all()
    csv_text = StringIO()
    csv_file = csv.writer(csv_text, dialect="excel")
    csv_file.writerow(["tracker_id", "tracker_name", "tracker_description", "tracker_type",
                      "mcq_choices", "log_id", "log_value", "log_timestamp", "log_note"])
    for tracker in trackers:
        logs = db.session.query(Log).filter(Log.tracker_id == tracker.id).all()
        for log in logs:
            csv_file.writerow([tracker.id, tracker.name, tracker.desc, tracker.type,
                              tracker.mcq, log.id, log.value, log.timestamp, log.note])
    return Response(csv_text.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=trackers.csv"})


@app.route("/import", methods=["POST"])
@login_required
def import_trackers():
    if request.method == "POST":
        upload = request.files["file"]
        if upload.filename:
            csv_content = upload.read()
            csv_text = str(csv_content, 'utf-8')
            csv_file = csv.DictReader(StringIO(csv_text), dialect="excel")

            user_fs_uniq = session["_user_id"]
            user = db.session.query(User).filter(
                User.fs_uniquifier == user_fs_uniq).first()
            for row in csv_file:
                tracker = db.session.query(Tracker).filter(
                    Tracker.id == int(row["tracker_id"])).first()
                if tracker:
                    pass
                if not tracker:
                    tracker = Tracker(
                        user_id=user.id, name=row["tracker_name"], desc=row["tracker_description"], type=row["tracker_type"], mcq=row["mcq_choices"])
                    db.session.add(tracker)
                    db.session.commit()
                log = db.session.query(Log).filter(
                    Log.id == int(row["log_id"])).first()
                if log:
                    import_timestamp = row["log_timestamp"]
                    if (import_timestamp != "" and datetime.strptime(import_timestamp, "%a, %d %b %Y %H:%M:%S %Z") >
                            datetime.strptime(log.timestamp,   "%a, %d %b %Y %H:%M:%S %Z")):
                        log.timestamp = import_timestamp
                        db.session.commit()
                if not log:
                    log = Log(
                        tracker_id=tracker.id, timestamp=row["log_timestamp"], value=row["log_value"], note=row["log_note"])
                    db.session.add(log)
                    db.session.commit()
        return redirect("/")
