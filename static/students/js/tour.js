$(function(){
  var tour = {
    id: "raspied-tour",
    steps: [
      {
        title: "Welcome to the RASPIED website!",
        content: "This tour will walk you through how to use the website to interact with the RASPIED robot. Let's get started! :)",
        target: document.querySelector("#logo-container.brand-logo"),
        placement: "bottom"
      },
      {
        title: "This is your home page",
        content: "This is where you can write code for the robot, upload code to the robot, and view a live video stream of the robot as it runs your code.",
        target: document.querySelector("#nav-home"),
        placement: "bottom"
      },
      {
        title: "This is the code editor tab",
        content: "All the tools for writing and uploading code are in this tab.",
        target: document.querySelector("#editor-tab-link"),
        xOffset: "center",
        placement: "bottom"
      },
      {
        title: "Code editor",
        content: "Your python code goes here. You can type the code in yourself, paste in some code, or even upload a file that you have saved on your computer.",
        target: document.querySelector("#editor"),
        placement: "top"
      },
      {
        title: "View the docs",
        content: "This will open the docs for the RASPIED robot in a new tab. The docs contain tutorials, FAQ's, and comprehensive documentation of the RASPIED robot library.",
        target: document.querySelector("#view-wiki-btn"),
        placement: "bottom"
      },
      {
        title: "Open an existing script",
        content: "This button will allow you to load any python script that you have saved on your computer. Once you have selected and uploaded the script, it will appear in the code editor below and you will then be able to edit it and/or run it on the robot.",
        target: document.querySelector("#open-script-btn"),
        placement: "bottom"
      },
      {
        title: "Save your script",
        content: "This button will download the the script currently in the code editor. This is useful if you want to save your work.",
        target: document.querySelector("#download-script-btn"),
        placement: "bottom"
      },
      {
        title: "Run your script!",
        content: "Clicking this button will upload the script in the code editor to the robot and run it. Note that this button will only be enabled if you have the current booking to use the robot.",
        target: document.querySelector("#run-script-btn"),
        placement: "bottom",
        onNext: function(){
          $("ul.tabs").tabs("select_tab", "output-tab");
        }
      },
      {
        title: "This is the output tab",
        content: "Here you can see a live video stream of the robot and view the output of the code that you run on the robot.",
        target: document.querySelector("#output-tab-link"),
        placement: "bottom"
      },
      {
        title: "Say hello to the RASPIED robot!",
        content: "This is a live video stream of the RASPIED robot.",
        target: document.querySelector("#video-help"),
        xOffset: "center",
        placement: "bottom"
      },
      {
        title: "Code output",
        content: "Any output from code that you run on the robot will be shown here.",
        target: document.querySelector("#terminal-output"),
        placement: "top"
      },
      {
        title: "Before you jump right in...",
        content: "You need to make a booking in order to upload code to the robot. You are allowed to make up to 5 bookings per month and each booking lasts for 1 hour.",
        target: document.querySelector("#nav-booking"),
        placement: "bottom",
        multipage: true,
        onNext: function(){
          window.location = window.location.href.replace("home", "booking");
        }
      },
      {
        title: "These are your upcoming bookings",
        content: "Any upcoming bookings that you have made are shown here.",
        target: document.querySelector("#user-bookings-card"),
        placement: "bottom"
      },
      {
        title: "Make a new booking",
        content: "To make a new booking, simply select the date and time that you wish to book and click the 'Make Booking' button. Your new booking should then appear in your list of upcomming bookings.",
        target: document.querySelector("#submit-new-booking"),
        placement: "bottom"
      },
      {
        title: "One more thing",
        content: "Remember to logout when you're done ;)",
        target: document.querySelector("#nav-logout"),
        placement: "bottom"
      },
      {
        title: "Now you're ready to go",
        content: "You can start by making a booking and then try writing and uploading some code to the robot. Have fun! :D",
        target: document.querySelector("#submit-new-booking"),
        placement: "bottom"
      }
    ]
  };

  if(window.location.href.includes("home")){
    $("#take-tour-btn").click(function(){
      hopscotch.startTour(tour);
    });

    if(is_first_login === true){
      hopscotch.startTour(tour);
    }
  }else if(window.location.href.includes("booking")){
    if (hopscotch.getState() === "raspied-tour:12") {
      hopscotch.startTour(tour);
    }
  }
});
