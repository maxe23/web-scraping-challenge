from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask
app = Flask(__name__)
# establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route for index.html
@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars =mars_data)

# Route for Scrape function
@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_scraped =scrape_mars.scrape()
    mars.update({},mars_scraped, upsert=True)
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)