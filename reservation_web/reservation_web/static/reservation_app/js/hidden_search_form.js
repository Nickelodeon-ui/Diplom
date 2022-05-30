$(document).ready(function () {
    $("#button_to_show_search_form").click(function () {
        if ($("#search_form").hasClass("selected")) {
            $("#search_form").hide();
            $("#search_form").removeClass("selected")
        }
        else {
            $("#search_form").show();
            $("#search_form").addClass("selected");
        }
    });
});