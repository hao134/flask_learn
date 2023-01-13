from app import app

from flask import render_template, request, redirect, jsonify, make_response

from datetime import datetime

import os

from werkzeug.utils import secure_filename

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
def index():

    # print(f"Flask ENV is set to: {app.config['ENV']}")
    # print(app.config["DB_NAME"])

    return render_template("public/index.html")

@app.route("/jinja")
def jinja():

    my_name = "Shih hao"

    age = 28

    langs = ["Python", "Javascript", "Golang", "Bash"]

    friends = {
        "shinchi":27,
        "an":27,
        "lishi":48,
        "liching":47
    }

    colours = ("Red", "Green")
    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pullin repo {self.name}"

        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name = "Flask Jinja",
        description = "Template design tutorial",
        url = "https://github.com/hao134/flask_learn"
    )
    def repeat(x, qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>THIS IS SOME HTML</h1>"

    suspicious = "<script>alert('You got hacked!!!')</script>"

    return render_template("public/jinja.html", my_name = my_name, age=age,
                            langs=langs, friends=friends, colours=colours,
                            cool=cool, GitRemote = GitRemote, repeat=repeat,
                            my_remote = my_remote, date = date, my_html = my_html,
                            suspicious=suspicious
    )


@app.route("/about")
def about():
    return "<h1 style='color:red'>About!</h1>"

@app.route("/sign-up", methods=["GET","POST"])
def sign_up():

    if request.method == "POST":

        req = request.form 

        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sign_up.html")


users = {
    "mitsuhiko" : {
        "name" : "Armin Ronacher",
        "bio" : "Creatof of the Flask framework",
        "twitter_handle" : "@mitsuhiko"
    },
    "gvanrossum" : {
        "name" : "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk" : {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle" : "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)

@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"foo is {foo}, bar is {bar}, baz is {baz}"

@app.route("/json", methods=["POST"])
def json():

    if request.is_json:

        req = request.get_json()

        response = {
            "message" : "JSON received",
            "name": req.get("name")
        }

        res = make_response(jsonify(response), 200)

        return res
    else:
        res = make_response(jsonify({"message":"No JSON received"}),400)
        return res

@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req),200)

    return res

# put this string after /query : ?foo=foo&bar=bar&baz=baz&title=query+strings+with+flask
@app.route("/query")
def query():

    if request.args:
        args = request.args

        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())

        return f"(Query {serialized})", 200

    else:
        return "No query received", 200

app.config["IMAGE_UPLOADS"] = "/Users/shihhao/Desktop/Projects/Python/flask_app/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 2.0 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".",1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods = ["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            if not allowed_image_filesize(request.cookies.get('filesize')):
                print("File exceed maximum size")
                return redirect(request.url)
            
            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extensions is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("image is saved")

            return redirect(request.url)

    return render_template("public/upload_image.html")

from flask import send_from_directory, abort

"""
string:
int:
float:
path:
uuid:
"""

app.config["CLIENT_IMAGES"] = "/Users/shihhao/Desktop/Projects/Python/flask_app/app/static/client/img"
app.config["CLIENT_CSV"] = "/Users/shihhao/Desktop/Projects/Python/flask_app/app/static/client/csv"
app.config["CLIENT_REPORTS"] = "/Users/shihhao/Desktop/Projects/Python/flask_app/app/static/client/reports"

@app.route("/get-image/<image_name>")
def get_image(image_name):

    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=False
        )
    except FileNotFoundError:
        abort(404)

    return "Thanks"

@app.route("/get-csv/<filename>")
def get_csv(filename):

    try:
        return send_from_directory(
            app.config["CLIENT_CSV"], filename=filename, as_attachment=False
        )
    except FileNotFoundError:
        abort(404)

    return "Thanks"

@app.route("/get-report/<path:path>")
def get_csv(path):
    try:
        return send_from_directory(
            app.config["CLIENT_REPORTS"], filename=path, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)