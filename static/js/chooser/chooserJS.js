var chooserJSPlanetInfo = [
  {name: 'earth', text: 'Earth (Moon)', img: 'earth.png', height1: "80px", width1: "80px", height2: "60px", width2: "60px", top: '115px', left: '175px', titleTop: '95px', titleLeft: '170px'},
  {name: 'jupiter', text: 'Jupiter', img: 'jupiter.png', height1: "200px", width1: "200px", height2: "150px", width2: "150px", top: '280px', left: '165px', titleTop: '265px', titleLeft: '240px'},
  {name: 'mars', text: 'Mars', img: 'mars.png', height1: "60px", width1: "60px", height2: "40px", width2: "40px", top: '60px', left: '260px', titleTop: '40px', titleLeft: '260px'},
  {name: 'mercury', text: 'Mercury', img: 'mercury.png', height1: "50px", width1: "50px", height2: "25px", width2: "25px", top: '295px', left: '55px', titleTop: '275px', titleLeft: '55px'},
  {name: 'neptune', text: 'Neptune', img: 'neptune.png', height1: "55px", width1: "55px", height2: "35px", width2: "35px", top: '60px', left: '450px', titleTop: '40px', titleLeft: '445px'},
  {name: 'saturn', text: 'Saturn', img: 'saturn.png', height1: "200px", width1: "200px", height2: "150px", width2: "150px", top: '170px', left: '270px', titleTop: '205px', titleLeft: '310px'},
  {name: 'smallBodies', text: 'Small Bodies', img: 'smallBodies.png', height1: "100px", width1: "100px", height2: "70px", width2: "70px", top: '360px', left: '365px', titleTop: '355px', titleLeft: '360px'},
  {name: 'uranus', text: 'Uranus', img: 'uranus.png', height1: "100px", width1: "100px", height2: "75px", width2: "75px", top: '120px', left: '375px', titleTop: '120px', titleLeft: '390px'},
  {name: 'venus', text: 'Venus', img: 'venus.png', height1: "80px", width1: "80px", height2: "60px", width2: "60px", top: '200px', left: '100px', titleTop: '180px', titleLeft: '115px'}
];


function init_hovers() {
  //jquery planet hovers
  $(document).ready(function() {

    $("#earth").hover(function() {
       $("#earth").stop().animate({ height: "80px", width: "80px"}, 300);
       document.getElementById("earthTitle").style.display = "inline";
    },function() {
        $("#earth").stop().animate({ height: "60px", width: "60px"}, 300);
       document.getElementById("earthTitle").style.display = "none";
    });
    $("#jupiter").hover(function() {
       $("#jupiter").stop().animate({ height: "200px", width: "200px"}, 300);
       document.getElementById("jupiterTitle").style.display = "inline";
    },function() {
        $("#jupiter").stop().animate({ height: "150px", width: "150px" }, 300);
       document.getElementById("jupiterTitle").style.display = "none";
    });
    $("#mars").hover(function() {
       $("#mars").stop().animate({ height: "60px", width: "60px"}, 300);
       document.getElementById("marsTitle").style.display = "inline";
    },function() {
        $("#mars").stop().animate({ height: "40px", width: "40px"}, 300);
       document.getElementById("marsTitle").style.display = "none";
    });
    $("#mercury").hover(function() {
       $("#mercury").stop().animate({ height: "50px", width: "50px"}, 300);
       document.getElementById("mercuryTitle").style.display = "inline";
    },function() {
        $("#mercury").stop().animate({ height: "25px", width: "25px"}, 300);
       document.getElementById("mercuryTitle").style.display = "none";
    });
    $("#neptune").hover(function() {
       $("#neptune").stop().animate({ height: "55px", width: "55px"}, 300);
       document.getElementById("neptuneTitle").style.display = "inline";
    },function() {
        $("#neptune").stop().animate({ height: "35px", width: "35px"}, 300);
       document.getElementById("neptuneTitle").style.display = "none";
    });
    $("#saturn").hover(function() {
       $("#saturn").stop().animate({ height: "200px", width: "200px"}, 300);
       document.getElementById("saturnTitle").style.display = "inline";
    },function() {
        $("#saturn").stop().animate({ height: "150px", width: "150px"}, 300);
       document.getElementById("saturnTitle").style.display = "none";
    });
    $("#smallBodies").hover(function() {
       $("#smallBodies").stop().animate({ height: "100px", width: "100px"}, 300);
       document.getElementById("smallBodiesTitle").style.display = "inline";
    },function() {
        $("#smallBodies").stop().animate({ height: "70px", width: "70px"}, 300);
       document.getElementById("smallBodiesTitle").style.display = "none";
    });
    $("#venus").hover(function() {
       $("#venus").stop().animate({ height: "80px", width: "80px"}, 300);
       document.getElementById("venusTitle").style.display = "inline";
    },function() {
        $("#venus").stop().animate({ height: "60px", width: "60px"}, 300);
       document.getElementById("venusTitle").style.display = "none";
    });
    $("#uranus").hover(function() {
       $("#uranus").stop().animate({ height: "100px", width: "100px"}, 300);
       document.getElementById("uranusTitle").style.display = "inline";
    },function() {
        $("#uranus").stop().animate({ height: "75px", width: "75px"}, 300);
       document.getElementById("uranusTitle").style.display = "none";
    });

  });
}


