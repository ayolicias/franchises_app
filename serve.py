from flask import Flask, render_template, jsonify, url_for, flash, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json

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


@app.route('/provinces/add', methods=['POST'])
def provinces_insert():
    try:
        Province = Base.classes.provinces
        data = request.args.get('proname')
        rmks = request.args.get('prodesc')
        if len(data) == 0:
            # Check if no data was passed to the methods
            flash('Oops! No values were specified')
        else:
            count = db.session.query(Province).filter_by(Province.pro_name == data).first()
            if count == 0:
                # When all data has been specified save it into the database
                new_province = Province(pro_name=data, remarks=rmks)
                db.session.add(new_province)
                db.session.commit()
                flash('Done! Province saved successfully!')
            else:
                flash('Oops! Province record already exist')
    except Exception as ex:
        # Show Error when all criteria are not met
        flash('Error! Failed to record province info', str(ex))
    return render_template("provinces/entry.html")


@app.route("/provinces/delete", methods=['POST'])
def provinces_del():
    return "Provinces Delete"


@app.route("/provinces/all", methods=['GET'])
def provinces_all():
    Province = Base.classes.provinces
    data = db.session.query(Province).all()
    data = ramp(data)
    return jsonify({'data': data})

if __name__ == "__main__":
    app.run(debug=True)