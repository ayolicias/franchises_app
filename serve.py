from flask import Flask, render_template, jsonify, url_for, flash, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
import imghdr
import smtplib

# mail_from = 'origin@mail.com'
# mail_to = ['supportagent1@credit-rescue.co.za', 'supportagent1@credit-rescue.co.za']
# mail_subject = 'Hello'
# mail_message_body = 'Hello World!'

# mail_to_string = ', '.join(mail_to)

# mail_message = f'''
# From: {mail_from}
# To: {mail_to_string}
# Subject: {mail_subject}

# {mail_message_body}
# '''

# server = smtplib.SMTP('localhost')
# server.sendmail(mail_from, mail_to, mail_subject, mail_message)
# server.quit()

# def convertToBinaryData(attachments):
#     # Convert digital data to binary format
#     with open(attachments, 'rb') as file:
#         binaryData = file.read()
#     return binaryData
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
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

@app.route("/", methods=['GET'])
def index():
    return render_template("dashboard/index.html")

# def write_file(franchise_id, filename):
#     # Convert binary data to proper format and write it on Hard Disk
#     with open(filename, 'wb', encoding="utf8", errors='ignore') as file:
 
    # cursor = connection.cursor()
    #     sql_fetch_blob_query = """SELECT * from attachments where id = %s"""

        # cursor.execute(sql_fetch_blob_query, (emp_id,))
        # record = cursor.fetchall()
        # for row in record:
        #     print("Id = ", row[0], )
        #     print("file = ", row[1])
        #     image = row[2]
        #     file = row[3]
        #     print("Storing employee image and bio-data on disk \n")
        #     write_file(image, photo)
        #     write_file(file, bioData)

    # except mysql.connector.Error as error:
    #     print("Failed to read BLOB data from MySQL table {}".format(error))

@app.route("/dashboard/metrics", methods=['GET'])
def dashboard_metric():
    #Province = Base.classes.provinces
    Province = db.Table("provinces", db.metadata, autoload=True, autoload_with=db.engine)
    data = db.session.query(Province).all()
    return jsonify({'raw': data})

@app.route("/franchises", methods=['GET'])
def franchises_index():
    return render_template("franchises/home.html")

@app.route("/attachments", methods=['GET'])
def attachments_index():
    return render_template("attachments/home.html")

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


@app.route('/provinces/add', methods=['POST'])
def provinces_insert():
    try:
        Province = Base.classes.provinces
        data = request.args.get('pro_name')
        # rmks = request.args.get('prodesc')
        if len(data) == 0:
            # Check if no data was passed to the methods
            flash('Oops! No values were specified')
        else:
            count = db.session.query(Province).filter_by(Province.pro_name == data).first()
            if count == 0:
                # When all data has been specified save it into the database
                new_province = Province(pro_name=data)
                db.session.add(new_province)
                db.session.commit()
                flash('Done! Province saved successfully!')
            else:
                flash('Oops! Province record already exist')
    except Exception as ex:
        # Show Error when all criteria are not met
        flash('Error! Failed to record province info', str(ex))
    return render_template("provinces/")

@app.route("/provinces/delete", methods=['POST'])
def provinces_del():
    return "Provinces Delete"

@app.route("/franchises/add", methods=['POST'])
def provinces_edit():
    return "Province Edit"

@app.route("/attachments/index", methods=['POST'])
def attachments_all():
    return "attachments home"

@app.route("/provinces/all", methods=['GET'])
def provinces_all():
    table_reflection = db.Table("provinces", db.metadata, autoload=True, autoload_with=db.engine)
    attrs = {"__table__": table_reflection}
    Provinces = type("table_name", (db.Model,), attrs)
    c = Provinces.query.all()
    raw = limp(c)
    return json.dumps(raw)

#!/usr/bin/env python3

"""Send the contents of a directory as a MIME message."""

import os
import smtplib
# For guessing MIME type based on file name extension
import mimetypes

from argparse import ArgumentParser

from email.message import EmailMessage
from email.policy import SMTP


def main():
    parser = ArgumentParser(description="""\
Send the contents of a directory as a MIME message.
Unless the -o option is given, the email is sent by forwarding to your local
SMTP server, which then does the normal delivery process.  Your local machine
must be running an SMTP server.
""")
    parser.add_argument('-d', '--directory',
                        help="""Mail the contents of the specified directory,
                        otherwise use the current directory.  Only the regular
                        files in the directory are sent, and we don't recurse to
                        subdirectories.""")
    parser.add_argument('-o', '--output',
                        metavar='FILE',
                        help="""Print the composed message to FILE instead of
                        sending the message to the SMTP server.""")
    parser.add_argument('-s', '--sender', required=True,
                        help='The value of the From: header (required)')
    parser.add_argument('-r', '--recipient', required=True,
                        action='append', metavar='RECIPIENT',
                        default=[], dest='recipients',
                        help='A To: header value (at least one required)')
    args = parser.parse_args()
    directory = args.directory
    if not directory:
        directory = '.'
    # Create the message
    msg = EmailMessage()
    msg['Subject'] = f'Contents of directory {os.path.abspath(directory)}'
    msg['To'] = ', '.join(args.recipients)
    msg['From'] = args.sender
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
    # Now send or store the message
    if args.output:
        with open(args.output, 'wb') as fp:
            fp.write(msg.as_bytes(policy=SMTP))
    else:
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)