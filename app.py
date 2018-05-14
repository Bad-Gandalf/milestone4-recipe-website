import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from classes import *

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'pat_doc_recipedb'
app.config["MONGO_URI"] = 'mongodb://admin:1Pfhr39Hdi4@ds119060.mlab.com:19060/pat_doc_recipedb'

mongo = PyMongo(app)



@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    _recipes=mongo.db.recipes.find()
    recipe_list = [recipe for recipe in _recipes]
    return render_template("recipe.html", recipes=recipe_list)
    
@app.route('/search_recipes')
def search_recipes():
    _recipes = mongo.db.recipes.find()
    recipe_list = [recipe for recipe in _recipes]
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template("searchrecipe.html", recipes = recipe_list, allergens = allergen_list, cuisines = cuisine_list)
    
@app.route('/find_recipe_by_name', methods=["POST"])
def find_recipe_by_name():
    search_term = {"recipe_name": request.form['recipe_name']}
    _recipes = mongo.db.recipes.find(search_term)
    matching_recipes = [recipe for recipe in _recipes]
    return render_template("recipesfound.html", recipes=matching_recipes)
    
@app.route('/find_recipe_cuisine_name', methods=["POST"])
def find_recipe_cuisine_name():
    search_term = {"cuisine_name": request.form['cuisine_name']}
    _recipes = mongo.db.recipes.find(search_term)
    matching_recipes = [recipe for recipe in _recipes]
    return render_template("recipesfound.html", recipes=matching_recipes)
    
@app.route('/find_recipe_allergen_name', methods=["POST"])
def find_recipe_allergen_name():
    search_term = {"allergens": request.form['allergens']}
    _recipes = mongo.db.recipes.find(search_term)
    matching_recipes = [recipe for recipe in _recipes]
    return render_template("recipesfound.html", recipes=matching_recipes)

@app.route("/add_recipe")
def add_recipe():
    _recipes = mongo.db.recipes.find()
    recipe_list = [recipe for recipe in _recipes]
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template("addrecipe.html", recipes = recipe_list, allergens = allergen_list, cuisines = cuisine_list)

@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    new_recipe = Recipe(request.form['recipe_name'], request.form['author'],
                        request.form['prep_time'], request.form['cook_time'], 
                        request.form['servings'],request.form['recipe_description'],
                        request.form['cuisine_name'], request.form['ingredients'],
                        request.form['method'], request.form.getlist('allergens'))
                        
                        
    recipes.insert_one(vars(new_recipe))
    print(vars(new_recipe))
    return redirect(url_for('add_recipe'))    
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes = mongo.db.recipes.find()
    cuisines = mongo.db.cuisines.find()
    allergens = mongo.db.allergens.find()
    return render_template("editrecipe.html", recipe=the_recipe, recipes=all_recipes, cuisines=cuisines, allergens=allergens)
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    updated_recipe = Recipe(request.form['recipe_name'], request.form['author'],
                        request.form['prep_time'], request.form['cook_time'], 
                        request.form['servings'],request.form['recipe_description'],
                        request.form['cuisine_name'], request.form['ingredients'],
                        request.form['method'], request.form.getlist('allergens'))
    recipes.update({'_id': ObjectId(recipe_id)}, vars(updated_recipe))
    return redirect(url_for('get_recipes'))
    
@app.route('/get_cuisines')
def get_cuisines():
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    return render_template('cuisine.html', cuisines=cuisine_list)
    

@app.route("/add_cuisine")
def add_cuisine():
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    return render_template("addcuisine.html", cuisines = cuisine_list)    

@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    new_cuisine = Cuisine(request.form['cuisine_name'], request.form['cuisine_description'])
    print(vars(new_recipe))
    cuisines.insert_one(vars(new_cuisine))
    return redirect(url_for('get_cuisines')) 
    
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    cuisines = mongo.db.cuisines.find()
    return render_template("editcuisine.html", cuisines=cuisines, cuisine=the_cuisine)
    
    
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))
 
 
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    new_cuisine = Cuisine(request.form['cuisine_name'], request.form['cuisine_description'])
    mongo.db.cuisines.update( {'_id': ObjectId(cuisine_id)},
       vars(new_cuisine))
    return redirect(url_for('get_cuisines'))
    
@app.route('/get_allergens')
def get_allergens():
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template('allergen.html', allergens=allergen_list)
    

@app.route("/add_allergen")
def add_allergen():
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template("addallergen.html", allergens = allergen_list)    

@app.route('/insert_allergen', methods=['POST'])
def insert_allergen():
    allergens = mongo.db.allergens
    new_allergen = Allergen(request.form['allergen_name'], request.form['allergen_description'])
    print(vars(new_allergen))
    allergens.insert_one(vars(new_allergen))
    return redirect(url_for('get_allergens')) 
    
@app.route('/edit_allergen/<allergen_id>')
def edit_allergen(allergen_id):
    the_allergen = mongo.db.allergens.find_one({"_id": ObjectId(allergen_id)})
    allergens = mongo.db.allergens.find()
    return render_template("editallergen.html", allergens=allergens, allergen=the_allergen)
    
    
@app.route('/delete_allergen/<allergen_id>')
def delete_allergen(allergen_id):
    mongo.db.allergens.remove({'_id': ObjectId(allergen_id)})
    return redirect(url_for('get_allergens'))
 
 
@app.route('/update_allergen/<allergen_id>', methods=['POST'])
def update_allergen(allergen_id):
    new_allergen = Allergen(request.form['allergen_name'], request.form['allergen_description'])
    mongo.db.allergens.update( {'_id': ObjectId(allergen_id)},
                             vars(new_allergen))
    return redirect(url_for('get_allergens'))


@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    upvotes = recipe.get("upvotes")
    if upvotes is None:
        mongo.db.recipes.insert({"_id": ObjectId(recipe_id), "upvotes": upvotes})
    else:    
        int(upvotes)
        upvotes += 1
        
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id), 'upvotes': upvotes})
    print (upvotes)
    return redirect(url_for('get_recipes'))



















"""@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    _category=mongo.db.categories.find_one({'_id':ObjectId(category_id)})
    return render_template("editcategory.html", category=_category)

    

    

    
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')
    
"""
    
if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)