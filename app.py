import os
from helper_functions import *
from flask import render_template, redirect, url_for, flash
from flask_paginate import Pagination
from bson.objectid import ObjectId
import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("DATABASE")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

#Data file to write csv to for statistical display                            
data_file = "static/data/recipe_mining.csv"
allergen_data_file = "static/data/allergen_data.csv"

#Gets recipes from mongo or mysql
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    page = get_page()
    _recipes=mongo.db.recipes.find().sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    recipe_list = paginate_list(_recipes, page, 10)
    return render_template("recipe.html", recipes=recipe_list, pagination=pagination)
    
        
@app.route('/recipe/<recipe_id>')
def recipe_description(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe_description.html", recipe=the_recipe)
    
#Search screen for recipes will preload options for allergens and cuisines.
@app.route('/search_recipes')
def search_recipes():
    _cuisines = mongo.db.cuisines.find().sort("cuisine_name")
    cuisine_list = [cuisine for cuisine in _cuisines]
    _allergens = mongo.db.allergens.find().sort("allergen_name")
    allergen_list = [allergen for allergen in _allergens]
    return render_template("searchrecipe.html", allergens = allergen_list, cuisines = cuisine_list)
    

#Partial search for recipe name    
@app.route('/find_recipe_by_name', methods=["POST"])
def find_recipe_by_name():
    page = get_page()
    search_term = {"recipe_name": {'$regex': request.form['recipe_name'], '$options': 'i'}}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Search by cuisine name    
@app.route('/find_recipe_cuisine_name', methods=["POST"])
def find_recipe_cuisine_name():
    page = get_page()
    search_term = {"cuisine_name": request.form['cuisine_name']}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Find recipes by allergen    
@app.route('/find_recipe_allergen_name', methods=["POST"])
def find_recipe_allergen_name():
    page = get_page()
    search_term = {"allergens": request.form['allergens']}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Partial text search of ingredients    
@app.route('/find_recipe_by_ingredient', methods=["POST"])
def find_recipe_by_ingredient():
    page = get_page()
    search_term = {"ingredients": {'$regex': request.form['ingredient_name'], '$options': 'i'}}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Form for adding new recipes to database    
@app.route("/add_recipe")
def add_recipe():
    _cuisines = mongo.db.cuisines.find().sort("cuisine_name", pymongo.ASCENDING)
    _allergens = mongo.db.allergens.find().sort("allergen_name", pymongo.ASCENDING)
    _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
    return render_template("addrecipe.html", allergens = _allergens, cuisines = _cuisines, countries = _countries)
    

#Inserting recipes into databse
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    try:
        recipes = mongo.db.recipes
        new_recipe = create_recipe()
        recipes.insert_one(new_recipe)
    except: 
        flash("All fields must be filled!")
        return redirect(url_for("add_recipe"))
    
    return redirect(url_for('get_recipes'))   

#Different templates required to send id for mysql many to many searches and updates
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", pymongo.ASCENDING)
    allergens = mongo.db.allergens.find().sort("allergen_name", pymongo.ASCENDING)
    _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
    return render_template("editrecipe.html", recipe=the_recipe, cuisines=cuisines, 
                        allergens=allergens, countries=_countries)
    

#Deleting in mysql requires deletion of many to many table rows that contain the allergens in the recipe.     
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

#Updating recipes after editing
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    updated_recipe = create_recipe()
    recipes.update({'_id': ObjectId(recipe_id)},{"$set": updated_recipe})
    return redirect(url_for('recipe_description', recipe_id=recipe_id))

#Will list all cuisines on the system and will display their descriptions    
@app.route('/get_cuisines')
def get_cuisines():
    page = get_page()
    _cuisines = mongo.db.cuisines.find()
    pagination = Pagination(page=page, total=_cuisines.count(), record_name='cuisines')
    cuisine_list = paginate_list(_cuisines, page, 10)
    return render_template('cuisine.html', cuisines=cuisine_list, pagination=pagination)

#Will list all countries in databases
@app.route('/get_countries')
def get_countries():
    page = get_page()
    _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
    pagination = Pagination(page=page, total=_countries.count(), record_name='countries')
    country_list = paginate_list(_countries, page, 10)
    return render_template('countries.html', countries=country_list, pagination=pagination)

#Render template for adding new country
@app.route("/add_country")
def add_country():
    return render_template("addcountry.html")

#Insert new country into database    
@app.route('/insert_country', methods=['POST'])
def insert_country():
    countries = mongo.db.countries
    new_country = create_country()
    countries.insert_one(new_country)
    return redirect(url_for('get_countries')) 
    
#Render template for editing countries    
@app.route('/edit_country/<country_id>')
def edit_country(country_id):
    the_country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
    return render_template("editcountry.html", country=the_country)
    
#Deleting countries from database    
@app.route('/delete_country/<country_id>')
def delete_country(country_id):
    mongo.db.countries.remove({'_id': ObjectId(country_id)})
    return redirect(url_for('get_countries'))
 
#Updating countries in database 
@app.route('/update_country/<country_id>', methods=['POST'])
def update_country(country_id):
    new_country = create_country()
    mongo.db.countries.update( {'_id': ObjectId(country_id)}, new_country)
    return redirect(url_for('get_countries'))

#Render template for adding new cuisine    
@app.route("/add_cuisine")
def add_cuisine():
    return render_template("addcuisine.html")    

#Insert new cuisine into database 
@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    new_cuisine = create_cuisine()
    cuisines.insert_one(new_cuisine)
    return redirect(url_for('get_cuisines')) 

#Render template for editing cuisines    
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    return render_template("editcuisine.html", cuisine=the_cuisine)
    
#Deleting cuisines from database    
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))
 
