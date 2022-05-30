$(document).ready(function () {
    var LowerBorder = 9
    var bgs_grid = document.getElementById("items__inner")

    $(".more").click(function () {
        var path = window.location.pathname
        if (path.includes("search-for-bg")) {
            var url = `./more-searched-bg/${LowerBorder}` 
        }
        else {
            var url = `./more-bg/${LowerBorder}`
        }
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                const boardgames = response.data
                if (boardgames.length != 0) {
                    let i;
                    for (i = 0; i < boardgames.length; i++) {
                        bgs_grid.innerHTML += `
                    <a class="item" href="/catalog/${boardgames[i]["slug"]}">
                    <div class="item__inner">
                        <img src="/media/${boardgames[i]["img"]}" alt="bg_logo" class="item__inner-img">
                        <div class="item__inner-content">
                            <p class="item__inner-content-name">${boardgames[i]["name"]}</p>
                            <p class="item__inner-content-quantity">На складе: ${boardgames[i]["quantity"]}</p>
                            <p class="item__inner-content-price">${boardgames[i]["price"]} р.</p>
                        </div>
                    </div>
                </a>`
                if (response.reached_max == true){
                    $(".more").hide();
                }
                    }
                } else {
                    $(".more").hide();
                }
                LowerBorder += 3
            }
        });
    });
});