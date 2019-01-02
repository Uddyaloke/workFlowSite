/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function myFunction (event, obj_id) {
  event.preventDefault()

  var x = document.getElementById('proceed-action-select-' + obj_id).selectedIndex
  var y = document.getElementById('proceed-action-select-' + obj_id).options

  var url = y[x].value

  if (url) {
    window.location.pathname = url
  } else {
    alert('Please Select Correct Action to Proceed')
    return false
  }
}
