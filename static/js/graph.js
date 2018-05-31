const RecipeDBApi = function() {

 this.init = function() {
  queue()
   .defer(d3.csv, "/static/data/recipe_mining.csv")
   .await(this.makeGraphs);
 };

 this.makeGraphs = function (error, data) {
  var ndx = crossfilter(data);

  //Data Parsing
  data.forEach(function(d) {
   d["upvotes"] = +d["upvotes"];
   d["cook_time"] = +d["cook_time"];
   d["prep_time"] = +d["prep_time"];
   
 
   if (d.cuisine_name == "") {
    d.Team = "No Cuisine";
   }
   else {
    return d.cuisine_name;
   }
   
  });
  
  
  console.log(data);

 //Pie Chart Participation By Country
 this.upvotes_by_cuisine = function(ndx) {

  var country_dim = ndx.dimension(dc.pluck("cuisine_name"));
  var upvotes = country_dim.group().reduceSum(dc.pluck("upvotes"));

  dc.pieChart("#upvotes_by_cuisine")
   .height(220)
   .radius(100)
   
   .transitionDuration(1500)
   .dimension(country_dim)
   .group(upvotes);

 }
 
this.recipes_in_cuisine = function(ndx) {
     var cuisine_dim = ndx.dimension(dc.pluck("cuisine_name"));
     var recipes = cuisine_dim.group()
     
     dc.pieChart("#recipes_by_cuisine")
     .height(220)
     .radius(100)
     .transitionDuration(1500)
     .dimension(cuisine_dim)
     .group(recipes);
 }
 
 this.most_occuring_countries = function(ndx) {
     
     var countries_dim = ndx.dimension(dc.pluck("country"));
     var numOfcountries = countries_dim.group();
     
     dc.pieChart("#most_occuring_countries")
     .height(220)
     .radius(100)
     .transitionDuration(1500)
     .dimension(countries_dim)
     .group(numOfcountries);
     
    
 };

this.upvotes_by_user = function(ndx) {
  var user_dim = ndx.dimension(dc.pluck("username"));
  var total_lifetime_score = user_dim.group().reduceSum(dc.pluck('upvotes'));

  dc.barChart("#most_upvoted_users")
   .width(1000)
   .height(300)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(user_dim)
   .group(total_lifetime_score)
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .elasticY(true)
   .xAxisLabel("Users")
   .yAxisLabel("UpVotes")
   .yAxis().ticks(4);

 };
 
 this.upvotes_by_country = function(ndx) {
  var user_dim = ndx.dimension(dc.pluck("country"));
  var total_lifetime_score = user_dim.group().reduceSum(dc.pluck('upvotes'));

  dc.barChart("#upvotes_by_country")
   .width(1000)
   .height(300)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(user_dim)
   .group(total_lifetime_score)
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .elasticY(true)
   .xAxisLabel("Users")
   .yAxisLabel("UpVotes")
   .yAxis().ticks(4);

 };
 



this.upvotes_by_cuisine(ndx);
this.recipes_in_cuisine(ndx);
this.most_occuring_countries(ndx);  
this.upvotes_by_user(ndx);
this.upvotes_by_country(ndx);

dc.renderAll();
};
};
const AllergensApi = function() {

 this.init = function() {
  queue()
   .defer(d3.csv, "/static/data/allergen_data.csv")
   .await(this.makeGraphs);
 };

 this.makeGraphs = function (error, data) {
  var ndx = crossfilter(data);

  //Data Parsing

 
this.most_occuring_allergens = function(ndx) {
     var allergens_dim = ndx.dimension(dc.pluck("allergen_name"));
     var frequency = allergens_dim.group()
     
   dc.barChart("#most_occuring_allergens")
   .width(1000)
   .height(300)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(allergens_dim)
   .group(frequency)
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .elasticY(true)
   .xAxisLabel("Allergens")
   .yAxisLabel("Frequency")
   .yAxis().ticks(4);
 };

this.most_occuring_allergens(ndx);  


dc.renderAll();
};
};
const P = new RecipeDBApi;
const Q = new AllergensApi;
P.init();
Q.init();
