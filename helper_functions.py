from flask import Flask, request
from flask_pymongo import PyMongo, pymongo
import csv

app = Flask(__name__)
mongo = PyMongo(app)


#This function is used to find what page number the user is currently on in order to help paginate list of results.        
def get_page():
    return request.args.get('page', 1, type=int) #Be part of a cntroller class

#This function will take the query, page number the user is currently on and the 
#number of results wanted per page and slice the list of query results accordingly.
def paginate_list(query, page_number, per_page):
    array = [item for item in query]
    paginated_array = array[((page_number*per_page)-per_page):(page_number*per_page)]
    return paginated_array

#This is a function to create a new recipe from user inputs. This cuts down on repetitive 
#code dramatically. It returns an object suitable for insertion in mongodb i.e vars(recipe)
def create_recipe():#Should be a method of Recipe controller class
    recipe = dict(username=request.form['username'].strip(), recipe_name=request.form['recipe_name'].strip().title(), 
                    author= request.form['author'].strip().title(), prep_time=request.form['prep_time'].strip(), 
                    cook_time=request.form['cook_time'].strip(), servings=request.form['servings'].strip(),
                    recipe_description=request.form['recipe_description'].strip(),
                        cuisine_name=request.form['cuisine_name'], ingredients=request.form['ingredients'].strip(),
                        method=request.form['method'].strip(), allergens=request.form.getlist('allergens'), 
                        country=request.form["country"])
    return recipe


#This is a function to create a new cuisine from user inputs. This cuts down on repetitive 
#code dramatically.                        
def create_cuisine():
    cuisine = dict(cuisine_name=request.form['cuisine_name'].title(), cuisine_description=request.form['cuisine_description'])
    return cuisine

#This is a function to create a new allergen from user inputs. This cuts down on repetitive 
#code dramatically.    
def create_allergen():
    allergen = dict(allergen_name=request.form['allergen_name'].title(), 
                    allergen_description=request.form['allergen_description'])
    return allergen

#This is a function to create a new country from user inputs. This cuts down on repetitive 
#code dramatically.    
def create_country():
    country= dict(country_name=request.form["country"].title())
    return country
    
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
       
def write_to_csv(data_file, cursor):
    with open(data_file, "w+") as outfile:
        fields = ["username", "recipe_name", "author", "prep_time", "cook_time","upvotes","cuisine_name","country"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)