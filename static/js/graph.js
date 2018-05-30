const RecipeDBApi = function() {

 this.init = function() {
  queue()
   .defer(d3.csv, "/static/data/recipe_mining.csv")
   .await(this.makeGraphs);
 };

 this.makeGraphs = function (error, data) {
  var ndx = crossfilter(data);

let allergen_list=[];
  //Data Parsing
  data.forEach(function(d) {
   d["upvotes"] = +d["upvotes"];
   d["cook_time"] = +d["cook_time"];
   d["prep_time"] = +d["prep_time"];
   
   console.log(d.allergens);
    function get_values(){
        
        var allergens = d.allergens.split(',');
        var array_length = allergens.length;
        for (var i = 0; i < array_length; i++) {
            allergens[i] = allergens[i].replace("[", '');
            allergens[i] = allergens[i].replace("]", '');
            allergens[i] = allergens[i].replace("{", '');
            allergens[i] = allergens[i].replace("}", '');
            allergens[i] = allergens[i].replace("'allergen_name':", '');
            allergens[i] = allergens[i].replace(/[']+/g, '');
            allergens[i] = allergens[i].trim();
            
            }
         allergen_list.push(Object.values(allergens));
         return allergen_list;
         }    
            
            
    d.allergens = get_values();
     
   
   
   if (d.cuisine_name == "") {
    d.Team = "No Cuisine";
   }
   else {
    return d.cuisine_name;
   }
   
  });
  
  
  console.log(data);

/*allergen_list = [].concat.apply([], allergen_list);
console.log(allergen_list);
 
var counts = {};
for (var i = 0; i < allergen_list.length; i++) {
    counts[allergen_list[i]] = 1 + (counts[allergen_list[i]] || 0);
}
console.log(counts);

function renameKeys(obj, newKeys) {
  const keyValues = Object.keys(obj).map(key => {
    const newKey = newKeys[key] || key;
    return { [newKey]: obj[key] };
  });
  return Object.assign({}, ...keyValues);
}
let result = Object.keys(counts).map(function(key) {
  let arr =  [key, counts[key]];
  let new_object = Object.assign({}, arr);
  const new_keys = { 0: "Name", 1:"Value"};
  let renamed_object = renameKeys(new_object, new_keys);
  return renamed_object;
});


console.log(result);*/

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
const P = new RecipeDBApi;
P.init();
