// $(document).ready(function () {

//     $(".submit-btn").click(function () {
//         var data = {}

//         data['country'] = document.getElementById("country").value; 
//         data['from_date'] = document.getElementById("from_date").value;
//         data['to_date'] = document.getElementById("to_date").value;
//         data['adults_qty'] = Number(document.getElementById("adults").value);
//         data['kids_qty'] = Number(document.getElementById("children").value);
//         data['rooms_qty'] = Number(document.getElementById("rooms").value);
//         data['csrfmiddlewaretoken'] = getCookie('csrftoken');

//         console.log(data)

//         $.ajax ({
//               type: 'POST',
//               url: './search_for_reservation',
//               data: data,
//               success: function(response){
//                 if (response.status == 1) {
//                     // Сообщение пользователю?  
//                     window.location = response.url;
//                 } else {
//                     alert(response.message);
//                 }
//               }
//             });
//     });
// });

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }