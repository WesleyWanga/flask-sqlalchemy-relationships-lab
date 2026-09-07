# EventWise Flask-SQLAlchemy Relationships API

## Project Description

EventWise is a Flask backend application that demonstrates relational database modeling using Flask-SQLAlchemy.

The application models events, sessions, speakers, and speaker bios. It demonstrates one-to-many, one-to-one, and many-to-many relationships.

## Relationships

- An Event has many Sessions.
- A Session belongs to an Event.
- A Speaker has one Bio.
- A Bio belongs to a Speaker.
- A Session has many Speakers through the `session_speakers` association table.
- A Speaker has many Sessions through the `session_speakers` association table.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Pytest
- Pipenv

## Installation

Clone the repository and enter the project directory:

```bash
cd workout-api