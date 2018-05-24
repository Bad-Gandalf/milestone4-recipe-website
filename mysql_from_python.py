import os
import pymysql

from flask import request

username = os.getenv('C9_USER')
connection = pymysql.connect(host="localhost",
                            user=username,
                            password = '',
                            db='recipes')




def get_recipes_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe ORDER BY upvotes DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    
        
def upvote_mysql(recipe_id):
    with connection.cursor() as cursor:
        sql ="UPDATE recipe SET upvotes = upvotes + 1 WHERE _id = %s"
        cursor.execute(sql, recipe_id)
        connection.commit()

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
        
        
def find_recipe_by_name_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        search_term = request.form["recipe_name"]
        sql = "SELECT * FROM recipe WHERE recipe_name RLIKE %s ORDER BY upvotes DESC;"
        cursor.execute(sql, search_term)
        result = cursor.fetchall()
        return result
        
def find_recipe_by_id_mysql(recipe_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM recipe WHERE _id = %s;"
        cursor.execute(sql, recipe_id)
        result = cursor.fetchall()
        for i in result:
            return i
        
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
    
    

def get_allergens_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM allergens ORDER BY allergen_name ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def get_cuisines_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM cuisines ORDER BY cuisine_name ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
        
def insert_allergen_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        row = (request.form["allergen_name"], request.form["allergen_description"])
        sql = "INSERT INTO allergens (allergen_name, allergen_description) VALUES (%s, %s);"
        cursor.execute(sql, row)
        connection.commit()
        
def insert_cuisine_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        row = (request.form["cuisine_name"], request.form["cuisine_description"])
        sql = "INSERT INTO cuisines (cuisine_name, cuisine_description) VALUES (%s, %s);"
        cursor.execute(sql, row)
        connection.commit()
    