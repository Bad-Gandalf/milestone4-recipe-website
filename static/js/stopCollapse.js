$(document).ready(function() {
            $('.collapsible-header a').click(function(e) {
                e.stopPropagation();
            });
            $('.collapsible').collapsible();
            $('select').material_select();
            $('.button-collapse').sideNav();
        });