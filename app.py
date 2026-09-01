import os
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "users.db"))


def get_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


@app.route("/", methods=["GET", "POST"])
def index():

    message = ""

    user = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)

        user = cursor.fetchone()

        conn.close()

    if user:
        session["username"] = user[1]
        session["role"] = user[3]
        return redirect(url_for("profile"))
    else:
        message = "用户名或密码错误！"

    return render_template("index.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            message = "两次密码不一致！"

        else:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )

            user = cursor.fetchone()

            if user:
                message = "用户名已经存在！"

            else:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, "user")
                )

                conn.commit()
                message = "注册成功！"

            conn.close()

    return render_template(
    "register.html",
    message=message
    )


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    return render_template("profile.html", username=username,role=session["role"])

@app.route("/message", methods=["GET", "POST"])
def message():

    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()


    if request.method == "POST":

        content = request.form.get("content")

        cursor.execute(
            "INSERT INTO messages(username, content) VALUES (?, ?)",
            (username, content)
        )

        conn.commit()


    cursor.execute(
        "SELECT * FROM messages WHERE username=?",
        (username,)
    )

    messages = cursor.fetchall()

    conn.close()


    return render_template(
        "message.html",
        messages=messages
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



@app.route("/delete/<int:id>")
def delete(id):


    if "username" not in session:
        return redirect(url_for("index"))


    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM messages WHERE id=? AND username=?",
        (id, username)
    )


    conn.commit()
    conn.close()


    return redirect(url_for("message"))



@app.route("/admin")
def admin():

    if "username" not in session:
        return redirect(url_for("index"))

    if session["role"] != "admin":
        return "权限不足"

    return render_template(
    "admin.html",
    username=session["username"],
    role=session["role"]
)




if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
