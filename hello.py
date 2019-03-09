from flask import Flask, request, jsonify, abort, redirect, url_for, render_template

import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)

@app.route("/")
def hello():
    print('Hi!')
    return "Hello my very best friend!"

@app.route("/user/<username>")
def print_username_name(username):
    return 'user %s' % username**2

@app.route("/iris/<param>")
def iris(param):
    param = [float(p) for p in param.split(',')]
    clf = joblib.load('model.pkl')
    return str(clf.predict(np.array(param).reshape(1, -1)))

@app.route("/show_image")
def show_image():
    return '<img scr="/static/123.jpg" alt="setosa">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)


@app.route("/iris_post", methods=['POST'])
def iris_post():
    try:
        content = request.get_json()
        param = [float(p) for p in content['flower'].split(',')]
        clf = joblib.load('model.pkl')
        predict = clf.predict(np.array(param).reshape(1, -1))
        return jsonify(str(predict))
    except:
        return redirect(url_for('bad_request'))

from flask import send_file
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename
import pandas as pd

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name)
        f = form.file.data
        filename = secure_filename(form.name.data)
        # f.save(os.path.join(
        #     filename
        # ))
        df = pd.read_csv(f, header=0)
        clf = joblib.load('model.pkl')
        predict = pd.DataFrame(clf.predict(df))
        predict.to_csv(filename, index=False)
        return send_file(filename,
                         mimetype='text/csv',
                         attachment_filename=filename,
                         as_attachment=True)

    return render_template('submit.html', form=form)

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''