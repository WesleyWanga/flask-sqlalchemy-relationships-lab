#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

try:
    from models import db, Event, Session, Speaker, Bio
except ModuleNotFoundError:
    from server.models import db, Event, Session, Speaker, Bio


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


# ---------------------------------------------------------
# EVENT ENDPOINTS
# ---------------------------------------------------------

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]), 200


@app.route("/events/<int:id>/sessions", methods=["GET"])
def get_event_sessions(id):
    event = db.session.get(Event, id)

    if event is None:
        return jsonify({
            "error": "Event not found"
        }), 404

    return jsonify([
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        }
        for session in event.sessions
    ]), 200


# ---------------------------------------------------------
# SPEAKER ENDPOINTS
# ---------------------------------------------------------

@app.route("/speakers", methods=["GET"])
def get_speakers():
    speakers = Speaker.query.all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]), 200


@app.route("/speakers/<int:id>", methods=["GET"])
def get_speaker(id):
    speaker = db.session.get(Speaker, id)

    if speaker is None:
        return jsonify({
            "error": "Speaker not found"
        }), 404

    if speaker.bio is not None:
        bio_text = speaker.bio.bio_text
    else:
        bio_text = "No bio available"

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }), 200


# ---------------------------------------------------------
# SESSION ENDPOINTS
# ---------------------------------------------------------

@app.route("/sessions/<int:id>/speakers", methods=["GET"])
def get_session_speakers(id):
    session = db.session.get(Session, id)

    if session is None:
        return jsonify({
            "error": "Session not found"
        }), 404

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": (
                speaker.bio.bio_text
                if speaker.bio is not None
                else "No bio available"
            )
        }
        for speaker in session.speakers
    ]), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    