# Code Institute - Milestone Project 4 - Recipe Manager
#### by Patrick Doherty

The brief I was given for this project was the following:

#### CREATE AN ONLINE COOKBOOK:

Create a web application that allows users to store and easily access cooking recipes
Put some effort into designing a database schema based on recipes, and any other related properties and entities (e.g. views, upvotes, ingredients, recipe authors, allergens, author’s country of origin, cuisine etc…). Make sure to put some thought into the relationships between them, and use either foreign keys (in the case of a relational database) or nesting (in the case of a document store) to connect these pieces of data
Create the backend code and frontend form to allow users to add new recipes to the site (at least a basic one, if you haven’t taken the frontend course)
Create the backend code to group and summarise the recipes on the site, based on their attributes such as cuisine, country of origin, allergens, ingredients, etc. and a frontend page to show this summary, and make the categories clickable to drill down into a filtered view based on that category. This frontend page can be as simple or as complex as you’d like; you can use a Python library such as matplotlib, or a JS library such as d3/dc (that you learned about if you took the frontend modules) for visualisation
Create the backend code to retrieve a list of recipes, filtered based on various criteria (e.g. allergens, cuisine, etc…) and order them based on some reasonable aspect (e.g. number of views or upvotes). Create a frontend page to display these, and to show some summary statistics around the list (e.g. number of matching recipes, number of new recipes. Optionally, add support for pagination, when the number of results is large
Create a detailed view for each recipes, that would just show all attributes for that recipe, and the full preparation instructions
Allow for editing and deleting of the recipe records, either on separate pages, or built into the list/detail pages
Optionally, you may choose to add basic user registration and authentication to the site. This can as simple as adding a username field to the recipe creation form, without a password (for this project only, this is not expected to be secure)

#### I completed this brief fully and used mongodb as the database. However on the suggestion of my mentor I did make an app that could switch between a mysql db and mongodb by changing one line of code. That can be found in "mysql/app_mongo_mysql.py".

## UX
#### User stories

1. Any user has full access to the site, there is no login to the site.
2. The user will immediately be presented with all the recipes (paginated to 10 a page).
3. They can click on a list tab and a small description will display below, they can also click on the title and be taken to a page detailing every aspect of the recipe. 
4. Any user can create create, update or delete any recipe currently. A user name is only requested when creating or editing a recipe, and this is just for record keeping. 
5. Any user can create, update or delete entries for Cuisines, Countries and Allergens also. No username is required for these entries.
6. To find a specific recipe a user can search by "recipe name", "cuisine", "country", "allergen" and "ingredient". Partial search works too. 
7. Users can also upvote recipes as many times as they wish, the recipes will be displayed from most to least upvoted. 
7. There is a statistics page displaying interactive charts that when clicked on will drill down to a filtered view based on that category. 
 

## Database Schema

My MongoDB database consists of 4 collections, one for each of the following:
- Recipes
- Cuisines
- Countries
- Allergens

The recipes collection will contain all information needed for one recipe including cuisines, countries and allergens.
The three other collections will provide options to select when a user is creating a new recipe, to give uniformity to the site. 

## Features

### Existing Features
- Simple recipe Manager App

### Potential future features
- Login authentication system
- Only creators of recipes can edit them
- Uploading pictures for the recipes, countries, allergens and cuisines.
- Adding a review system to each recipe, where other users can comment on their experience with the recipe.
- Limiting upvoting to one per user per recipe, and adding downvoting possibility. 


## Technologies used:
##### HTML - hypertext markup language
##### CSS - cascading style sheets 
##### Javascript - client side scripting language
##### Python - Programming Language
##### Git Bash & GitHub -for version control and backup of code
##### Bootstrap - A framework for developing responsive, mobile 1st websites.
##### Flask - python web framework
##### Postman - Postman helps you develop APIs faster
##### MongoDB - Non-relational database
##### MySQL - Relational database (not used in production site)

##### Libraries I needed to install
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation, and allow for AJAX requests.
- [crossfilter](https://github.com/crossfilter/crossfilter)
    - to parse and compare data
- [d3](https://d3js.org/)
    - to create charts from data
- [dc](https://dc-js.github.io/dc.js/)
    - to create charts from data
- [queue](https://github.com/d3/d3-queue)
    - This allows us to await collection of data before running scripts.


## Testing
 
### Automated testing


#### Test Suite
I have used unittests to check that the website was working. The only routes I could not unittest where create, update and delete entries. If I had to use flask with
mongo in the future I may use MockDB to test create update and delete. Theses tests can be seen in "tests_app.py". I had also tested the same for mysql routes and
they can be found in "/mysql/tests_mysql.py" In writing the unitttest I also used Postman to help me see what and how data needed to be sent to specific urls. The data I 
passed through, I knew was on the database already, such as recipe id. 

#### Manual testing

When building helper functions I would have to check if they were producing the correct results and this involved alot of reloading pages as assertion tests were not 
particularly suitable. I would also have to check the .csv files were being created properly and then adjust my functions to make it so. 

I tested create, update and delete for all entries in to the four collections; Recipes, cuisines, countries and allergens as I could not do them through unittest 
at this time. In making sure they would work I would print a lot of response data to see if I was getting everything correct. I would also check if the data was being
stored correctly in the database. To check the statistics summaries or the charts I would make a note of them, then create a new recipe that would alter the results 
and then check the stats page again to see that it had been updated. I did the same to make sure the upvoting mechanism worked. 


#### Cross-browser Testing
I developed the site mainly on Chrome but have also since tested it on Safari and Firefox with no issues.
All user stories have been checked with developer tools for their responsiveness. 
Through this method I tested a wide variety of devices; iPhone 5,6,7,8,X, 
iPad, iPad Pro, Google Pixel 2 and Galaxy S5. I am very happy with how my project scales on different devices.

#### Code Validation
I ran all my files through validators to check for errors.
    - W3C for CSS.
    - W3C for HTML.
    - JS Hint for Javascript.
    - [pep8online](http://pep8online.com) - for Python

## Deployment
- Project was deployed to heroku with ease.
- Created Procfile and requirements.txt
- Created new heroku app and set environment variables.
- Pushed to heroku.
- Linked pre-existing mongodb to new site, no installation necessary.

## Credits


### Acknowledgements
- [BBC Recipes](https://www.bbc.com/food/recipes) for helping me fill the database with entries.
- The many chef's named in the recipes. 
