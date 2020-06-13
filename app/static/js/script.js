var togglepost = function(e) {
  var more = e.querySelector(".more");

  $(more).slideToggle();
}

var layoutPicker = document.getElementById("layout");
var cssfile = localStorage.getItem('cssfile') || '../static/css/comfortable.css';
document.getElementById("style").setAttribute("href", cssfile);
if (cssfile === '../static/css/comfortable.css') {
  document.getElementById("comfortable").selected = true;
  document.getElementById("compact").selected = false;
} else {
  document.getElementById("compact").selected = true;
  document.getElementById("comfortable").selected = false;
}


var changecss = function(e) {
  if (e.target.value === "compact") {
    localStorage.setItem('cssfile', '../static/css/compact.css');
  } else {
    localStorage.setItem('cssfile', '../static/css/comfortable.css');
  }

  cssfile = localStorage.getItem('cssfile');
  document.getElementById("style").setAttribute("href", cssfile);
}

layoutPicker.addEventListener('change', changecss);
