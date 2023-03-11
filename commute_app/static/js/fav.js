const data = document.currentScript.dataset;
const check_fav = data.fav
var fav_box = document.getElementById("checkbox")


function handle_fav() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
    document.getElementById("fav_form").submit();
}

// if (check_fav == "fav") {
//     fav_box.checked = true
// } else {
//     fav_box.checked = false
// }

// console.log(data.fav)