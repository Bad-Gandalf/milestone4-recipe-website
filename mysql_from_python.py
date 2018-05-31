import os
import pymysql
import csv
from flask import request

username = os.getenv('C9_USER')
connection = pymysql.connect(host="localhost",
                            user=username,
                            password = '',
                            db='recipes')

#This will query the many-to-many table and link recipeID to allergenIDs
def get_existing_allergens_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ="SELECT a._id, a.allergen_name FROM recipe_allergen AS m INNER JOIN allergens AS a ON m.allergenID = a._id WHERE recipeID=%s;"
        cursor.execute(sql, recipe_id)
        result = cursor.fetchall()
        return result

#This function will get the recipes from mysql and then use the previous two 
#functions to attach the allergens to the dictionary to be displayed to the user. 
def get_recipes_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe ORDER BY upvotes DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            i["allergens"] = get_existing_allergens_mysql(i["_id"])
        print (result)
        return result

#Insert a recipe taken from the form and insert it into mysql. Upvotes are set to 0
#automatically.
def insert_recipe_mysql():
    with connection.cursor() as cursor:
        row = (request.form['recipe_name'].strip().title(), request.form['recipe_description'].strip(),
                        request.form['ingredients'].strip(), request.form['author'].strip().title(), 
                        request.form['username'].strip(), request.form['cuisine_name'], 
                        request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                        request.form['method'].strip(), request.form['servings'].strip(),
                        request.form["country"], 0)
        
        sql = """INSERT INTO recipe (recipe_name, recipe_description, 
                ingredients, author, username, cuisine_name, prep_time, 
                cook_time, method, servings, country, upvotes) 
                VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);"""               
        cursor.execute(sql, row)
        connection.commit()

#This function will find the most recent created recipe ID, directly after the
#recipe has been inserted. This allows us to correctly add the allergens to 
# the many to many table.
def get_most_recent_recipe_id(): 
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT MAX(_id) FROM recipe;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            allergen_id = i["MAX(_id)"]
        return allergen_id

#Inserting allergen_ID and recipe_ID into many-to-many table. It takes the recipe_id
#returned from the previous function as an argument
def insert_allergens_to_recipe(recipe_id):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `recipe_allergen` (recipeID, allergenID) VALUES (%s, %s)"
        allergen_list = request.form.getlist('allergens')
        print(allergen_list)
        for allergen in allergen_list:
            row = (recipe_id, allergen)
            cursor.execute(sql, row)
        connection.commit()

#Delete rows from many-to-many table where recipe_id is ...        
def delete_recipe_allergen_row(recipe_id):
     with connection.cursor() as cursor:
        sql = "DELETE FROM `recipe_allergen` WHERE recipeID=%s;"
        row = (recipe_id)
        cursor.execute(sql, row)
        connection.commit()

#A combination of the previous to functions to update a many-to-many table correctly.
def change_allergens_mysql(recipe_id):
    delete_recipe_allergen_row(recipe_id)
    insert_allergens_to_recipe(recipe_id)
    
#Find recipe by its id, its delivered in a list so it extracts the one dictionary
#rather than a list of one dictionary.
def find_recipe_by_id_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe WHERE _id = %s;"
        cursor.execute(sql, recipe_id)
        result = cursor.fetchall()
        for i in result:
            return i
            
#Updates recipe when given recipe_id
def update_recipe_mysql(recipe_id):
    with connection.cursor() as cursor:
        row = (request.form['recipe_name'].strip().title(), request.form['recipe_description'].strip(),
                        request.form['ingredients'].strip(), request.form['author'].strip().title(), 
                        request.form['username'].strip(), request.form['cuisine_name'], 
                        request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                        request.form['method'].strip(), request.form['servings'].strip(),
                        request.form["country"], int(recipe_id))
        sql = """UPDATE recipe SET recipe_name = %s, recipe_description = %s, 
                ingredients = %s, author = %s, username = %s, cuisine_name = %s, 
                prep_time = %s, cook_time = %s, method = %s, servings = %s, 
                country = %s WHERE _id=%s;"""
        
        cursor.execute(sql, row)    
        connection.commit()

#This updates many-to-many allergen table when recipe is updated.
def update_recipe_allergens(recipe_id):
    with connection.cursor() as cursor:        
        allergen_list = request.form.getlist('allergens')
        sql2 = "INSERT INTO `recipe_allergen` (recipeID, allergenID) VALUES (%s, %s)"
        for allergen in allergen_list:
            row2 = (recipe_id, allergen)
            cursor.execute(sql2, row2)
        connection.commit()

#Country functions    
def delete_recipe_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ="DELETE FROM recipe WHERE _id = %s"
        cursor.execute(sql, recipe_id)
        connection.commit()

def get_countries_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM country ORDER BY country_name ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
        
def insert_country_mysql():
    with connection.cursor() as cursor:
        row = (request.form["country"])
        cursor.execute("INSERT INTO country (country_name) VALUES (%s);", row)
        connection.commit() 

