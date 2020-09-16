from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class sitetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newstitle = db.Column(db.String(25), nullable=False)
    hexcolor = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    describe = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False)

class hometable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(25), nullable=False)
    plaintext = db.Column(db.Text, nullable=False)
    addlinks = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    return render_template("mainpage/index.html", nevs_data=sitetable.query.all(), hw_preview=len(hometable.query.all()))

@app.route("/assign", methods=["POST", "GET"])
def adding():
    if request.method != "POST":
        return render_template("create-note/index.html")
    else:
        newstitle = request.form["subject"]
        hexcolor = request.form["hexcolor"]
        category = request.form["categ"]
        describe = request.form["describe"]
        author = request.form["author"]
        maintext = request.form["maintext"]
        newid = len(sitetable.query.all())+1
        item = sitetable(newstitle=newstitle,hexcolor=hexcolor, category=category, describe=describe, author=author)
        db.session.add(item)
        db.session.commit()
        with open("templates/news/"+str(newid)+".html", "w", encoding="utf-8") as handle:
            data = '''
{% extends 'news/newsbase.html' %}
{% block title %}'''+newstitle+'''{% endblock %}
{% block header %}'''+newstitle+'''{% endblock %}
{% block maintext %}'''+maintext+'''{% endblock %}
'''
            handle.write(data)
            handle.close()
            return redirect("/")

@app.route("/view-news/<int:newspaper>")
def viewnewspaper(newspaper):
    return render_template("news/"+str(newspaper)+".html")

@app.route("/h")
def homewrk_view():
    return render_template("hw/index.html", hw=hometable.query.all())

@app.route("/add-homework", methods=["POST", "GET"])
def add_homework():
    if request.method != "POST":
        return render_template("hw/add.html")
    else:
        sub = request.form["subject"]
        maintext = request.form["maintext"]
        lnk = request.form["addlinks"]
        item = hometable(subject=sub, plaintext=maintext, addlinks=lnk)
        db.session.add(item)
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)