$(document).ready(function() {
    $('.collapsible-header a').click(function(e) {
        e.stopPropagation();
    });
    $('.collapsible').collapsible();
    $('select').material_select();
    $('.button-collapse').sideNav();
});

// This code operates on the link that is also the title of the recipe. It prevents a collapsible div showing. 
// It will still collapse when anywhere else on the panel is clicked on.