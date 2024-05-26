from flask import Flask, render_template, session, redirect, url_for, flash
from forms import LoginForm, NameForm, SignUpForm, CreateTeamForm, AddTeamMember, EventForm
import sqlite3


app = Flask(__name__)
app.secret_key = 'verysecretkeyfrong'


@app.route('/', methods=["GET", "POST"])
def Index(data="PLEASE LOGIN"):
    if not "PersonID" in session:
        return redirect(url_for('Login'))

    PersonID = session.get('PersonID')
    con = sqlite3.connect("DatabaseTable.db")
    cur = con.cursor()
    event_data = cur.execute("SELECT Team1.TeamName, GamesList.column2, Team2.TeamName, EventInfo.EventDate, EventInfo.EventName, EventInfo.Description FROM EventInfo INNER JOIN TeamNames as Team1 ON EventInfo.TeamIDOne = Team1.TeamID INNER JOIN TeamNames as Team2 ON EventInfo.TeamIDTwo = Team2.TeamID INNER JOIN GamesList ON GamesList.column1 = EventInfo.GameID WHERE Team1.TeamID IN (SELECT TeamID FROM TeamMembers WHERE PersonID = ?) OR Team2.TeamID IN (SELECT TeamID FROM TeamMembers WHERE PersonID = ?)", (PersonID, PersonID, )).fetchall()
    games_data = cur.execute("SELECT GamesList.column2 as 'Name', GamesList.column1 AS 'GameID' FROM GamesList INNER JOIN FavoriteGames ON GamesList.column1 = FavoriteGames.column1 WHERE FavoriteGames.PersonID = ?", (PersonID,))
    games_data = games_data.fetchall()
    con.close()
    return render_template('index.html', data=games_data, event_data=event_data)

@app.route('/Login', methods=["GET", "POST"])
def Login(data="No Form Yet", PasswordFind="no password"):
    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        data = [password, email]
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        PasswordFind = cursor.execute("SELECT PasswordName, PersonID FROM UserInfo WHERE EmailName = ?", (email,)).fetchone()
        if PasswordFind:

            if PasswordFind[0] == password:
                session['PersonID'] = PasswordFind[1]
                flash("You successfully logged in!", 'info')
                return render_template('Index.html')
    return render_template('Login.html', login=False, form=form, data=data, PasswordFind=PasswordFind)

@app.route('/SignUp', methods=["GET", "POST"])
def SignUp(data="SIGN UP PLS"):
    form = SignUpForm()
    if form.validate_on_submit():
        last_name = form.lname.data
        first_name = form.name.data
        password = form.password.data
        email = form.email.data
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        cursor.execute( "INSERT INTO UserInfo VALUES(NULL,?,?,?,?)", (last_name, first_name, password, email,))
        con.commit()
        con.close()
    return render_template('SignUp.html', data=data, form=form)
@app.route('/Games', methods=["GET", "POST"])
def Games(data="GAME LIST"):
    if not "PersonID" in session:
        return redirect(url_for('Login'))
    form = NameForm()
    if form.validate_on_submit():
        name = str(form.name.data)
    else:
        name = ''
    con = sqlite3.connect("DatabaseTable.db")
    cur = con.cursor()
    games_data = cur.execute("SELECT column2 as 'Name', column3 AS 'Platform', column4 AS 'Year', column1 AS 'GameID' FROM GamesList WHERE column2 LIKE ?", (f"%{name}%",))
    games_data = games_data.fetchall()[1::]
    con.close()
    return render_template('Games.html', login=False, data=games_data, form=form)

@app.route('/GamesData/<column1>', methods=["GET", "POST"])
def GamesData (column1):
    if not "PersonID" in session:
        return redirect(url_for('Login'))
    con = sqlite3.connect("DatabaseTable.db")
    cur = con.cursor()
    games_data = cur.execute("SELECT column2 as 'Name', column3 AS 'Platform', column4 AS 'Year', column5 AS 'Genre', column6 AS 'Publisher' FROM GamesList WHERE column1 = ?", (column1,)).fetchone()
    con.close()
    return render_template('GamesData.html', games_data=games_data, column1=column1)


@app.route('/CreateTeam/<column1>', methods=["GET", "POST"])
def CreateTeam (column1):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    form = CreateTeamForm()
    if form.validate_on_submit():
        TeamName = form.TeamName.data
        TeamSpeech = form.TeamSpeech.data
        TeamCaptain = session.get('PersonID')
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO TeamNames VALUES(NULL,?,?,?,?)", (TeamName, TeamSpeech, column1, TeamCaptain,))
        con.commit()
        con.close()
        return redirect(url_for('Teams'))
    return render_template("CreateTeam.html", column1=column1, form=form)

