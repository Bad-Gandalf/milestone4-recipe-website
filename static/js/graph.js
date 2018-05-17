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
   d.Tournaments = +d.Tournaments;
   d["cook_time"] = +d["cook_time"];
   d["prep_time"] = +d["prep_time"];
   //Data Cleansing i.e. No Team = Independant      
  
   if (d.allergens == []) {
    d.Team = "No Allergens";
   }
   else {
    return d.allergens;
   }
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

 //Pie Chart Participation By Country
 this.show_recipes_by_cuisine = function(ndx) {

  var country_dim = ndx.dimension(dc.pluck("cuisine_name"));
  var upvotes = ndx.dimension(dc.pluck("upvotes"));

  dc.pieChart("#lifetime-score-by-country")
   .height(220)
   .radius(100)
   .transitionDuration(1500)
   .dimension(country_dim)
   .group(upvotes);

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
/* this.show_lifetime_scores_by_character = function(ndx) {
  var character_dim = ndx.dimension(dc.pluck("Character"));
  var total_lifetime_score = character_dim.group().reduceSum(dc.pluck('Lifetime Score'));

  dc.barChart("#total-lifetime-score-by-character")
   .width(1000)
   .height(300)
   .margins({ top: 10, right: 50, bottom: 75, left: 75 })
   .dimension(character_dim)
   .group(total_lifetime_score)
   .transitionDuration(500)
   .x(d3.scale.ordinal())
   .xUnits(dc.units.ordinal)
   .elasticY(true)
   .xAxisLabel("Characters")
   .yAxisLabel("Lifetime Score")
   .yAxis().ticks(4);

 }
 // Barchart for Average Lifetime scores by Character
 this.show_average_lifetime_score_per_character = function(ndx) {
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
  /*this.show_average_lifetime_score_per_character(ndx);
  this.show_participation_by_country(ndx);
  this.show_lifetime_rank_to_actual_scores_correlation(ndx);
  // this.show_lifetime_scores_by_team(ndx);
  this.show_lifetime_scores_by_character_gender(ndx);
  this.show_average_lifetime_score_per_character_gender(ndx);*/

dc.renderAll();
};
};
const P = new RecipeDBApi;
P.init();
