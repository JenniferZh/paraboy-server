from flask import Flask, jsonify, request, abort
import random
import sqlite3

app = Flask(__name__)
dbpath = 'paraDB.db'


@app.route('/user/sign', methods=['POST'])
def user_sign():
    try:
        id = request.json['id']
        pwd = request.json['pwd']
        rank = random.randint(0, 9)
        online = 0
        with sqlite3.connect(dbpath) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO user (ID, PWD, RANK, ONLINE) VALUES (?,?,?,?)", (id, pwd, rank, online))
            conn.commit()
        return jsonify({'status': 'OK'})
    except:
        conn.rollback()
        return jsonify({'status': 'FAIL'})
    finally:
        conn.close()


@app.route('/user/login', methods=['POST'])
def user_login():
    try:
        id = request.json['id']
        print(id)
        pwd = request.json['pwd']
        with sqlite3.connect(dbpath) as conn:
            cur = conn.cursor()
            cur.execute("SELECT PWD FROM user WHERE ID="+str(id))
            print("SELECT PWD FROM user WHERE ID='"+id+"'")
            row = cur.fetchall()
            print(row[0][0])
            if row is None:
                return jsonify({'status' : 'IDNOTFOUND'})
            elif row[0][0] != pwd:
                return jsonify({'status' : 'WRONGPWD'})
            else:
                cur.execute("UPDATE user SET ONLINE = 1 WHERE ID = " + str(id))
                conn.commit()
                print("haha")
                return jsonify({'status' : 'OK'})
    except:
        conn.rollback()
        return jsonify({'status': 'FAIL'})
    finally:
        conn.close()


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': 123})


if __name__ == '__main__':
    app.run()
