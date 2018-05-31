from flask import Flask, request
from flask_pymongo import PyMongo, pymongo
import csv

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'pat_doc_recipedb'
app.config["MONGO_URI"] = 'mongodb://admin:1Pfhr39Hdi4@ds119060.mlab.com:19060/pat_doc_recipedb'
mongo = PyMongo(app)
#Class for a new recipe when inserting into mongodb.
class Recipe(object):
    upvotes = 0
    def __init__(self, username, recipe_name, author, prep_time, cook_time, servings, recipe_description, cuisine_name, ingredients, method, allergens, country):
        self.username = username
        self.recipe_name = recipe_name
        self.author = author
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.recipe_description = recipe_description
        self.cuisine_name = cuisine_name
        self.ingredients = ingredients
        self.method = method
        self.allergens = allergens
        self.country = country

#Class for a new user when inserting into mongodb. (Currently unused)        
class User(object):
    def __init__(self, username, country):
        self.username = username
        self.country = country

#Class for a new cuisine when inserting into mongodb
class Cuisine(object):
    def __init__(self, cuisine_name, cuisine_description):
        self.cuisine_name = cuisine_name
        self.cuisine_description = cuisine_description

#Class for a new allergen when inserting into mongodb        
class Allergen(object):
    def __init__(self, allergen_name, allergen_description):
        self.allergen_name = allergen_name
        self.allergen_description = allergen_description

#Class for a new country when inserting into mongodb        
class Country(object):
    def __init__(self, country_name):
        self.country_name = country_name

#This function is used to find what page number the user is currently on in order to help paginate list of results.        
def get_page():
    return request.args.get('page', 1, type=int)

#This function will take the query, page number the user is currently on and the 
#number of results wanted per page and slice the list of query results accordingly.
def paginate_list(query, page_number, per_page):
    array = [item for item in query]
    paginated_array = array[((page_number*per_page)-per_page):(page_number*per_page)]
    return paginated_array

#This is a function to create a new recipe from user inputs. This cuts down on repetitive 
#code dramatically. It returns an object suitable for insertion in mongodb i.e vars(recipe)
def create_recipe():
    recipe = Recipe(request.form['username'].strip(), request.form['recipe_name'].strip().title(), request.form['author'].strip().title(),
                        request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                        request.form['servings'].strip(),request.form['recipe_description'].strip(),
                        request.form['cuisine_name'], request.form['ingredients'].strip(),
                        request.form['method'].strip(), request.form.getlist('allergens'), request.form["country"])
    return vars(recipe)

#This is a function to create a new cuisine from user inputs. This cuts down on repetitive 
#code dramatically.                        
def create_cuisine():
    cuisine = Cuisine(request.form['cuisine_name'].title(), request.form['cuisine_description'])
    return vars(cuisine)

#This is a function to create a new allergen from user inputs. This cuts down on repetitive 
#code dramatically.    
def create_allergen():
    allergen = Allergen(request.form['allergen_name'].title(), request.form['allergen_description'])
    return vars(allergen)

#This is a function to create a new country from user inputs. This cuts down on repetitive 
#code dramatically.    
def create_country():
    country= Country(request.form["country_name"].title())
    return vars(country)
    
# Find allergen data for mining and display statistically
def get_allergens_data():
    cursor_allergens= mongo.db.recipes.find({}, {'_id':0, "allergens":1})
    allergen_list = []
    for i in cursor_allergens:
        for j in (i["allergens"]):
            if j != "":
                allergen_list.append([j])
    return allergen_list

# Write allergen data to csv for displaying statistics.    
def write_allergens_csv_mongo(allergen_list, data_file):
    with open(data_file, "w+") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['allergen_name'])
        for x in allergen_list:
            writer.writerow(x)
        