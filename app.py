import os
from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_pymongo import PyMongo, pymongo
import pymysql
from flask_paginate import Pagination
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from bson import json_util
from classes import *
import csv
from mysql_from_python import *

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'pat_doc_recipedb'
app.config["MONGO_URI"] = 'mongodb://admin:1Pfhr39Hdi4@ds119060.mlab.com:19060/pat_doc_recipedb'

mongo = PyMongo(app)
username = os.getenv('C9_USER')

connection = pymysql.connect(host="localhost",
                            user=username,
                            password = '',
                            db='recipes')
                            
data_file = "static/data/recipe_mining.csv" 
#Change between 'mysql' and 'mongo' to change database
database = "mysql" 

#Gets recipes from mongo or mysql
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    page = get_page()
    if database == "mongo":
        _recipes=mongo.db.recipes.find().sort('upvotes', pymongo.DESCENDING)
        pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
        recipe_list = paginate_list(_recipes, page, 10)
        return render_template("recipe.html", recipes=recipe_list, pagination=pagination)
    elif database == "mysql":
        _recipes = get_recipes_mysql()
        pagination = Pagination(page=page, total=len(_recipes), record_name='recipes')
        recipe_list = paginate_list(_recipes, page, 10)
        return render_template("recipemysql.html", recipes=recipe_list, pagination=pagination)

#Search screen for recipes will preload options for allergens and cuisines.
@app.route('/search_recipes')
def search_recipes():
    if database == "mongo":
        _cuisines = mongo.db.cuisines.find().sort("cuisine_name")
        cuisine_list = [cuisine for cuisine in _cuisines]
        _allergens = mongo.db.allergens.find().sort("allergen_name")
        allergen_list = [allergen for allergen in _allergens]
        return render_template("searchrecipe.html", allergens = allergen_list, cuisines = cuisine_list)
    elif database == "mysql":
        _cuisines = get_cuisines_mysql()
        _allergens = get_allergens_mysql()
        return render_template("searchrecipemysql.html", allergens=_allergens, cuisines=_cuisines)

