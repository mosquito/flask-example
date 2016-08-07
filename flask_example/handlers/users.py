from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from ..app import app
from ..models.users import User


@app.route("/users/", methods=['GET'])
def users():
    return render_template("users.html", users=User.query.all())


@app.route("/users/", methods=['POST'])
def add_user():
    user = User(
        name=request.form['name'],
        email=request.form['email'],
    )

    app.db.add(user)
    app.db.commit()

    return redirect(url_for('users'), code=302)
