// collapse navbar to drawer on mobile
(function($){
  $(function(){
    $('.button-collapse').sideNav();
  }); // end of document ready
})(jQuery);

// allow modals to be triggered
$(document).ready(function(){
  // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
  $('.modal-trigger').leanModal();
});

// get the csrf token and preprocess ajax requests so django doesn't complain about forged requests
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method){
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings){
    if(!csrfSafeMethod(settings.type) && !this.crossDomain){
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
