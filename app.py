from flask import Flask,request,jsonify
import sqlite3
from flask_cors import CORS

def users_database():

    con = sqlite3.connect('users.db')
    print("Created Database successfully")

    con.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY , name TEXT, surname TEXT, email TEXT, password TEXT)')
    print("Users Table created successfully")
    
    con.execute('CREATE TABLE IF NOT EXISTS voting(id INTEGER PRIMARY KEY AUTOINCREMENT , logo TEXT, name TEXT, acronym TEXT, Leaders TEXT, votes INTEGER)')
    print("Users Table created successfully")

    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM users")
    print(mycursor.fetchall())

    con.close()

users_database()

app = Flask (__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
@app.route('/add-user/', methods=['POST'])
def add_new_user():
     if request.method == "POST":
         msg= None
         try:
            post_data = request.get_json()
            id_no = post_data['id']
            name = post_data['name']
            surname = post_data['surname']
            email = post_data['email']
            password = post_data['password']

            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                conn.row_factory = dict_factory
                cur.execute("INSERT INTO users(id, name, surname, email, password) VALUES(?,?,?,?,?)", (id_no, name, surname, email, password))
                conn.commit()
                msg = "Record added successfully"

         except Exception as e:
            msg = 'error'+ str(e)

         finally:
            return {'msg': msg}

@app.route('/show-users/', methods=['GET'])
def show():
    try:
        with sqlite3.connect('users.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                cur.execute("SELECT * FROM users")
                rows = cur.fetchall()
    except Exception as e:
        print("Something went wrong" + str(e))
    return jsonify(rows)


# --------------- Voting Begins ------------------#
# @app.route('/poll/', methods=['POST'])
# def vot():
    # with sqlite3.connect('users.db') as conn:
        # cur = conn.cursor()
        # conn.row_factory = dict_factory
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/ncW9BswZ/R86a79793bbd6a3fee97ec7bb98a1fbc7-rik-UZzeq-Vu-Hh-IJg-Nw-riu-http-cdn-bdlive-co-za-images-logos-ANClog.jpg', 'African National Congress', 'ANC', 'https://i.postimg.cc/2yZFMP69/OIP.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/NfM73JJx/800px-Democratic-Alliance-SA-logo-svg.png', 'Democratic Alliance', 'DA', 'https://i.postimg.cc/d0mykrN1/1024px-John-Steenhuisen.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/fLyRz961/Logo-of-the-EFF.png', 'Economic Freedom Fighters', 'EFF', 'https://i.postimg.cc/MZhVL6Bz/Julius-Malema-EFF-CIC-2019.png'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/ZYQzgXn4/800px-Inkatha-Freedom-Party-logo-svg.png', 'Inkatha Freedom Party', 'IFP', 'https://i.postimg.cc/Hsh62CS1/Velenkosini-Hlabisa.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/13FbVtyj/800px-Freedom-Front-Plus-svg.png', 'Freedom Front Plus', 'VF+', 'https://i.postimg.cc/XqMsbKCN/800px-PJ-Groenewald-cropped.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/2SZ8jh3b/800px-Congress-of-the-People-logo-svg.png', 'Congress of the People', 'COPE', 'https://i.postimg.cc/hjTMrCC8/Defense-gov-News-Photo-991207-D-9880-W-182-cropped.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/RCbyZYkh/800px-Pan-Africanist-Congress-of-Azania-logo-svg.png', 'Pan Africanist Congress of Azania', 'PAC', 'https://i.postimg.cc/prYgrVzF/R1bd70bd86aa4784b536d53c03a8b86f3-rik-Yy-Y1-Un-Ig-o-OOt-A-riu-http-www-pa-org-za-media-root-images-MZWA.jpg'))
        # cur.execute("INSERT OR IGNORE into voting(logo, name, acronym, Leaders) VALUES (?, ?, ?, ?)",('https://i.postimg.cc/NfD40294/Al-Jama-ah-logo.png', 'Al Jama-ah', 'ALJAMA-AH', 'https://i.postimg.cc/7PshYxPz/SABC-News-al-jamah-Ganief-Hendriks.jpg'))
        # conn.commit()
# vot()

@app.route('/list-poll/', methods=['GET'])
def list_poll():
    polls = []
    try:
        with sqlite3.connect('users.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                cur.execute("SELECT * FROM voting")
                polls = cur.fetchall()
    except Exception as e:
        conn.rollback()
        print("Something went wrong" + str(e))
    finally:
        conn.close()
    return jsonify(polls)

# -------- Adding up votes --------- #