def get_country_mysql_by_id(country_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM country WHERE _id=%s;"
        cursor.execute(sql, country_id)
        result = cursor.fetchall()
        for i in result:
            return i 
        
def delete_country_mysql(country_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ="DELETE FROM country WHERE _id = %s"
        cursor.execute(sql, country_id)
        connection.commit()

def update_country_mysql(country_id):
    with connection.cursor() as cursor:
        row = (request.form['country_name'], country_id)
        cursor.execute("UPDATE country SET country_name = %s WHERE _id=%s;", row)    
        connection.commit()

#Cuisine Functions
def get_cuisines_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM cuisines ORDER BY cuisine_name ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def insert_cuisine_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        row = (request.form["cuisine_name"], request.form["cuisine_description"])
        sql = "INSERT INTO cuisines (cuisine_name, cuisine_description) VALUES (%s, %s);"
        cursor.execute(sql, row)
        connection.commit()
        
def get_cuisine_by_id_mysql(cuisine_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM cuisines WHERE _id = %s;"
        cursor.execute(sql, cuisine_id)
        result = cursor.fetchall()
        for i in result:
            return i
    
def update_cuisine_mysql(cuisine_id):
    with connection.cursor() as cursor:
        row = (request.form['cuisine_name'], request.form['cuisine_description'], int(cuisine_id))
        cursor.execute("UPDATE cuisines SET cuisine_name = %s, cuisine_description = %s WHERE _id=%s;", row)    
        connection.commit()
        
def delete_cuisine_mysql(cuisine_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ="DELETE FROM cuisines WHERE _id = %s"
        cursor.execute(sql, cuisine_id)
        connection.commit()

#Allergen Functions

def get_allergens_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM allergens ORDER BY allergen_name ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_allergen_by_id_mysql(allergen_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM allergens WHERE _id = %s;"
        cursor.execute(sql, allergen_id)
        result = cursor.fetchall()
        for i in result:
            return i

def insert_allergen_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        row = (request.form["allergen_name"], request.form["allergen_description"])
        sql = "INSERT INTO allergens (allergen_name, allergen_description) VALUES (%s, %s);"
        cursor.execute(sql, row)
        connection.commit()
        
def delete_recipe_allergens(recipe_id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM `recipe_allergen` WHERE recipeID=%s;"
        row = (recipe_id)
        cursor.execute(sql, row)
        connection.commit()
    

def update_allergen_mysql(allergen_id):
    with connection.cursor() as cursor:
        row = (request.form['allergen_name'], request.form['allergen_description'], int(allergen_id))
        cursor.execute("UPDATE allergens SET allergen_name = %s, allergen_description = %s WHERE _id=%s;", row)    
        connection.commit()

def delete_allergen_mysql(allergen_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ="DELETE FROM allergens WHERE _id = %s"
        cursor.execute(sql, allergen_id)
        connection.commit()        

#Search by functions       

def find_recipe_by_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["recipe_name"]
        sql = "SELECT * FROM recipe WHERE recipe_name RLIKE %s ORDER BY upvotes DESC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        for i in result:
            i["allergens"] = get_existing_allergens_mysql(i["_id"])
        return result
        

        
def find_recipe_by_cuisine_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["cuisine_name"]
        sql = "SELECT * FROM recipe WHERE cuisine_name RLIKE %s ORDER BY recipe_name ASC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        for i in result:
            i["allergens"] = get_existing_allergens_mysql(i["_id"])
        return result
        
#Function finds all recipe_ids based on the lalegren_ids they are connected with in 
# many-to-many table (recipe_allergen).
def find_recipe_allergen_name_mysql():
    recipe_ids = []
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["allergens"]
        sql = "SELECT * FROM recipe_allergen WHERE allergenID=%s;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        for i in result:
            recipe_ids.append(i["recipeID"])
    return recipe_ids

#This returns a list of the recipes that have the ids supplied by the previous 
#function
def find_recipes_by_allergens():
    found_recipes = []
    all_recipes = get_recipes_mysql()
    recipe_ids = find_recipe_allergen_name_mysql()
    for i in recipe_ids:
         for j in all_recipes:
             if i == j["_id"]:
                 found_recipes.append(j)
    return found_recipes

    
#Partial text search for ingredient and returns matching recipes
def find_recipe_by_ingredient_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["ingredient_name"]
        sql = "SELECT * FROM recipe WHERE ingredients RLIKE %s ORDER BY recipe_name ASC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        for i in result:
            i["allergens"] = get_existing_allergens_mysql(i["_id"])
        return result
        
#Upvotes        
def upvote_mysql(recipe_id):
    with connection.cursor() as cursor:
        sql ="UPDATE recipe SET upvotes = upvotes + 1 WHERE _id = %s"
        cursor.execute(sql, recipe_id)
        connection.commit()
        
def get_data_for_csv_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT `username`, `recipe_name`, `author`, `prep_time`, `cook_time`,`upvotes`,`cuisine_name`,`country` FROM recipe;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
        
def write_to_csv(data_file, cursor):
    with open(data_file, "w+") as outfile:
        fields = ["username", "recipe_name", "author", "prep_time", "cook_time","upvotes","cuisine_name","country"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)    
            
def get_allergen_data_csv_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT m.allergenID, a.allergen_name FROM recipe_allergen AS m INNER JOIN allergens AS a ON m.allergenID = a._id;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
        
def write_allergens_to_csv(data_file, cursor):
    with open(data_file, "w+") as outfile:
        fields = ["allergenID", "allergen_name"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)
    