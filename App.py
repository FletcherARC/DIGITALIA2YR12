from flask import Flask, render_template, session, redirect, url_for
from forms import LoginForm, NameForm
import sqlite3

app = Flask(__name__)
app.secret_key = 'verysecretkeyfrong'




@app.route('/', methods=["GET", "POST"])
def Index(data="PLEASE LOGIN"):
    return render_template('Index.html', login=False, data=data)

@app.route('/Login', methods=["GET", "POST"])
def Login(data="No Form Yet"):
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email = form.email.data
        data = [name, password, email]
        return Index(data=data)
    return render_template('Login.html', login=True, form=form, data=data)

@app.route('/Games', methods=["GET", "POST"])
def Games(data="GAME LIST"):
    form = NameForm()
    if form.validate_on_submit():
        name = str(form.name.data)
    else:
        name = ''
    con = sqlite3.connect("Games_Table.db")
    cur = con.cursor()
    games_data = cur.execute("SELECT column2 as 'Name', column3 AS 'Platform', column4 AS 'Year' FROM GamesList WHERE column2 = ?", (name,))
    games_data = games_data.fetchall()
    con.close()
    return render_template('Games.html', login=False, data=games_data, form=form)



if __name__ == '__main__':
    app.run(debug=True)
