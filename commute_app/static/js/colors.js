var Body = {
  setColor: function(color){
    document.querySelector('body').style.color = color;
  },
  setBackgroundColor: function(color){
    document.querySelector('body').style.backgroundColor = color;
  }
}

var Links = {
  setColor: function(color){
    $('a').css('color', color);
  }
}

function nightDayHandler(self){
  // var target = document.querySelector('body');
  if(self.value === 'Night'){
    Body.setBackgroundColor('black');
    Body.setColor('white');
    Links.setColor('powderblue');
    self.value = 'Day';
    } else {
    Body.setBackgroundColor('beige');
    Body.setColor('black');
    Links.setColor('darkblue');
    // todo: How can I set this to default css style?
    // for example, I want that a:hover back
    self.value = 'Night';
    }
}