//create planet div/img
function createChooserJS (el) {

  var container = document.getElementById(el);
  var div = document.createElement("div");
  div.setAttribute('id', 'chooserBackground');
  div.style.zIndex = 2;
  div.style.width = '540px';
  div.style.height = '490px';
  div.style.position = 'relative';
  div.style.background = "#000000 url(\""+ chooserJSPath +"sun.png\") no-repeat bottom left";
  container.appendChild(div);

  var title = document.createElement("span");
  title.setAttribute('id', 'chooserTitle');
  title.innerHTML = 'Solar System';
  title.style.zIndex = 10;
  title.style.color = '#ffffff';
  title.style.fontWeight = 'bold';
  title.style.fontFamily = 'sans-serif';
  title.style.fontSize = '16px';
  title.style.position = 'absolute';
  title.style.top = '15px';
  title.style.left = '15px';
  div.appendChild(title);
  
  for (var j = 0; j < chooserJSPlanetInfo.length; j++) {
    var span = document.createElement("span");
    span.setAttribute('id', chooserJSPlanetInfo[j]['name'] + 'Title');
    span.innerHTML = chooserJSPlanetInfo[j]['text'];
    span.style.zIndex = 10;
    span.style.color = '#ffffff';
    span.style.fontWeight = 'bold';
    span.style.fontFamily = 'sans-serif';
    span.style.fontSize = '14px';
    span.style.position = 'absolute';
    span.style.display = 'none';
    span.style.top = chooserJSPlanetInfo[j]['titleTop'];
    span.style.left = chooserJSPlanetInfo[j]['titleLeft'];
    div.appendChild(span);
    var a = document.createElement("a");
    if (chooserJSURL[chooserJSPlanetInfo[j]['name']]) {
	a.setAttribute('href',	chooserJSURL[chooserJSPlanetInfo[j]['name']]);
    }		
    div.appendChild(a);
    var img = document.createElement("img");
    img.setAttribute('id', chooserJSPlanetInfo[j]['name']);
    img.src = ((chooserJSPath) ? chooserJSPath : '') + chooserJSPlanetInfo[j]['img'];
    img.style.zIndex = 10;
    img.style.position = 'absolute';
    img.style.height = chooserJSPlanetInfo[j]['height2'];
    img.style.width = chooserJSPlanetInfo[j]['width2'];
    img.style.top = chooserJSPlanetInfo[j]['top'];
    img.style.left = chooserJSPlanetInfo[j]['left'];
    img.style.border = "none";
    a.appendChild(img);
  }
  init_hovers();
};
