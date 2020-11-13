# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped in mission_to_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


# Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.

@app.route('/')
def home():

    page_data = mongo.db.mars.find_one()

    return render_template("index.html", data=page_data)


# Create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# Create `scrape` function that will execute all of your scraping code from above
# Return one Python dictionary containing all of the scraped data.
# Store the return value in Mongo
@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)






if __name__ == "__main__":
    app.run(debug=True)
