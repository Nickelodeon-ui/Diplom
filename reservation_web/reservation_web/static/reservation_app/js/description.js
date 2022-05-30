$(document).ready(function () {
    $(".hidden_description").hide();

    $(".full_description_link").click(function(){
        $(".hidden_description").show();
        $(this).hide();
    });
});