#!/usr/bin/python3
""" Starts a Flask web application. """

from flask import Flask, render_template
from models import storage
from models.state import State

# creates an instance of the Flask class and assigns it to the variable app
app = Flask(__name__)


# Teardown app context to remove the
#   current SQLAlchemy session after each request
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


# Define the route for '/cities_by_states'
@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all states and related cities.

    States/cities are sorted by name.
    """
    # Fetch all State objects from the DBStorage
    states = storage.all(State)

    # Render the template and pass the list of states to the template
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
