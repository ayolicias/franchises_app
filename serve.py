from flask import Flask, render_template, jsonify, url_for, flash, requests, redirect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
import imghdr
import smtplib
import os.path
import requests
import sqlite3
import posixpath
import django_heroku

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
app = Flask(__name__)
app.secret_key = '99d0*93/>-23@#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:demo@localhost/franchises'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)
  

def as_dict(row):
    data = vars(row)
    del data['_sa_instance_state']
    return data

def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()

    return binary

def ramp(row):
    raw = None
    if len(row) == 1:
        raw = vars(row[0])
    else:
        print(row)
        raw = vars(row)
    data = raw
    del data['_sa_instance_state']
    return data

def limp(row):
    raw = None
    bulk = list()
    if len(row) == 1:
        raw = vars(row[0])
    else:
        for itm in row:
            raw = vars(itm)
            data = raw
            del data['_sa_instance_state']
            bulk.append(raw)
    return bulk

def sqlite_connect(franchises):

    try:
        # Create a connection
        conn = sqlite3.connect(franchises)
    except sqlite3.Error:
        print(f"Error connecting to the database '{franchises}'")
    finally:
        return conn

def insert_file(entry, franchises):
    try:
        # Establish a connection
        connection = sqlite_connect(franchises)
        print(f"Connected to the database `{franchises}`")

        # Create a cursor object
        cursor = connection.cursor()

        sqlite_insert_blob_query = f"""
        INSERT INTO {attachments} (upload_id, id) VALUES (pdf, 1)
        """

        # Convert the file into binary
        binary_file = convert_into_binary(entry)
        data_tuple = (entry, binary_file)

        # Execute the query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        connection.commit()
        print('File inserted successfully')
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob into the table", error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

def write_to_file(binary_code, attachments):
    # Convert binary to a proper file and store in memory
    with open(attachments, 'wb') as file:
        file.write(binary_code)
    print(f'Created file with name: {attachments}')

def retrieve_file(upload, franchises, attachments):
    try:
        # Establish a connection
        connection = sqlite_connect(franchises)
        print(f"Connected to the database `{franchises}`")

        # Create a cursor object
        cursor = connection.cursor()

        sql_retrieve_file_query = f"""SELECT * FROM {attachments} WHERE name = file_id, id"""
        cursor.execute(sql_retrieve_file_query, (franchises/entry))

        # Retrieve results in a tuple
        record = cursor.fetchone()
        # Save to a file
        write_to_file(record[1], record[0])
    except sqlite3.Error as error:
        print("Failed to insert blob into the table", error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

@app.route("/", methods=['GET'])
def index():
    return render_template("dashboard/index.html")

@app.route("/dashboard/metrics", methods=['GET'])
def dashboard_metric():
    #Province = Base.classes.provinces
    Province = db.Table("provinces", db.metadata, autoload=True, autoload_with=db.engine)
    data = db.session.query(Province).all()
    return jsonify({'raw': data})

@app.route("/franchises", methods=['GET'])
def franchises_index():
    return render_template("franchises/home.html")

@app.route("/franchises/entry", methods=['GET'])
def franchises_add():
    return render_template("franchises/entry.html")

@app.route("/franchises/delete", methods=['POST'])
def franchises_del():
    return "Franchise Delete"

@app.route("/franchises/add", methods=['POST'])
def franchises_edit():
    return "Franchises Edit"

@app.route("/franchises/all", methods=['GET'])
def franchises_all():
    table_reflection = db.Table("franchises", db.metadata, autoload=True, autoload_with=db.engine)
    attrs = {"__table__": table_reflection}
    Franchises = type("table_name", (db.Model,), attrs)
    c = Franchises.query.all()
    raw = limp(c)
    return json.dumps(raw)

@app.route("/provinces", methods=['GET'])
def provinces_index():
    return render_template("provinces/home.html")

@app.route("/provinces/entry", methods=['GET'])
def provinces_add():
    return render_template("provinces/entry.html")

@app.route("/provinces/delete", methods=['POST'])
def provinces_del():
    return "Provinces Delete"

@app.route("/franchises/add", methods=['POST'])
def provinces_edit():
    return "Province Edit"

# @app.route('/franchises/entry', methods=['GET', 'POST'])
# def franchises_entry():
#     if request.method == 'POST' and 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         rec = Photo(filename=filename, user=g.user.id)
#         rec.store()
#         flash("Photo saved.")
#         return redirect(url_for('show', id=rec.id))
#     return render_template('/franchises/entry.html')

# @app.route('/franchises/entry<id>')
# def entry(id):
#     photo = Photo.load(id)
#     if photo is None:
#         abort(404)
#     url = photos.url(photo.filename)
#     return render_template('/franchises/entry.html', url=url, photo=photo)

    # media = UploadSet('media', default_dest=lambda app: app.instance_root)
    # configure_uploads(app, (photos, media))
    # patch_request_class(app)        
    # patch_request_class(app, 32 * 1024 * 1024)

    def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
 
@app.route("/provinces/all", methods=['GET'])
def provinces_all():
    table_reflection = db.Table("provinces", db.metadata, autoload=True, autoload_with=db.engine)
    attrs = {"__table__": table_reflection}
    Provinces = type("table_name", (db.Model,), attrs)
    c = Provinces.query.all()
    raw = limp(c)
    return json.dumps(raw)

@app.route("/upload_files/all", methods=['GET'])
def upload_files_all():
    table_reflection = db.Table("upload_files", db.metadata, autoload=True, autoload_with=db.engine)
    attrs = {"__table__": table_reflection}
    Provinces = type("table_name", (db.Model,), attrs)
    c = Upload_files.query.all()
    raw = limp(c)
    return json.dumps(raw)
    
django_heroku.settings(locals())

if __name__ == "__main__":
    app.run(debug=True)