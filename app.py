from flask import Flask, session, render_template, request, flash, redirect
# from db_connector import database

# db = database()

app = Flask(__name__)
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
app.secret_key = "secretKey"

import routes, user_routes

if __name__ == '__main__':
    app.run(debug=True)