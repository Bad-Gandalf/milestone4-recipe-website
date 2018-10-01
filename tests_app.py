from app import app
import unittest
from flask import Flask, session, url_for



"""These test should be run when the app is using mongodb as the database. 
The tests only cover pages that do not require a change to the database i.e create, update and delete."""

class FlaskTestCase(unittest.TestCase):
    """These tests check for a recipe in the db already 'Jamaican Rum Truffles' """
    def test_index(self):
        # The homepage should have a list of recipes and this partiular recipe should be there. 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
    
    
    def test_recipe_description(self): 
        # Find the recipe description page for a specific recipe
        tester = app.test_client(self)
        response = tester.get('/recipe/{}'.format("5bae859ae6ca9599a3f58915"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Omit the rum for the teetotallers" in response.data)
        
    def test_search_recipes(self):
        # Test the search recipe page is working
        tester = app.test_client(self)
        response = tester.get('/search_recipes', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Ingredient" in response.data)
        self.assertTrue(b"Search Recipe" in response.data)
        
    def test_search_by_recipe(self):
        # Test that the search by recipe function is working and the correct recipe is returned. 
        tester = app.test_client(self)
        response = tester.post('/find_recipe_by_name', data=dict(recipe_name="truffles"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data)
        
    def test_search_by_cuisine(self):
        # Test that the search by cuisine function is working
        tester = app.test_client(self)
        response = tester.post('/find_recipe_cuisine_name', data=dict(cuisine_name="Carribean"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data) 
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
        
    def test_search_by_allergen(self):
        # Test that the search by allergen function is working
        tester = app.test_client(self)
        response = tester.post('/find_recipe_allergen_name', data=dict(allergens="Milk"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data) 
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
       
    def test_search_by_ingredient(self):
        # Test that search by ingredient function is working
        tester = app.test_client(self)
        response = tester.post('/find_recipe_by_ingredient', data=dict(ingredient_name="chocolate"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lorraine Pascale" in response.data)
        self.assertTrue(b"Jamaican Rum Truffles" in response.data)
        
    def test_add_recipe(self):
        # Test page for adding a new recipe loads
        tester = app.test_client(self)
        response = tester.get('/add_recipe', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Add Recipe" in response.data)
        self.assertTrue(b"Choose Allergens" in response.data)
        
        
    def test_add_country(self):
        # Test page for adding a new country loads
        tester = app.test_client(self)
        response = tester.get('/add_country', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Country Name" in response.data)
        
    def test_add_cuisine(self):
        # Test page for adding a new cuisine loads
        tester = app.test_client(self)
        response = tester.get('/add_cuisine', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Cuisine Description" in response.data)
        
    def test_add_allergen(self):
        # Test page for adding a new allergen loads
        tester = app.test_client(self)
        response = tester.get('/add_allergen', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Allergen Description" in response.data)
        
        
    def test_get_cuisines(self):
        # Test page for adding a new allergen loads
        tester = app.test_client(self)
        response = tester.get('/get_cuisines', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"African" in response.data)
        
    def test_get_countries(self):
        # Test Page for country list retrieval loads
        tester = app.test_client(self)
        response = tester.get('/get_countries', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Afghanistan" in response.data)
        
    def test_get_allergens(self):
        # Test Page for allergen list retrieval loads
        tester = app.test_client(self)
        response = tester.get('/get_allergens', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lupin" in response.data)
        
    def test_display_stats(self):
        # Test page for statistics loads
        tester = app.test_client(self)
        response = tester.get('/display_stats', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Statistics Taken From Recipe Database" in response.data)
        
    def test_edit_recipe(self):
        # Test Edit Recipe page, that it loads the specific information about said recipe to be edited.
        tester = app.test_client(self)
        response = tester.get('/edit_recipe/{}'.format("5bae859ae6ca9599a3f58915"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"walnut sized pieces" in response.data)
        self.assertTrue(b"Edit Recipe" in response.data)
        
    def test_edit_cuisine(self):
        # Test Edit Cuisine page, that it loads the specific information about said cuisine to be edited.
        tester = app.test_client(self)
        response = tester.get('/edit_cuisine/{}'.format("5afafe86e6ca956704d2e058"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Beat the takeaway with recipes from Chinese cookery master Ken Hom and other BBC chefs" in response.data)
        self.assertTrue(b"Edit Cuisine" in response.data)    
        
    def test_edit_country(self):
        # Test Edit Country page, that it loads the specific information about said country to be edited.
        tester = app.test_client(self)
        response = tester.get('/edit_country/{}'.format("5afebbb4e6ca95d972f37d9d"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Afghanistan" in response.data)
        self.assertTrue(b"Edit Country" in response.data)
        
    def test_edit_allergen(self):
        # Test Edit Allergen page, that it loads the specific information about said allergen to be edited.
        tester = app.test_client(self)
        response = tester.get('/edit_allergen/{}'.format("5af3200cf36d2856a8eea643"), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Edit Allergen" in response.data)
        self.assertTrue(b"This includes celery stalks" in response.data)
        
        
    

        
        
if __name__ == '__main__':
    unittest.main()