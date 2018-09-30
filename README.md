# Code Institute - Milestone Project 5 - Recipe Manager
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
 


## Features

### Existing Features
- Simple Quiz App

### Potential future features
- Login authentication system
- Only creators of recipes can edit them
- Uploading pictures for the recipes, countries, allergens and cuisines.
- Adding a review system to each recipe, where other users can comment on their experience with the recipe.


## Technologies used:
##### HTML - hypertext markup language
##### CSS - cascading style sheets 
##### Javascript - client side scripting language
##### Python - Programming Language
##### Git Bash & GitHub -for version control and backup of code
##### Bootstrap - A framework for developing responsive, mobile 1st websites.
##### Flask - python web framework
##### Postman - Postman helps you develop APIs faster
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
- [intro.js](https://github.com/usablica/intro.js)
    - For guided tour of charts with explanations.

## Testing
 
### Automated testing

#### TDD
To ensure I was designing functions correctly I used tests to drive development. The majority of these can be found in helper_tests.py.
I could not write tests for all functions especially those required to write, retrieve and operate on data in a text file. I did however print my results
whilst designing the functions. I would also be able to check the text file itself to see if everything was working. I would also compare these to what 
the site was rendering, over and over again until I was getting the results I wanted. 

#### Test Suite
Once I was happy with the site I used unittest to do fully automated tests of the quiz app. I simulated a user logging on, and then going through each of the questions
eventually leading to the leaderboard. I also made sure to do a few runs, including incorrect answers and question skips. I made sure to 
test for the correct responses whther they were based on final score or incorrect answers. These can be found in test_app.py. All routes were tested including
the routes specifically for javascript. I also used Postman to check that I recieving the correct HTML when sending information to routes.

### Manual testing
#### Preventing Cheating
During my development I tired to break the game as often as possible, this seemed to be most easy by pressing the back button. I had originally designed the 
app to have a specific url for each question and users could simply visit these urls and answer the questions again. I removed this possibility by using
"sessions". This would allow for tracking a users progress and ensuring they could not go backwards or forwards or potentially answer any question
they were not supposed to. 

At the very end of my testing I noticed I was using a value from a hidden input (the solution to the question) to validate the answers. Anyone who could 
open dev tools could see this and simply copy it. They could even change it and that would work as the new solution. I removed this possiblity and found 
a simple work around. 

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

## Deployment
- Project was deployed to heroku with ease.
- Created Procfile and requirements.txt
- Created new heroku app and set environment variables.
- Pushed to heroku. Click [here](https://tolkien-riddle-quiz.herokuapp.com/) to visit the site.

## Credits

### Media
- All of the original links the images used can be found in /data/riddle_data.json. All taken from google image searches. 


### Acknowledgements
- J. R. R. Tolkien for his timeless riddles.
- Thanks to the following Youtubers for sharing their knowledge
    - [Pretty Printed](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)
    - [Tekboi Tutorials](https://www.youtube.com/channel/UCIx6RlgCn3dXR5mHF33_wsA)