@app.route('/logout')
def logout():
    session.pop('PersonID', None)
    return redirect(url_for('Index'))

@app.route('/addfavorite/<column1>', methods=["GEt", "POST"])
def addfavorite (column1):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    try:
        PersonID = session.get('PersonID')
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO FavoriteGames VALUES(?,?)", (column1, PersonID,))
        con.commit()
        con.close()
    except:
        flash("Game already in Favorites")
    return redirect(url_for('Games'))

@app.route('/teams', methods=["GET", "POST"])
def Teams():
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    PersonID = session.get('PersonID')
    con = sqlite3.connect("DatabaseTable.db")
    cursor = con.cursor()
    captain_of = cursor.execute("SELECT TeamName, TeamSpeech, TeamGame FROM TeamNames WHERE TeamCaptain = ?", (PersonID,)).fetchall()
    con.close()
    con = sqlite3.connect("DatabaseTable.db")
    cursor = con.cursor()
    member_of = cursor.execute("SELECT TeamNames.TeamName, group_concat(UserInfo.FirstName), TeamNames.TeamCaptain, TeamNames.TeamSpeech, TeamNames.TeamID, GamesList.column2 FROM TeamNames LEFT JOIN TeamMembers ON TeamNames.TeamID = TeamMembers.TeamID LEFT JOIN UserInfo ON UserInfo.PersonID = TeamMembers.PersonID LEFT JOIN GamesList ON TeamNames.TeamGame = GamesList.column1 WHERE TeamNames.TeamCaptain IN (SELECT TeamCaptain FROM TeamNames INNER JOIN TeamMembers ON TeamNames.TeamID = TeamMembers.TeamID WHERE TeamMembers.PersonID = ?) OR TeamNames.TeamCaptain = ? GROUP BY TeamNames.TeamID", (PersonID,PersonID,)).fetchall()
    con.close()
    return render_template('teams.html', captain_of=captain_of, member_of=member_of)


@app.route('/removefavorite/<column1>', methods=["GET", "POST"])
def removefavorite (column1):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    try:
        PersonID = session.get('PersonID')
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM FavoriteGames WHERE column1 = ? AND PersonID = ?", (column1, PersonID,))
        con.commit()
        con.close()
    except:
        flash("Game already not in favorites")
    return redirect(url_for('Games'))


@app.route('/AddMembers/<TeamID>', methods=["GET", "POST"])
def AddMembers(TeamID):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    form = AddTeamMember()
    if form.validate_on_submit():
        try:
            email = form.emailname.data
            con = sqlite3.connect("DatabaseTable.db")
            cursor = con.cursor()
            cursor.execute("INSERT INTO TeamMembers VALUES(?, (SELECT PersonID FROM UserInfo WHERE EmailName = ?))", (TeamID, email,))
            con.commit()
            con.close()
            flash("Member added")
        except sqlite3.IntegrityError:
            flash("Member already in team.")
        except:
            flash("No user found with email.")

    return render_template('AddMembers.html', form=form, TeamID=TeamID)

@app.route('/ShowRivalTeams/<TeamID>', methods=["GET", "POST"])
def ShowRivalTeams(TeamID):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    con = sqlite3.connect("DatabaseTable.db")
    cursor = con.cursor()
    Teams = cursor.execute("SELECT TeamName, TeamID FROM TeamNames WHERE TeamGame = (SELECT TeamGame FROM TeamNames WHERE TeamID = ?) AND TeamID != ?", (TeamID, TeamID,)).fetchall()
    con.close()
    return render_template('ShowRivalTeams.html', TeamID=TeamID, Teams=Teams)

@app.route('/CreateEvent/<TeamID1>/<TeamID2>', methods=["GET", "POST"])
def CreateEvent(TeamID1, TeamID2):
    if "PersonID" not in session:
        return redirect(url_for('Login'))
    form = EventForm()
    if form.validate_on_submit():
        eventdate = form.eventdate.data
        eventname = form.eventname.data
        eventdesc = form.eventdesc.data
        con = sqlite3.connect("DatabaseTable.db")
        cursor = con.cursor()
        gameID = cursor.execute("SELECT TeamGame FROM TeamNames WHERE TeamID = ?", (TeamID1,)).fetchall()
        cursor.execute("INSERT INTO EventInfo Values(NULL,?,?,?,?,?,?)", (eventname, eventdate, TeamID1,TeamID2, gameID[0][0], eventdesc,))
        con.commit()
        con.close()
        flash("Successfully Created")
        return redirect(url_for('Index'))
    return render_template('CreateEvent.html', TeamID1=TeamID1, TeamID2=TeamID2, form=form)
if __name__ == '__main__':
    app.run(debug=True)