#Updating cuisines in database 
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    new_cuisine = create_cuisine()
    mongo.db.cuisines.update( {'_id': ObjectId(cuisine_id)}, new_cuisine)
    return redirect(url_for('get_cuisines'))

#List all allergens in the database.    
@app.route('/get_allergens')
def get_allergens():
    page = get_page()
    _allergens = mongo.db.allergens.find().sort("allergen_name")
    pagination = Pagination(page=page, total=_allergens.count(), record_name='allergens')
    allergen_list = paginate_list(_allergens, page, 10)
    return render_template('allergen.html', allergens=allergen_list, pagination=pagination)
    
#Template for adding a new allergen
@app.route("/add_allergen")
def add_allergen():
    return render_template("addallergen.html")    

#Inserting a new allergen into the database
@app.route('/insert_allergen', methods=['POST'])
def insert_allergen():
    allergens = mongo.db.allergens
    new_allergen = create_allergen()
    allergens.insert_one(new_allergen)
    return redirect(url_for('get_allergens')) 
    
#Render template for editing allergens   
@app.route('/edit_allergen/<allergen_id>')
def edit_allergen(allergen_id):
    the_allergen = mongo.db.allergens.find_one({"_id": ObjectId(allergen_id)})
    return render_template("editallergen.html", allergen=the_allergen)
    
#Delete allergen from database    
@app.route('/delete_allergen/<allergen_id>')
def delete_allergen(allergen_id):
    mongo.db.allergens.remove({'_id': ObjectId(allergen_id)})
    return redirect(url_for('get_allergens'))
 
#Update allergen in database
@app.route('/update_allergen/<allergen_id>', methods=['POST'])
def update_allergen(allergen_id):
    new_allergen = create_allergen()
    mongo.db.allergens.update( {'_id': ObjectId(allergen_id)}, new_allergen)
    return redirect(url_for('get_allergens'))

#Increase the upvotes by clicking on the thumbs up button, then be redirected to that specific recipe page
@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, { "$inc" :{'upvotes': 1}})
    return redirect(url_for('recipe_description', recipe_id=recipe_id))

#Create a csv file from data in db and display in charts
@app.route('/display_stats')
def display_stats():
    cursor= mongo.db.recipes.find({}, {'_id':0,"username":1, "recipe_name":1, "author":1, "prep_time":1, "cook_time":1, "upvotes": 1, "cuisine_name":1, "country":1})
    write_to_csv(data_file, cursor)
    write_allergens_csv_mongo(get_allergens_data(), allergen_data_file)
    return render_template("statistics.html")

app.secret_key = os.environ.get('SECRET_KEY')  

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)