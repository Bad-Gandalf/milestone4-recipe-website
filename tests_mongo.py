from app import app
import unittest
from flask import Flask, session, url_for
from mysql_from_python import get_most_recent_recipe_id


class FlaskTestCase(unittest.TestCase):
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
    
    
    def test_recipe_description(self): #
        tester = app.test_client(self)
        response = tester.get('/recipe/{}'.format("5bae859ae6ca9599a3f58915"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Omit the rum for the teetotallers" in response.data)
        
    def test_search_recipes(self):
        tester = app.test_client(self)
        response = tester.get('/search_recipes', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Ingredient" in response.data)
        self.assertTrue(b"Search Recipe" in response.data)
        
    def test_search_by_recipe(self):   
        tester = app.test_client(self)
        response = tester.post('/find_recipe_by_name', data=dict(recipe_name="truffles"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data)
        
    def test_search_by_cuisine(self):   
        tester = app.test_client(self)
        response = tester.post('/find_recipe_cuisine_name', data=dict(cuisine_name="Carribean"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data) 
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
        
    def test_search_by_allergen(self): # Only mysql
        tester = app.test_client(self)
        response = tester.post('/find_recipe_allergen_name', data=dict(allergens="Milk"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data) 
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
       
    def test_search_by_ingredient(self):  
        tester = app.test_client(self)
        response = tester.post('/find_recipe_by_ingredient', data=dict(ingredient_name="chocolate"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data)
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
        
    def test_add_recipe(self):
        tester = app.test_client(self)
        response = tester.get('/add_recipe', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Add Recipe" in response.data)
        self.assertTrue(b"Choose Allergens" in response.data)
        
        
    def test_add_country(self):
        tester = app.test_client(self)
        response = tester.get('/add_country', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Country Name" in response.data)
        
    def test_add_cuisine(self):
        tester = app.test_client(self)
        response = tester.get('/add_cuisine', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Cuisine Description" in response.data)
        
    def test_add_allergen(self):
        tester = app.test_client(self)
        response = tester.get('/add_allergen', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Allergen Description" in response.data)
        
        
    def test_get_cuisines(self):
        tester = app.test_client(self)
        response = tester.get('/get_cuisines', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"African" in response.data)
        
    def test_get_countries(self):
        tester = app.test_client(self)
        response = tester.get('/get_countries', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Afghanistan" in response.data)
        
    def test_get_allergens(self):
        tester = app.test_client(self)
        response = tester.get('/get_allergens', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lupin" in response.data)
        
    def test_display_stats(self):
        tester = app.test_client(self)
        response = tester.get('/display_stats', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Statistics Taken From Recipe Database" in response.data)
        

        
        
if __name__ == '__main__':
    unittest.main()