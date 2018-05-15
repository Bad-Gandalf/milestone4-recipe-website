from flask import request

class Recipe(object):
    upvotes = 0
    def __init__(self, username, recipe_name, author, prep_time, cook_time, servings, recipe_description, cuisine_name, ingredients, method, allergens):
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
        
class User(object):
    def __init__(self, username, first_name, last_name, country):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.country = country

class Cuisine(object):
    def __init__(self, cuisine_name, cuisine_description):
        self.cuisine_name = cuisine_name
        self.cuisine_description = cuisine_description
        
class Allergen(object):
    def __init__(self, allergen_name, allergen_description):
        self.allergen_name = allergen_name
        self.allergen_description = allergen_description
        
class Country(object):
    def __init__(self, country_name, country_description):
        self.country_name = country_name
        self.country_description = country_description
        
        

def get_page():
    return request.args.get('page', 1, type=int)

def paginate_list(query, page_number, per_page):
    array = [item for item in query]
    paginated_array = array[((page_number*per_page)-per_page):(page_number*per_page)]
    return paginated_array
    
def create_recipe():
    recipe = Recipe(request.form['username'], request.form['recipe_name'], request.form['author'],
                        request.form['prep_time'], request.form['cook_time'], 
                        request.form['servings'],request.form['recipe_description'],
                        request.form['cuisine_name'], request.form['ingredients'],
                        request.form['method'], request.form.getlist('allergens'))
    return vars(recipe)
                        
def create_cuisine():
    cuisine = Cuisine(request.form['cuisine_name'], request.form['cuisine_description'])
    return vars(cuisine)
    
def create_allergen():
    allergen = Allergen(request.form['allergen_name'], request.form['allergen_description'])
    return vars(allergen)