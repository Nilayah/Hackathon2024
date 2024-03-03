import flask
import sqlite3
import hashlib

app = flask.Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return flask.redirect(flask.url_for('signin'))

@app.route("/signin", methods=['GET'])
def signin():
    return flask.render_template("sign_in.html")

@app.route("/signin", methods=['POST'])
def signin_page(): 
    username = flask.request.form['username']
    password = flask.request.form['password']

    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    found = c.execute(f"SELECT EXISTS (SELECT username FROM user WHERE username=? and password=?)", (username, password, )).fetchone()
    c.close()
    conn.close()

    if (found[0] == 1):
        return flask.redirect(f'/main/{username}')
    else:
        return flask.render_template("create_user.html", username=username, password=password)

@app.route("/main/<username>", methods=['GET'])
def main(username):
    conn = sqlite3.connect('data/doctors.db')
    c = conn.cursor()
    doctors = c.execute(f"SELECT * FROM doctor").fetchall()
    c.close()
    conn.close()
    return flask.render_template("main.html", username=username, doctors=doctors)

@app.route("/main/<username>", methods=['POST'])
def main_page(username): 
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    user_info = c.execute(f"SELECT username, password, age, gender, race, ethnicity FROM user WHERE username=?)", (username, )).fetchone()
    c.close()
    conn.close()
    return 0

@app.route("/user", methods=['POST'])
def create_user(): 
    username = flask.request.form['username']
    password = flask.request.form['password']
    age = flask.request.form['age']
    gender = flask.request.form['gender']
    race = flask.request.form['race'] #FIX TO DO MULTIPLE
    ethnicity = flask.request.form['ethnicity']

    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO user (username, password, age, gender, race, ethnicity) VALUES ('{username}', '{password}', '{age}', '{gender}', '{race}', '{ethnicity}')")
    c.close()
    conn.commit()
    conn.close()

    return flask.redirect(f'/main/{username}')

@app.route("/doctor/<username>", methods=['GET'])
def doctor(username):
    return flask.render_template("create_doctor.html", username=username)

@app.route("/doctor/<username>", methods=['POST'])
def create_doctor(username): 
    firstname = flask.request.form['firstname']
    lastname = flask.request.form['lastname']
    location = flask.request.form['location']
    pic = flask.request.form['pic']
    age = flask.request.form['age']
    gender = flask.request.form['gender']
    race = flask.request.form['race'] #FIX TO DO MULTIPLE
    ethnicity = flask.request.form['ethnicity']
    rate = int(flask.request.form['rate'])

    conn = sqlite3.connect('data/doctors.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO doctor (firstname, lastname, age, gender, race, ethnicity, pic, location, rate) VALUES ('{firstname}', '{lastname}', '{age}', '{gender}', '{race}', '{ethnicity}', '{pic}', '{location}', '{rate}')")
    c.close()
    conn.commit()
    conn.close()
    
    return flask.redirect(f'/main/{username}')

@app.route("/viewdoctor/<doctor_name>", methods=['GET'])
def view_doctor(doctor_name):
    conn = sqlite3.connect('data/doctors.db')
    c = conn.cursor()
    doctor_info = c.execute(f"SELECT firstname, lastname, age, gender, race, ethnicity, pic, location, rate FROM doctor WHERE firstname=?", (doctor_name, )).fetchone()
    c.close()
    conn.close()
    return flask.render_template("display_doctor.html", doctor_info=doctor_info)

@app.route("/comment", methods=['GET'])
def comment():
    return flask.render_template("comments.html")

@app.route("/comment/<username>/<doctor_name>", methods=['GET'])
def comment_no(username, doctor_name):
    return flask.render_template("create_comment.html")

@app.route("/comment/<username>/<doctor_name>", methods=['POST'])
def create_comment(username, doctor_name): 
    description = flask.request.form['description']

    conn = sqlite3.connect('data/doctors.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO comments (doctor_name, description, username) VALUES ('{doctor_name}', '{description}', '{username}')")
    c.close()
    #conn.commit()
    conn.close()
    
    return flask.redirect(f'/main/{username}')

@app.route("/view_comments/<doctor_name>", methods=['GET', 'POST'])
def view_comments(doctor_name): 
    description = flask.request.form['description']

    conn = sqlite3.connect('data/doctors.db')
    c = conn.cursor()
    comment_info = c.execute(f"SELECT doctor_name, description, username FROM comments WHERE doctor_name=?)", (doctor_name, )).fetchone()
    user_info = c.execute(f"SELECT username, age, gender, race, ethnicity FROM comments WHERE username=?)", (comment_info[2], )).fetchone()
    c.close()
    #conn.commit()
    conn.close()
    
    return flask.render_template("view_all_comments.html", comment_info=comment_info, user_info=user_info)
    
if __name__ == '__main__':
    # Start the server
    app.run(port=8060, host='127.0.0.1', debug=True, use_evalex=False, use_reloader=False)