import os
import pymysql

from flask import request

username = os.getenv('C9_USER')
connection = pymysql.connect(host="localhost",
                            user=username,
                            password = '',
                            db='recipes')

def get_allergens_for_recipe_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT A.allergen_name FROM recipe INNER JOIN (SELECT recipe_allergen.recipeID, GROUP_CONCAT(allergens.allergen_name SEPARATOR ',') AS allergen_name FROM recipe_allergen INNER JOIN allergens ON allergens._id = recipe_allergen.allergenID GROUP BY recipe_allergen.allergenID) AS A ON recipe._id = A.recipeID where recipe._id = %s;"
        cursor.execute(sql, recipe_id)
        result = cursor.fetchall()
        result_list = map(lambda d: d['allergen_name'], result)
        return result_list


def get_recipes_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe ORDER BY upvotes DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            i["allergens"] = get_allergens_for_recipe_mysql(i["_id"])
        return result

def insert_recipe_mysql():
    with connection.cursor() as cursor:
        row = (request.form['recipe_name'].strip().title(), request.form['recipe_description'].strip(),
                        request.form['ingredients'].strip(), request.form['author'].strip().title(), 
                        request.form['username'].strip(), request.form['cuisine_name'], 
                        request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                        request.form['method'].strip(), request.form['servings'].strip(),
                        request.form["country"])
                        
        cursor.execute("INSERT INTO recipe (recipe_name, recipe_description, ingredients, author, username, cuisine_name, prep_time, cook_time, method, servings, country) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s);", row)
        connection.commit()

def find_recipe_by_id_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe WHERE _id = %s;"
        cursor.execute(sql, recipe_id)
        result = cursor.fetchall()
        for i in result:
            return i
        
def update_recipe_mysql(recipe_id):
    with connection.cursor() as cursor:
        row = (request.form['recipe_name'].strip().title(), request.form['recipe_description'].strip(),
                        request.form['ingredients'].strip(), request.form['author'].strip().title(), 
                        request.form['username'].strip(), request.form['cuisine_name'], 
                        request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                        request.form['method'].strip(), request.form['servings'].strip(),
                        request.form["country"], int(recipe_id))
        
        cursor.execute("UPDATE recipe SET recipe_name = %s, recipe_description = %s, ingredients = %s, author = %s, username = %s, cuisine_name = %s, prep_time = %s, cook_time = %s, method = %s, servings = %s, country = %s WHERE _id=%s;", row)    
        connection.commit()
    
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
        
        

    
#Country functions

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



#Search by ** functions       

def find_recipe_by_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["recipe_name"]
        sql = "SELECT * FROM recipe WHERE recipe_name RLIKE %s ORDER BY upvotes DESC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        return result
        

        
def find_recipe_by_cuisine_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["cuisine_name"]
        sql = "SELECT * FROM recipe WHERE cuisine_name RLIKE %s ORDER BY recipe_name ASC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        return result

def find_recipe_allergen_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["allergen_name"]
        sql = "SELECT * FROM recipe WHERE allergen_name RLIKE %s ORDER BY recipe_name ASC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        return result
        
def find_recipe_by_ingredient_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["ingredient_name"]
        sql = "SELECT * FROM recipe WHERE ingredients RLIKE %s ORDER BY recipe_name ASC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        return result
        
#Upvotes        
def upvote_mysql(recipe_id):
    with connection.cursor() as cursor:
        sql ="UPDATE recipe SET upvotes = upvotes + 1 WHERE _id = %s"
        cursor.execute(sql, recipe_id)
        connection.commit()
        
