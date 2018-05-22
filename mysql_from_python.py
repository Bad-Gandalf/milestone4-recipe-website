import os
import pymysql

from flask import request

username = os.getenv('C9_USER')
connection = pymysql.connect(host="localhost",
                            user=username,
                            password = '',
                            db='Recipes')
def get_recipes_mysql():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM Recipe;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    

get_recipes_mysql()
    
"""try:
    with connection.cursor() as cursor:
        row1 = ("Gluten", "Wheat (such as spelt and Khorasan wheat/Kamut), rye, barley and oats is often found in foods containing flour, such as some types of baking powder, batter, breadcrumbs, bread, cakes, couscous, meat products, pasta, pastry, sauces, soups and fried foods which are dusted with flour.")
        row2 = ("Crustaceans", "Crabs, lobster, prawns and scampi are crustaceans. Shrimp paste, often used in Thai and south-east Asian curries or salads, is an ingredient to look out for.")
        row3 = ("Eggs", "Eggs are often found in cakes, some meat products, mayonnaise, mousses, pasta, quiche, sauces and pastries or foods brushed or glazed with egg.")
        row4 = ("Fish", "You will find this in some fish sauces, pizzas, relishes, salad dressings, stock cubes and Worcestershire sauce.")
        row5 = ("Lupin","Yes, lupin is a flower, but it is also found in flour! Lupin flour and seeds can be used in some types of bread, pastries and even in pasta.")
        row6 = ("Molluscs", "These include mussels, land snails, squid and whelks, but can also be commonly found in oyster sauce or as an ingredient in fish stews")
        row7 = ("Mustard", "Liquid mustard, mustard powder and mustard seeds fall into this category. This ingredient can also be found in breads, curries, marinades, meat products, salad dressings, sauces and soups.")
        row8 = ("Nuts",  "Not to be mistaken with peanuts (which are actually a legume and grow underground), this ingredient refers to nuts which grow on trees, like cashew nuts, almonds and hazelnuts. You can find nuts in breads, biscuits, crackers, desserts, nut powders (often used in Asian curries), stir-fried dishes, ice cream, marzipan (almond paste), nut oils and sauces.")
        row9 = ("Peanuts","Peanuts are actually a legume and grow underground, which is why it is sometimes called a groundnut. Peanuts are often used as an ingredient in biscuits, cakes, curries, desserts, sauces (such as satay sauce), as well as in groundnut oil and peanut flour.")
        row10 = ("Sesame Seeds", "These seeds can often be found in bread (sprinkled on hamburger buns for example), breadsticks, houmous, sesame oil and tahini. They are sometimes toasted and used in salads.")
        row11 = ("Soya", "Often found in bean curd, edamame beans, miso paste, textured soya protein, soya flour or tofu, soya is a staple ingredient in oriental food. It can also be found in desserts, ice cream, meat products, sauces and vegetarian products.")
        row12 = ("Sulphur Dioxide", "This is an ingredient often used in dried fruit such as raisins, dried apricots and prunes. You might also find it in meat products, soft drinks, vegetables as well as in wine and beer. If you have asthma, you have a higher risk of developing a reaction to sulphur dioxide.")
        row13 = ("Milk",  "Milk is a common ingredient in butter, cheese, cream, milk powders and yoghurt. It can also be found in foods brushed or glazed with milk, and in powdered soups and sauces.")
        
        cursor.execute("INSERT INTO Allergens (name, allergen_description) VALUES (%s, %s);", row13)
        connection.commit()
        
finally:
    connection.close()"""
    
def insert_recipe_mysql():   
    try:
        with connection.cursor() as cursor:
            row = (request.form['recipe_name'].strip().title(), request.form['recipe_description'].strip(),
                            request.form['ingredients'].strip(), request.form['author'].strip().title(), 
                            request.form['username'].strip(), request.form['cuisine_name'], 
                            request.form['prep_time'].strip(), request.form['cook_time'].strip(), 
                            request.form['method'].strip(), request.form['servings'].strip(),
                            request.form["country"], str(request.form.getlist('allergens')))
                            
            cursor.execute("INSERT INTO Recipe (recipe_name, recipe_description, ingredients, author, username, cuisine_name, prep_time, cook_time, method, servings, country, allergens) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);", row)
            connection.commit()
        
    finally:
        connection.close()
    
