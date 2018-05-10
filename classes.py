class Recipe(object):
    def __init__(self, recipe_name, author, prep_time, cook_time, servings, recipe_description, cuisine_name, ingredients, method, allergens):
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
        
class Allergens(object):
    def __init__(self, allergen_name, allergen_description):
        self.allergen_name = allergen_name
        self.allergen_description = allergen_description
        
class Country(object):
    def __init__(self, country_name, country_description):
        self.country_name = country_name
        self.country_description = country_description
        
        
new_recipe = Recipe("poached egg", "George RR Martin", 1, 5, 1, "Poached egg on toast", "English", "Egg, bread, salt, pepper", "1.jfbkz 2.fbkzeun 3.feunkf", "Egg")
print(vars(new_recipe))
    