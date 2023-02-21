var myVideo = document.getElementById("video");//player
var coolPlay = document.getElementById("cool-play");
var cPlay = document.getElementById("c-play");//play button 
var cProgress = document.getElementById("c-progress");
var cPlayed = document.getElementById("c-played");//played progress bar
var cDrag = document.getElementById("c-drag");//index of the progress bar
var cCurrentTime = document.getElementById("c-currentTime");
var cTotalTime = document.getElementById("c-totalTime");
var loading = document.getElementsByClassName("icon-c-loading");//loading logging
var refresh = document.getElementsByClassName("icon-c-refresh");//reload button
var voice = document.getElementsByClassName("i-voice");//volume button
var voice_mask = document.getElementsByClassName("voice-mask");//full bar for volume
var voice_bared= document.getElementsByClassName("voice-bared");//currernt bar for volume
var voice_dot = document.getElementsByClassName("voice-dot");
var voice_num = 0.8;
volume(voice_num);//initialize
function volume(n){
  myVideo.volume = n;
  voice_bared[0].style.height=n*100 + 'px';
}
function playPause() {
  if(myVideo.paused) {
    Play();
  } else {
    Pause();
  }
};
function Play(){
  cPlay.className = "icon-c-pause";
  myVideo.play();
}
function Pause(){
  cPlay.className = "icon-c-play";
  myVideo.pause();
}
refresh[0].onclick = function (){
  Load();
}
function Load(){
  Pause();
  myVideo.load();
  cPlayed.style.width = 0+"%";
  cDrag.style.display="none";
  cCurrentTime.innerHTML = "00:00:00";
  cTotalTime.innerHTML = "00:00:00";
}
// player time & progress bar
myVideo.ontimeupdate = function(){  
  var currTime = this.currentTime,    // current time of the video
      duration = this.duration;       // total duration of the video
  if(currTime == duration){
    Pause();
  }
  // percentage 
  var pre = currTime / duration * 100 + "%";
  // display progress bar
  cPlayed.style.width = pre;
  var progressWidth = cProgress.offsetWidth;
  var leftWidth = progressWidth*(currTime / duration);
  if(leftWidth > 8 && (progressWidth - leftWidth) > 4){
    cDrag.style.display="block";    
  } else {
    cDrag.style.display="none";
  }  
  cDrag.style.left = progressWidth*(currTime / duration)-4 + "px";
  // display current progress playing time
  cCurrentTime.innerHTML = getFormatTime(currTime,duration);
  cTotalTime.innerHTML = getFormatTime(duration,duration);
};
// when browser can play with no loading pause
myVideo.oncanplaythrough = function() {
  loading[0].style.display="none";
}
// when video stop for loading the next frame
myVideo.onwaiting = function() {
  loading[0].style.display="block";
}
// user move/jump to new location in video
myVideo.onseeking = function() {
  if (myVideo.readyState == 0 || myVideo.readyState == 1) {
    loading[0].style.display="block";
  }
}

cProgress.onclick = function(e){
  var event = e || window.event;
  console.log("Click Position: "+(event.offsetX / this.offsetWidth) * myVideo.duration);
  myVideo.currentTime = (event.offsetX / this.offsetWidth) * myVideo.duration;
};

function getFormatTime(time,duration) {
  var time = time || 0;         
  
  var h = parseInt(time/3600),
      m = parseInt(time%3600/60),
      s = parseInt(time%60);

  m = m < 10 ? "0"+m : m; 
  h = h < 10 ? "0"+h : h;
  s = s < 10 ? "0"+s : s;
  return h+":"+m+":"+s;

}   
/* Audio Related */
//mute the video
voice[0].onclick = function(){  
  if(myVideo.muted){
    voice[0].className="i-voice icon-c-voice";
    myVideo.muted=false;
    if(voice_num >= 0 && voice_num <= 1){
      volume(voice_num);
    } else {
      volume(0.8);
    }    
  } else {
    voice_num = myVideo.volume; //record the volume before mute
    voice[0].className='i-voice icon-c-mute';
    myVideo.muted=true;
    volume(0);
  }  
}
//change the volume
voice_mask[0].onclick = function(e){
  var event = e || window.event;  
  if(event.offsetY >= 100){
    voice[0].className='i-voice icon-c-mute';
    myVideo.muted=true;
    volume(0);
    return;
  }
  volume((100-event.offsetY)/100);
};

var fullscreen = document.getElementById('cool-fullScreen');
var FullScreenTF = true;
function launchFullscreen(element) {
  if(element.requestFullscreen) {
    element.requestFullscreen();
  } else if(element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if(element.msRequestFullscreen) {
    element.msRequestFullscreen();
  } else if(element.oRequestFullscreen) {
    element.oRequestFullscreen();
  } else if(element.webkitRequestFullscreen) {
    element.webkitRequestFullScreen();
  } else {
    alert("Your browser version is too low to support full screen function!");
  }
  FullScreenTF = false;
};

function exitFullscreen() {
  if(document.exitFullscreen) {
    document.exitFullscreen();
  } else if(document.msExitFullscreen) {
    document.msExitFullscreen();
  } else if(document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if(document.oRequestFullscreen) {
    document.oCancelFullScreen();
  } else if(document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else {
    alert("Your browser version is too low to support full screen function!");
  }
  FullScreenTF = true;
};
fullscreen.onclick = function() {       
  if(FullScreenTF) {
    launchFullscreen(coolPlay);
    fullscreen.className = "icon-c-shrink";         
  } else {
    exitFullscreen();
    fullscreen.className = "icon-c-enlarge";          
  }
};
