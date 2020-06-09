var togglepost = function(e) {
  var more = e.querySelector(".more");

  $(more).slideToggle();
}

var confirmbox = function(e) {
  console.log("Class ID: " + e.getAttribute("classid"));

  if (confirm("Are you sure?")) {
    console.log("Hid class!");
  } else {
    return false;
  }

}
