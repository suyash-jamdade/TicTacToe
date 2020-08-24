from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)

# app.config["SECRET_KEY"] = '3464b9227663ae8ff9abec840f1b563c'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

# db = SQLAlchemy(app)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/start")
def start():
    if "board" not in session:
        default()
    session["moves"] += 1
    print(session["moves"])
    if session["moves"] == 9:
        return render_template("result.html")
    return render_template("game.html", game=session["board"], turn=session["turn"])


@app.route("/clear")
def clear():
    default()
    return redirect(url_for("start"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["turn"] = switch_player(session["turn"])

    if ((session["board"][row][0] == session["board"][row][1] == session["board"][row][2]) and (
            session["board"][row][0] is not None)):
        winner = session["board"][row][0]
        return render_template("result.html", win=winner)

    if ((session["board"][0][col] == session["board"][1][col] == session["board"][2][col]) and (
            session["board"][0][col] is not None)):
        winner = session["board"][0][col]
        return render_template("result.html", win=winner)

    if (session["board"][0][0] == session["board"][1][1] == session["board"][2][2]) and (
            session["board"][0][0] is not None):
        winner = session["board"][0][0]
        return render_template("result.html", win=winner)

    if (session["board"][0][2] == session["board"][1][1] == session["board"][2][0]) and (
            session["board"][0][2] is not None):
        winner = session["board"][0][2]
        return render_template("result.html", win=winner)

    return redirect(url_for("start"))


@app.route("/computer_move")
def computer_move():
    if "board" not in session:
        default()
    move = minmax(session["board"], session["turn"])
    return redirect(url_for("play", row=str(move[1][0]), col=str(move[1][1])))


@app.route("/reset")
def reset():
    default()
    return render_template("game.html", game=session["board"], turn=session["turn"])


def default():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    session["moves"] = 0
    return session["board"],session["turn"],session["moves"]


def switch_player(player):
    if player == "X":
        return "O"
    else:
        return "X"


def isOver(board, moves):
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return (True, row[0])
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return (True, board[0][col])
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return (True, board[0][0])
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return (True, board[1][1])
    if moves == 9:
        return (True, None)
    return (False, None)


def minmax(curBoard, turn):
    # X wins = 1, O wins = -1, tie = 0
    possMoves = []
    for i in range(3):
        for j in range(3):
            if curBoard[i][j] == None:
                possMoves.append((i, j))

    over = isOver(curBoard, 9 - len(possMoves))
    if over[0]:
        if over[1] == "X":
            return (1, None)
        elif over[1] == "O":
            return (-1, None)
        else:
            return (0, None)

    if turn == "X":
        maxmove = None
        maxval = -2
        for a in possMoves:
            c = curBoard[:]
            c[a[0]][a[1]] = "X"
            result = minmax(c, "O")
            c[a[0]][a[1]] = None
            if result[0] > maxval:
                maxval = result[0]
                maxmove = a
        return (maxval, maxmove)
    else:
        minmove = None
        minval = 2
        for a in possMoves:
            c = curBoard[:]
            c[a[0]][a[1]] = "O"
            result = minmax(c, "X")
            c[a[0]][a[1]] = None
            if result[0] < minval:
                minval = result[0]
                minmove = a
        return (minval, minmove)


if __name__ == '__main__':
    app.run(debug=True)
