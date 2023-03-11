data = document.currentScript.dataset;
const check_fav = data.fav
var fav_box = document.getElementById("checkbox")


function handle_fav() {
    console.log("handle")
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () { 
        x.className = x.className.replace("show", ""); }, 1000);
    setTimeout(function() {
        document.getElementById("fav_form").submit();
    }, 1000);
    
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

if (check_fav == "fav") {
    fav_box.checked = true
}