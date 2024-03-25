from app import app
from flask import render_template

@app.route('/')
def hello_world():
    try:
        app.logger.info('Serving the Hello World page')
        return render_template('index.html')
    except Exception as e:
        app.logger.error('Error serving the Hello World page: %s', str(e), exc_info=True)