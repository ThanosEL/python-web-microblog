import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.MicroBlog


    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry__content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%d-%m-%Y")
            app.db.entries.insert_one({"content": entry__content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]    
        return render_template("home.html", entries=entries_with_date)
    
    return app