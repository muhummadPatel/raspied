/* booking.js
 *
 * Handles interactions on the bookings page including async booking actions.
 */

var timepicker;
var datepicker;

// Initilaise the time and date pickers including disabling clots that have already
// been booked.
var init_booking_form = function(){
  // initialise the time and date picker components
  datepicker = $(".datepicker").pickadate({
    onSet: function(){
      update_disabled_timeslots();
      update_booking_form();
    },
    min: true
  });

  timepicker = $(".timepicker").pickatime({
    onSet: update_booking_form,
    interval: 60,
    format: "HH:i"
  });

  // Settup the booking form to clean up the data and post the booking requests
  $("#new-booking-form").on('submit', function(event){
    event.preventDefault();

    var date = $("#new-booking-date").val();
    var time = $("#new-booking-time").val();

    var datetime = date + " " + time;

    data = { datetime_str:  datetime};
    $.post("/students/booking/", data, function(response){
      Materialize.toast(response, 4000);

      update_booking_list();
      update_disabled_timeslots();

      timepicker.pickatime("picker").clear();
      datepicker.pickadate("picker").clear();
    }).fail(function(response){
      Materialize.toast("Sorry, failed! " + response.responseText, 4000);
    });
  });

  update_booking_form();
};

// Disables all the booked timeslots for the currently selected date
var update_disabled_timeslots = function(){
  // read the currently selected date
  var date = $("#new-booking-date").val();
  date = moment(new Date(date)).format("DD.MMMM.YYYY");

  if(date === "Invalid date"){
    return;
  }

  // get all the booked timeslots for the currently selected date adn disable them
  // in the time picker
  $.getJSON("/students/booking/listall/" + date + "/", function(bookings){
    if(bookings.length > 0){
      var booked_slots = [];
      $.each(bookings, function(index, booking){
        start_time = moment(booking.fields.start_time).format("H");
        booked_slots.push(start_time);
      });

      booked_slots = booked_slots.map(function(str){
        return parseInt(str);
      });

      timepicker.pickatime("picker").set("disable", false);
      timepicker.pickatime("picker").set("enable", true);
      timepicker.pickatime("picker").set("disable", booked_slots);
    }
  }).fail(function(){
    console.log("Failed to retrieve json for all bookings for date:" + date);
  });
};

// set up the list of user bookings
var init_booking_list = function(){
  update_booking_list();
  $("#user-bookings-list").on("click", ".secondary-content", delete_booking);
};

// update the booking form to enable/disable the submit button based on whether
// the date and time inputs have been populated
var update_booking_form = function(){
  var date = $("#new-booking-date").val();
  var time = $("#new-booking-time").val();

  $("#submit-new-booking").toggleClass("disabled", !(date && time));
  if(!(date && time)){
    $("#submit-new-booking").attr("disabled");
  }else{
    $("#submit-new-booking").removeAttr("disabled");
  }
};

// async update of the list of user bookings. Used after any booking additions
// and deletions to update the list of bookings.
var update_booking_list = function(){
  $("#user-bookings-list").empty();

  $.getJSON("/students/booking/list/", function(user_bookings){
    if(user_bookings.length === 0){
      help_text = "<li class=\"collection-item avatar\"><div><span class=\"subtext\" style=\"color:darkgrey;\">You have no upcoming bookings.</span></div></li>";
      $("#user-bookings-list").append(help_text);
    }else{
      $.each(user_bookings, function(index, booking){
        booking_id = booking.pk;
        date = moment(booking.fields.start_time).format("Do MMM YYYY");

        current_time = moment();
        start_time = moment(booking.fields.start_time);
        is_current = start_time.isBefore(current_time)? "current-booking": "";
        delete_icon = start_time.isBefore(current_time)? "": "<a id=\"delete-booking_" + booking_id + "\" href=\"#\" class=\"secondary-content\"><i class=\"material-icons md-18\">delete</i></a>";

        start_time = start_time.format("HH:mm");
        end_time = moment(booking.fields.end_time).format("HH:mm");
        booking_info = start_time + " - " + end_time;

        list_item_html = "<li class=\"collection-item avatar "+ is_current +" \"><div><span class=\"title\">" + date + "</span><p id=\"booking_" + booking_id + "\" class=\"subtext\">" + booking_info + "</p>" + delete_icon + "<div></li>";
        $("#user-bookings-list").append(list_item_html);
      });
    }
  }).fail(function(){
    Materialize.toast("Sorry, could not load your bookings", 4000);
  });
};

// deletes the required booking
var delete_booking = function(event){
  event.preventDefault();

  source_btn = $(this);
  booking_id = source_btn.attr("id").match(/\d+/g);
    if(booking_id.length === 0){
    Materialize.toast("Sorry, booking not found", 4000);
    return false;
  }else{
    booking_id = booking_id[0];
  }

  // POST to delete the specified booking
  $.post("/students/booking/" + booking_id + "/delete/", function(response){
    Materialize.toast("Successfully deleted booking", 4000);

    update_booking_list();
  }).fail(function(response){
    Materialize.toast("Could not delete booking", 4000);
  });
};

// initialises the booking form and the list of bookings when the page has
// completed loading
$(function(){
  init_booking_form();
  init_booking_list();
});