#Partial search for recipe name    
@app.route('/find_recipe_by_name', methods=["POST"])
def find_recipe_by_name():
    page = get_page()
    if database == "mongo":
        search_term = {"recipe_name": {'$regex': request.form['recipe_name'], '$options': 'i'}}
        _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
        pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    elif database == "mysql":
        _recipes = find_recipe_by_name_mysql()
        pagination = Pagination(page=page, total=len(_recipes), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Search by cuisine name    
@app.route('/find_recipe_cuisine_name', methods=["POST"])
def find_recipe_cuisine_name():
    page = get_page()
    if database == "mongo":
        search_term = {"cuisine_name": request.form['cuisine_name']}
        _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
        pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    elif database == "mysql":
        _recipes = find_recipe_by_cuisine_name_mysql()
        pagination = Pagination(page=page, total=len(_recipes), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Find recipes by allergen    
@app.route('/find_recipe_allergen_name', methods=["POST"])
def find_recipe_allergen_name():
    page = get_page()
    if database == "mongo":
        search_term = {"allergens": request.form['allergens']}
        _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
        pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    elif database == "mysql":
        _recipes = find_recipes_by_allergens()
        pagination = Pagination(page=page, total=len(_recipes), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Partial text search of ingredients    
@app.route('/find_recipe_by_ingredient', methods=["POST"])
def find_recipe_by_ingredient():
    page = get_page()
    if database == "mongo":
        search_term = {"ingredients": {'$regex': request.form['ingredient_name'], '$options': 'i'}}
        _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
        pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    elif database == "mysql":
        _recipes = find_recipe_by_ingredient_mysql()
        pagination = Pagination(page=page, total=len(_recipes), record_name='recipes')
    matching_recipes = paginate_list(_recipes, page, 10)
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

#Form for adding new recipes to database    
@app.route("/add_recipe")
def add_recipe():
    if database == "mongo":
        _cuisines = mongo.db.cuisines.find().sort("cuisine_name", pymongo.ASCENDING)
        _allergens = mongo.db.allergens.find().sort("allergen_name", pymongo.ASCENDING)
        _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
        return render_template("addrecipe.html", allergens = _allergens, cuisines = _cuisines, countries = _countries)
    elif database == "mysql":
        _cuisines = get_cuisines_mysql()
        _allergens = get_allergens_mysql()
        _countries =get_countries_mysql()
        return render_template("addrecipemysql.html", allergens = _allergens, cuisines = _cuisines, countries = _countries)

#Inserting recipes into databse
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    if database == "mongo":
        recipes = mongo.db.recipes
        new_recipe = create_recipe()
        recipes.insert_one(new_recipe)
    elif database == "mysql": #recipes and allergens are inserting separately due to many to many table for allergens
        insert_recipe_mysql()
        insert_allergens_to_recipe(get_most_recent_recipe_id())
    return redirect(url_for('get_recipes'))   

#Different templates required to send id for mysql many to many searches and updates
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    if database == "mongo":
        the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        cuisines = mongo.db.cuisines.find().sort("cuisine_name", pymongo.ASCENDING)
        allergens = mongo.db.allergens.find().sort("allergen_name", pymongo.ASCENDING)
        _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
        return render_template("editrecipe.html", recipe=the_recipe, cuisines=cuisines, 
                            allergens=allergens, countries=_countries)
    elif database == "mysql":
        the_recipe = find_recipe_by_id_mysql(recipe_id)
        cuisines = get_cuisines_mysql()
        existing_allergens = find_allergen_name_by_id(get_existing_allergens_mysql(recipe_id))
        allergens = get_allergens_mysql()
        _countries =get_countries_mysql()
        return render_template("editrecipemysql.html", recipe=the_recipe, cuisines=cuisines, 
                            allergens=allergens, countries=_countries, 
                            existing_allergens= existing_allergens)

#Deleting in mysql requires deletion of many to many table rows that contain the allergens in the recipe.     
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if database == "mongo":
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    elif database == "mysql":
        delete_recipe_mysql(recipe_id)
        delete_recipe_allergen_row(recipe_id)
    return redirect(url_for('get_recipes'))

#Updating recipes after editing
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    if database == "mongo":
        recipes = mongo.db.recipes
        updated_recipe = create_recipe()
        recipes.update({'_id': ObjectId(recipe_id)},{"$set": updated_recipe})
    elif database == "mysql":
        update_recipe_mysql(recipe_id)
        change_allergens_mysql(recipe_id)
    return redirect(url_for('get_recipes'))

#Will list all cuisines on the system and will display their descriptions    
@app.route('/get_cuisines')
def get_cuisines():
    page = get_page()
    if database == "mongo":
        _cuisines = mongo.db.cuisines.find()
        pagination = Pagination(page=page, total=_cuisines.count(), record_name='cuisines')
    elif database == "mysql":
        _cuisines = get_cuisines_mysql()
        pagination = Pagination(page=page, total=len(_cuisines), record_name='cuisines')
    cuisine_list = paginate_list(_cuisines, page, 10)
    return render_template('cuisine.html', cuisines=cuisine_list, pagination=pagination)

#Will list all countries in databases
@app.route('/get_countries')
def get_countries():
    page = get_page()
    if database == "mongo":
        _countries = mongo.db.countries.find().sort("country_name", pymongo.ASCENDING)
        pagination = Pagination(page=page, total=_countries.count(), record_name='countries')
    elif database == "mysql":
        _countries = get_countries_mysql()
        pagination = Pagination(page=page, total=len(_countries), record_name='countries')
    country_list = paginate_list(_countries, page, 10)
    return render_template('countries.html', countries=country_list, pagination=pagination)

#Render template for adding new country
@app.route("/add_country")
def add_country():
    return render_template("addcountry.html")

#Insert new country into database    
@app.route('/insert_country', methods=['POST'])
def insert_country():
    if database == "mongo":
        countries = mongo.db.countries
        new_country = create_country()
        countries.insert_one(new_country)
    elif database == "mysql":
        insert_country_mysql()
    return redirect(url_for('get_countries')) 

#Render template for adding new cuisine    
@app.route("/add_cuisine")
def add_cuisine():
    return render_template("addcuisine.html")    

#Insert new cuisine into database 
@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    if database == "mongo":
        cuisines = mongo.db.cuisines
        new_cuisine = create_cuisine()
        cuisines.insert_one(new_cuisine)
    elif database == "mysql":
        insert_cuisine_mysql()
    return redirect(url_for('get_cuisines')) 

#Render template for editing cuisines    
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    if database == "mongo":
        the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    elif database == "mysql":
        the_cuisine = get_cuisine_by_id_mysql(cuisine_id)
    return render_template("editcuisine.html", cuisine=the_cuisine)
    
#Deleting cuisines from database    
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    if database == "mongo":
        mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    elif database == "mysql":
        delete_cuisine_mysql(cuisine_id)
    return redirect(url_for('get_cuisines'))
 
#Updating cuisines in database 
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    if database == "mongo":
        new_cuisine = create_cuisine()
        mongo.db.cuisines.update( {'_id': ObjectId(cuisine_id)},
       new_cuisine)
    elif database == "mysql":
        update_cuisine_mysql(cuisine_id)
    return redirect(url_for('get_cuisines'))

#List all allergens in the database.    
@app.route('/get_allergens')
def get_allergens():
    page = get_page()
    if database == "mongo":
        _allergens = mongo.db.allergens.find()
        pagination = Pagination(page=page, total=_allergens.count(), record_name='allergens')
    elif database == "mysql":
        _allergens = get_allergens_mysql()
        pagination = Pagination(page=page, total=len(_allergens), record_name='allergens')
    allergen_list = paginate_list(_allergens, page, 10)
    return render_template('allergen.html', allergens=allergen_list, pagination=pagination)
    
#Template for adding a new allergen
@app.route("/add_allergen")
def add_allergen():
    return render_template("addallergen.html")    

#Inserting a new allergen into the database
@app.route('/insert_allergen', methods=['POST'])
def insert_allergen():
    if database == "mongo":
        allergens = mongo.db.allergens
        new_allergen = create_allergen()
        allergens.insert_one(new_allergen)
    elif database == "mysql":
        insert_allergen_mysql()
    return redirect(url_for('get_allergens')) 
    
#Render template for editing allergens   
@app.route('/edit_allergen/<allergen_id>')
def edit_allergen(allergen_id):
    if database == "mongo":
        the_allergen = mongo.db.allergens.find_one({"_id": ObjectId(allergen_id)})
    elif database == "mysql":
        the_allergen = get_allergen_by_id_mysql(allergen_id)
    return render_template("editallergen.html", allergen=the_allergen)
    
#Delete allergen from database    
@app.route('/delete_allergen/<allergen_id>')
def delete_allergen(allergen_id):
    if database == "mongo":
        mongo.db.allergens.remove({'_id': ObjectId(allergen_id)})
    elif database == "mysql":
        delete_allergen_mysql(allergen_id)
    return redirect(url_for('get_allergens'))
 
#Update allergen in database
@app.route('/update_allergen/<allergen_id>', methods=['POST'])
def update_allergen(allergen_id):
    if database == "mongo":
        new_allergen = create_allergen()
        mongo.db.allergens.update( {'_id': ObjectId(allergen_id)},
                             new_allergen)
    elif database == "mysql":
        update_allergen_mysql(allergen_id)
    return redirect(url_for('get_allergens'))

#Increase the upvotes by clicking on the thumbs up button
@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    if database == "mongo":
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, { "$inc" :{'upvotes': 1}})
    elif database == "mysql":
        upvote_mysql(recipe_id)
    return redirect(url_for('get_recipes'))

#Create a csv file from data in mongodb. Will make this for mysql soon.
@app.route('/write_csv')
def write_csv():
    cursor= mongo.db.recipes.find({}, {'_id':0,"username":1, "recipe_name":1, "author":1, "prep_time":1, "cook_time":1, "upvotes": 1, "cuisine_name":1, "allergens":1, "country":1})
    with open(data_file, "w+") as outfile:
        fields = ["username", "recipe_name", "author", "prep_time", "cook_time","upvotes","cuisine_name","allergens", "country"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)
    return render_template("statistics.html")

#Will display statistics in dc d3 format pulled from csv created above.    
@app.route('/display_stats')
def display_stats():
    return render_template("statistics.html")



    
if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)