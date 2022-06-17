from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)
load_dotenv()

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "development.db" if os.environ.get("FLASK_ENV") == "development" else "database.db"
print(DATABASE_FILE)
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':

        defaultData = requests.get("https://rhul.buggyrace.net/specs/data/defaults.json")
        defaultCost = json.loads(defaultData.text)

        typesData = requests.get("https://rhul.buggyrace.net/specs/data/types.json")
        typesCost = json.loads(typesData.text)

        return render_template("buggy-form.html", defaultData=defaultCost, typesData=typesCost)
    elif request.method == 'POST':
        msg=""
        data = json.loads(request.data)
        #-----------------------
        # SERVER SIDE VALIDATION
        if data['qty_wheels'].strip().isdigit() == False or data['qty_wheels'] < data['qty_tyres']:
            return render_template("updated.html", msg = "Invalid input")
        #-----------------------

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                print(data)
                print(data["qty_wheels"])
                #cur.execute(
                 #   "INSERT INTO buggies (id, qty_wheels, flag_color, flag_color_secondary, flag_pattern, algo, antibiotic, armour, attack, aux_power_type, aux_power_units, banging, fireproof, hamster_booster, insulated, power_type, power_units, qty_attacks, qty_tyres, tyres, total_cost) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  #  (2,data['qty_wheels'], data['flag_color'], data['flag_color_secondary'], data['flag_pattern'], data['algo'], data['antibiotic'], data['armour'], data['attack'], data['aux_power_type'], data['aux_power_units'], data['banging'], data["fireproof"], data["hamster_booster"], data["insulated"], data["power_type"], data["power_unites"], data["qty_attacks"], data["qty_tyres"], data["tyres"], data["total_cost"])
                #)

                cur.execute(
                    f"INSERT INTO buggies (id, qty_wheels, flag_color, flag_color_secondary, flag_pattern, algo, antibiotic, armour, attack, aux_power_type, aux_power_units, banging, fireproof, hamster_booster, insulated, power_type, power_units, qty_attacks, qty_tyres, tyres, total_cost) VALUES (3,{int(data['qty_wheels'])},'{data['flag_color']}','{data['flag_color_secondary']}','{data['flag_pattern']}','{data['algo']}','{data['antibiotic']}','{data['armour']}','{data['attack']}','{data['aux_power_type']}',{int(data['aux_power_units'])},'{data['banging']}','{data['fireproof']}',{int(data['hamster_booster'])},'{ data['insulated']}','{data['power_type']}',{int(data['power_units'])},{int(data['qty_attacks'])},{int(data['qty_tyres'])},'{data['tyres']}',0)"
                )
                #, (2,4,'white','black','plain','steady','no','none','none','none',0,'no','no',0,'no','petrol',1,0,4,'knobbly',0)
                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():

    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()

    fetchDelete = request.args.get("delete")
    print(fetchDelete)
    if fetchDelete:
        print("Here")
        cur.execute("DELETE FROM buggies WHERE id=?", (fetchDelete))
        con.commit()

    cur.execute("SELECT * FROM buggies")
    record = cur.fetchall();

    allData = []
    for buggies in record:
        desc = list(zip(*cur.description))[0]
        data = dict(zip(desc,buggies))
        allData.append(data)

    fetchId = request.args.get("id")
    buggyId = fetchId if fetchId else ""
    return render_template("buggy.html", buggy=allData, buggyId=buggyId)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();

        defaultData = requests.get("https://rhul.buggyrace.net/specs/data/defaults.json")
        defaultCost = json.loads(defaultData.text)

        typesData = requests.get("https://rhul.buggyrace.net/specs/data/types.json")
        typesCost = json.loads(typesData.text)
    elif request.method == "POST":
        cur.execute(
            "UPDATE buggies set qty_wheels=? flag_color=? flag_color_secondary=? flag_pattern=? algo=? antibiotic=? armour=? attack=? aux_power_type=? aux_power_units=? banging=? fireproof=? hamster_booster=? insulated=? power_type=? power_units=? qty_attacks=? qty_tyres=? tyres=? total_cost=? WHERE id=?",
            (request.form['qty_wheels'], request.form['flag_color'], request.form['flag_color_secondary'], request.form['flag_pattern'], request.form['algo'], request.form['antibiotic'], request.form['armour'], request.form['attack'], request.form['aux_power_type'], request.form['aux_power_units'], request.form['banging'], request.form["fireproof"], request.form["hamster_booster"], request.form["insulated"], request.form["power_type"], request.form["power_unites"], request.form["qty_attacks"], request.form["qty_tyres"], request.form["tyres"], request.form["total_cost"], request.form['id'])
        )
    return render_template("buggy-form.html", data=record, defaultData=defaultCost, typesData=typesCost)

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning     
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })


@app.route("/info")
def info_page():
    data = requests.get("https://rhul.buggyrace.net/specs/data/types.json")
    cost = json.loads(data.text)
    if request.method == "GET":
        return render_template("info.html", cost=cost)


@app.route('/poster')
def poster():
   return render_template('poster.html')

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    alloc_port = os.environ.get('CS1999_PORT')
    app.run(debug=True, host="0.0.0.0", port=alloc_port)
