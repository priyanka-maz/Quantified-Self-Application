import time
from application.jobs.workers import celery
from datetime import datetime
from flask import current_app as app
from flask_sse import sse
from celery.schedules import crontab
from application.controllers import *
from application.email  import *
from application.database import db


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=00, hour=10),
        daily_reminder.s(),
    )

    sender.add_periodic_task(
        crontab(minute=30, hour=10, day_of_month=1),
        monthly_report.s(),
    )


@celery.task
def daily_reminder():
    users = db.session.query(User).all()
    for user in users:
        print("Sending email to ", user.email)
        send_email(user.email, "Quantified Self App: Daily Reminder",
                   "<a href=http://localhost:8080/>Here</a> is where you should go right now.", "html")


@celery.task
def monthly_report():
    users = db.session.query(User).all()
    for user in users:
        email = user.email
        trackers = db.session.query(Tracker).filter(
            Tracker.user_id == user.id).all()
        timestamp = []
        for tracker in trackers:
            logs = db.session.query(Log).filter(
                Log.tracker_id == tracker.id).all()
            logs = sorted(logs, key=lambda k: k.timestamp, reverse=True)
            if len(logs) == 0:
                timestamp.append("Not reviewed yet.")
            else:
                timestamp.append(logs[0].timestamp)
        print(timestamp)
        report_html = render_template(
            "report.html", email=email, trackers=trackers, timestamp=timestamp)
        print("Sending email to ", user.email)
        send_email(user.email, "Quantified Self App: Monthly Report",
                   report_html, "html")
