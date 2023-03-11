data = document.currentScript.dataset;
const r_overall = parseInt(data.overall)
const r_commute = parseInt(data.commute)
const r_restaurant = parseInt(data.restaurant)
const r_grocery = parseInt(data.grocery)
const r_medical = parseInt(data.medical)

var overall_stars = document.getElementsByClassName("overall_stars fa fa-star star")
var commute_stars = document.getElementsByClassName("commute_stars fa fa-star star");
var restaurant_stars = document.getElementsByClassName("restaurant_stars fa fa-star star");
var grocery_stars = document.getElementsByClassName("grocery_stars fa fa-star star");
var medical_stars = document.getElementsByClassName("medical_stars fa fa-star star");

overall_color = getColor(r_overall)
Array.from(overall_stars).forEach((s, index) => {
    if(index<r_overall) {
        s.style.color = overall_color;
    }
})

commute_color = getColor(r_commute)
Array.from(commute_stars).forEach((s, index) => {
    if(index<r_commute) {
        s.style.color = commute_color;
    }
})

restaurant_color = getColor(r_restaurant)
Array.from(restaurant_stars).forEach((s, index) => {
    if(index<r_restaurant) {
        s.style.color = restaurant_color;
    }
})

grocery_color = getColor(r_grocery)
Array.from(grocery_stars).forEach((s, index) => {
    if(index<r_grocery) {
        s.style.color = grocery_color;
    }
})

medical_color = getColor(r_medical)
Array.from(medical_stars).forEach((s, index) => {
    if(index<r_medical) {
        s.style.color = medical_color;
    }
})


function getColor(score){
    // perfect
    if(score>=4.5) {
        return "#b8d38f";
    }

    // good
    else if(score >=4) {
        return "#b8f1ed";
    }

    // ok
    else if(score >=3) {
        return "#fecf45";
    }

    // okk
    else if(score >=2) {
        return "#ff9b6a";
    }

    // bad
    else {
        return "#f1707d";
    }

  }
