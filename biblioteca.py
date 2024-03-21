from flask import Flask, render_template, request, flash, url_for, session, redirect, session
app = Flask(__name__)

@app.route('/')
def index ():
    return render_template ('index.html')
app.run(host='0.0.0.0', port=81, debug=True)