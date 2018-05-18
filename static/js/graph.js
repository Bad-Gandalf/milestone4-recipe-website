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
        var allergen_list = [];
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



 // Actual Score versus Lifetime Rank Scatter Plot
 /*this.show_cuisine_name_to_upvotes_correlation = function(ndx) {

  /*var countryColors = d3.scale.ordinal()
   .domain(["Japan", "United States", "Republic of Korea", "Taiwan", "United Kingdom", "France", "Singapore", "China", "Dominican Republic", "Belgium", "Norway"])
   .range(["black", "blue", "red", "yellow", "orange", "grey", "green", "pink", "purple", "brown", "light-blue"])

  var rDim = ndx.dimension(dc.pluck("cuisine_name"));
  var rankDim = ndx.dimension(function(d) {
   return [d.Rank, d["Actual Score"], d.Name, d.Country, d.Character]
  });

  var actualScoresDim = rankDim.group();

  var minRank = rDim.bottom(1)[0].Rank;
  var maxRank = rDim.top(1)[0].Rank


  dc.scatterPlot("#Lifetime-rank-to-actual-score")
   .width(1000)
   .height(300)
   .x(d3.scale.linear().domain([minRank, maxRank]))
   .brushOn(false)
   .symbolSize(8)
   .clipPadding(10)
   .xAxisLabel("Lifetime Rank")
   .yAxisLabel("Actual Score")
   .title(function(d) {
    return d.key[2] + " has an actual score of " + d.key[1] + " and ranks #" + d.key[0] + ". Character: " + d.key[4];
   })
   .colorAccessor(function(d) {
    return d.key[3];
   })
   .colors(countryColors)
   .dimension(rankDim)
   .group(actualScoresDim)
   .margins({ top: 10, right: 10, bottom: 75, left: 70 });

 }*/
var counts = {};
for (var i = 0; i < allergen_list.length; i++) {
    counts[allergen_list[i]] = 1 + (counts[allergen_list[i]] || 0);
}
let unique_allergen_list = allergen_list.filter(function (x, i, a) { 
    return a.indexOf(x) == i; 
});

console.log(allergen_list);
 //Pie Chart Participation By Country
 this.show_recipes_by_cuisine = function(ndx) {

  var country_dim = ndx.dimension(dc.pluck("cuisine_name"));
  var upvotes = country_dim.group().reduceSum(dc.pluck("upvotes"));

  dc.pieChart("#lifetime-score-by-country")
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
     
     dc.pieChart("#most_occuring_allergens")
     .height(220)
     .radius(100)
     .transitionDuration(1500)
     .dimension(countries_dim)
     .group(numOfcountries);
     
    
 }

 /*/Pie Chart Lifetime Points By Team
 this.show_lifetime_scores_by_team = function (ndx) {
     var team_dim = ndx.dimension(dc.pluck("Team"));
     var total_lifetime_score = team_dim.group().reduceSum(dc.pluck('Lifetime Score'));

     dc.pieChart("#total-lifetime-score-by-team")
         .height(220)
         .radius(100)
         .transitionDuration(1500)
         .dimension(team_dim)
         .group(total_lifetime_score);
 }*/
 // Barchart for Lifetime scores by Character
this.upvotes_by_user = function(ndx) {
  var user_dim = ndx.dimension(dc.pluck("username"));
  var total_lifetime_score = user_dim.group().reduceSum(dc.pluck('upvotes'));

  dc.barChart("#total-lifetime-score-by-character")
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

 }
 
 this.upvotes_by_country = function(ndx) {
  var user_dim = ndx.dimension(dc.pluck("country"));
  var total_lifetime_score = user_dim.group().reduceSum(dc.pluck('upvotes'));

  dc.barChart("#average-lifetime_score_by-character")
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

 }
 // Barchart for Average Lifetime scores by Character
 /*this.show_average_lifetime_score_per_character = function(ndx) {
  var dim = ndx.dimension(dc.pluck('Character'));

  function add_item(p, v) {
   p.count++;
   p.total += v["Lifetime Score"];
   p.average = p.total / p.count;
   return p;
  }

  function remove_item(p, v) {
   p.count--;
   if (p.count == 0) {
    p.total = 0;
    p.average = 0;
   }
   else {
    p.total -= v["Lifetime Score"];
    p.average = p.total / p.count;
   }
   return p;
  }

  function initialise() {
   return { count: 0, total: 0, average: 0 };
  }

  var averageLifetimeScoreByCharacter = dim.group().reduce(add_item, remove_item, initialise);

  dc.barChart("#average-lifetime_score_by-character")
   .width(1000)
   .height(300)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(dim)
   .group(averageLifetimeScoreByCharacter)
   .valueAccessor(function(d) {
    return d.value.average.toFixed(2);
   })
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .y(d3.scale.linear().domain([0, 170000]))
   .xAxisLabel("Character")
   .yAxisLabel("Average Lifetime Score")
   .yAxis().ticks(4);
 }

 // Bar Charts By Gender
 this.show_lifetime_scores_by_character_gender = function(ndx) {
  var gender_dim = ndx.dimension(dc.pluck("Character Gender"));
  var total_lifetime_score = gender_dim.group().reduceSum(dc.pluck('Lifetime Score'));

  dc.barChart("#total-lifetime-score-by-character-gender")
   .width(300)
   .height(220)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(gender_dim)
   .group(total_lifetime_score)
   .valueAccessor(function(d) {
    return d.value;
   })
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .elasticY(true)
   .xAxisLabel("Character Gender")
   .yAxisLabel("Total Lifetime Score")
   .yAxis().ticks(4);
 }

 this.show_average_lifetime_score_per_character_gender = function(ndx) {
  var dim = ndx.dimension(dc.pluck('Character Gender'));

  function add_item(p, v) {
   p.count++;
   p.total += v["Lifetime Score"];
   p.average = p.total / p.count;
   return p;
  }

  function remove_item(p, v) {
   p.count--;
   if (p.count == 0) {
    p.total = 0;
    p.average = 0;
   }
   else {
    p.total -= v["Lifetime Score"];
    p.average = p.total / p.count;
   }
   return p;
  }

  function initialise() {
   return { count: 0, total: 0, average: 0 };
  }

  var averageLifetimeScoreByCharacter = dim.group().reduce(add_item, remove_item, initialise);

  dc.barChart("#average-lifetime_score_by-character-gender")
   .width(300)
   .height(220)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(dim)
   .group(averageLifetimeScoreByCharacter)
   .valueAccessor(function(d) {
    return d.value.average.toFixed(2);
   })
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .y(d3.scale.linear().domain([0, 120000]))
   .xAxisLabel("Character Gender")
   .yAxisLabel("Average Lifetime Score")
   .yAxis().ticks(4);
 }*/


this.show_recipes_by_cuisine(ndx);
this.recipes_in_cuisine(ndx);
this.most_occuring_countries(ndx);  
this.upvotes_by_user(ndx);
this.upvotes_by_country(ndx);
/*  this.show_participation_by_country(ndx);
  this.show_lifetime_rank_to_actual_scores_correlation(ndx);
  // this.show_lifetime_scores_by_team(ndx);
  this.show_lifetime_scores_by_character_gender(ndx);
  this.show_average_lifetime_score_per_character_gender(ndx);*/

dc.renderAll();
};
};
const P = new RecipeDBApi;
P.init();
