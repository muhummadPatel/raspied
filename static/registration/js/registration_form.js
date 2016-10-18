$(function(){
  var passwordHelpText = "<p class=\"help\">The password must contain at least 8 characters and cannot be entirely numeric.</p>";
  $(".input-field > input#id_password1").parent().append(passwordHelpText);
});
