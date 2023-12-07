# Runs the development version of the server
rm "library.db"
export FLASK_CONFIG="development"
flask run --port=5001
