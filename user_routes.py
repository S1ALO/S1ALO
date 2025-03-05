from flask import Flask, render_template, session, request, flash, redirect
from __main__ import app
import sqlite3
import hashlib
import routes

@app.route('/log-out')
def log_out():
    session.pop('user', None)
    return redirect('/')