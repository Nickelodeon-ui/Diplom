$(document).ready(function () {
    // For suggestion bgs form 
    $(".formstart_btn").click(function () {
        $(".hidden_form-background").show()
        $(".hidden_form-background").css("height", $(document).height());
        $(".footer__form").fadeIn(500);
        $(".hidden_form-background").addClass("selected");
        $(".footer__form").addClass("selected");
    });    

    $(".hidden_form-background").click(function () {
        if ($(this).hasClass("selected")) {
            $(this).hide();
            $(".footer__form").hide();
            $(this).removeClass("selected");
            $(".footer__form").removeClass("selected");
        }
    });

    $(".footer_form-img").click(function () {
        // Exactly the same only for cross    
        if ($(".hidden_form-background").hasClass("selected")) {
            $(".hidden_form-background").hide();
            $(".footer__form").hide();
            $(".hidden_form-background").removeClass("selected");
            $(".footer__form").removeClass("selected");
        }
    });

    $(".dop_info").click(function () {
        if ($(".hidden_search_details").hasClass("selected")) {
            $(".hidden_search_details").hide();
            $(".hidden_search_details").removeClass("selected");
        }
        else {
            $(".hidden_search_details").show();
            $(".hidden_search_details").addClass("selected").focus();
        }
    });

    document.addEventListener('click', (event) => {
        const withinBoundariesofDopInfo = event.composedPath().includes(document.querySelector('.dop_info'))
        const withinBoundariesofHiddenDetails = event.composedPath().includes(document.querySelector('.hidden_search_details'))
        const qtyOfPathElements = event.composedPath().length;
        console.log(qtyOfPathElements)
       
        if (Boolean(!withinBoundariesofHiddenDetails & !withinBoundariesofDopInfo & $(".hidden_search_details").hasClass("selected"))) {
            $(".hidden_search_details").hide();
            $(".hidden_search_details").removeClass("selected");
        };
        
        if (qtyOfPathElements == 19){
            element = document.getElementById("dop_info");
            element_adults = document.getElementById("id_adults_qty");
            element_children = document.getElementById("id_kids_qty");
            element_rooms = document.getElementById("id_rooms_qty");
            
            element.innerText = `Взрослые: ${element_adults.value}; Дети: ${element_children.value}; Номера: ${element_rooms.value}`;
        };

        if (qtyOfPathElements == 15){
            element = document.getElementById("dop_info_2");
            element_adults = document.getElementById("adults_qty_id_2");
            element_children = document.getElementById("kids_qty_id_2");
            element_rooms = document.getElementById("rooms_qty_id_2");
            
            
            element.innerText = `Взрослые: ${element_adults.value}; Дети: ${element_children.value}; Номера: ${element_rooms.value}`;
        };
    });
});