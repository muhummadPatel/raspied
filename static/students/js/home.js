/* home.js
 *
 * Handles interactions on the home page and sets up the code editor and
 * websocket connections to the robot terminal and video stream.
 */

// Sets up the connection to the live video stream server using the streaming
// server address sent to the template by django.
var init_video_stream = function(){
  // Setup the WebSocket connection and start the player
  // NOTE: streaming server ip is inserted into the homa page template when it is
  // rendered on the server side
  var client = new WebSocket("ws://" + streaming_server_ip + ":8084/");

  client.onclose = function(){
    $("#video-help").text("Live video stream of the robot disconnected");
  };
  client.onerror = function(){
    $("#video-help").text("Could not connect to the live video stream of the robot");
  };

  // Don't do a jquery lookup for canvas. We need the actual element, not a jquery object
  var canvas = document.getElementById("videoCanvas");
  var player = new jsmpeg(client, {canvas: canvas});
};

// Sets up the code editor and the output terminal ace editors
var init_code_editors = function(){
  // set up the custom autocompletion for the Robot API functions
  var langTools = ace.require("ace/ext/language_tools");

  var custom_completer = {
    getCompletions: function(editor, session, pos, prefix, callback) {
      var word_data = {
        "Robot()":                  "Robot constructor",
        "forward()":                "Move forward x blocks",
        "reverse()":                "Reverse x blocks",
        "left()":                   "Turn left x steps",
        "right()":                  "Turn right x steps",
        "stop()":                   "Stops the robot",
        "follow_path(path)":        "Follow the given path x",
        "pathfind([x, y])":         "Move robot to position x",
        "get_position()":           "Get robot's current x,y co-ord",
        "get_rotation()":           "Get robot's current rotation",
        "add_obstacles(obs)":       "Add obstacles to grid",
        "reset_obstacles()":        "Clear virtual obstacles",
        "find_path(a, b)":          "Get path between a and b",
        "get_start_pos()":          "Return the starting position",
        "get_start_rot()":          "Return the starting rotation",
        "print_grid()":             "Print the grid (showing obstacles)",
        "camera.detect_colour()":   "Return colour of the current block",
        "ir.detect_obstacle()":     "Detects if an obstacle is in front of Robot",
        "ir.wait_for_obstacle()":   "Returns True when an obstacle is detected",
        "us.get_distance()":        "Returns distance to nearest object in cm",
        "led.red_on()":             "Turn on red LED",
        "led.blue_on()":            "Turn on blue LED",
        "led.yellow_on()":          "Turn on yellow LED",
        "led.red_off()":            "Turn off red LED",
        "led.blue_off()":           "Turn off blue LED",
        "led.yellow_off()":         "Turn off yellow LED",
        "led.red_flash()":          "Flash red LED",
        "led.blue_flash()":         "Flash blue LED",
        "led.yellow_flash()":       "Flash yellow LED",
      };

      callback(null, Object.keys(word_data).map(function(word) {
        return {
          caption: word,
          value: word,
          meta: word_data[word]
        };
      }));
    }
  };

  // set up the python code editor
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  editor.getSession().setMode("ace/mode/python");
  langTools.setCompleters([custom_completer]);
  editor.setOptions({
      enableBasicAutocompletion: true,
      enableSnippets: false,
      enableLiveAutocompletion: true
  });
  editor.getSession().setTabSize(4);
  editor.getSession().setUseSoftTabs(true);

  // set up the output terminal
  if($("#terminal-output").length > 0){
    var terminal_output = ace.edit("terminal-output");
    terminal_output.setTheme("ace/theme/monokai");
    terminal_output.setReadOnly(true);
    terminal_output.setShowPrintMargin(false);
    terminal_output.getSession().setMode("ace/mode/text");
    terminal_output.getSession().setTabSize(4);
    terminal_output.getSession().setUseSoftTabs(true);
  }

  // populate the code editor with the cached user script (if it exists), or the
  // default boilerplate code.
  var cached_user_script = localStorage.getItem("cached_user_script_" + username);
  if(cached_user_script){
    editor.setValue(cached_user_script);
    editor.focus();
    editor.gotoLine(0);
  }else{
    editor.setValue($("#boilerplate-data").html());
    editor.focus();
    editor.gotoLine(0);
  }
};

// initialise the row of buttons above the editor and attach the required
// event listeners/handlers.
var init_buttons = function(){
  $("#download-script-btn").click(function(){
    var editor = ace.edit("editor");
    var user_script = editor.getValue();

    var filename = "raspied_script.py";
    swal({
      title: "Save as",
      text: "Please enter the filename (with a .py extension)::",
      type: "input",
      showCancelButton: true,
      closeOnConfirm: false,
      animation: "slide-from-bottom",
      inputPlaceholder: "raspied_script.py"
    }, function(input){
      if(input === false){
        console.log("returning false");
        return false;
      }
      if(input !== ""){
        filename = input;
      }

      var blob = new Blob([user_script], {type: "text/plain;charset=utf-8"});
      saveAs(blob, filename);
      swal.close();
    });
  });

  $("#new-script-btn").click(function(){
    var editor = ace.edit("editor").session;
    editor.setValue($("#boilerplate-data").html());
    localStorage.removeItem("cached_user_script_" + username);
  });

  $("#file-upload-form").on("submit", function(event){
    event.preventDefault();

    var file = document.getElementById("file-input").files[0];
    var reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function() {
      var editor = ace.edit("editor").session;
      editor.setValue(this.result);
    };
  });
};

// Opens a websocket connection to the robot terminal and sets up handlers to
// help display data received over this websocket conenction.
var init_robot_terminal = function(){
  if($("#terminal-output").length < 1){
    $("#robot-help").show();

  }else{
    var ws_path = "ws://" + window.location.host + "/robot_terminal/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    socket.onmessage = function(message){
      var data = JSON.parse(message.data);

      if(data.error){
        Materialize.toast(data.error, 4000);
        return;
      }

      if(data.join){
        console.log("Robot terminal socket: terminal opened");

      }else if(data.leave){
        console.log("Robot terminal socket: terminal closed");

        $("#terminal-output").remove();
        Materialize.toast("Connection to robot closed", 4000);

      }else if(data.code_done){
        ace.edit("terminal-output").getSession().insert({
            row: ace.edit("terminal-output").getSession().getLength(),
            column: 0
          }, data.message);


          Materialize.toast("Program ended, now resetting the robot", 6000);
      }else if(data.message){
        ace.edit("terminal-output").getSession().insert({
            row: ace.edit("terminal-output").getSession().getLength(),
            column: 0
          }, data.message);
      }else{
        console.log("Robot terminal socket: Undefined message received");
      }
    };

    socket.onopen = function(){
      console.log("Robot terminal socket: socket connected");

      socket.send(JSON.stringify({
        "command": "join",
        "robot": $("#terminal-output").attr("data-robot-id")
      }));
    };

    socket.onclose = function(){
      console.log("Robot terminal socket: socket disconnected");
    };

    $(".run-script-btn").on("click", function(){
      ace.edit("terminal-output").getSession().setValue("");

      var editor = ace.edit("editor");
      var user_script = editor.getValue();

      socket.send(JSON.stringify({
        "command": "send",
        "robot": $("#terminal-output").attr("data-robot-id"),
        "message": user_script
      }));

      $("ul.tabs").tabs("select_tab", "output-tab");

      return false;
    });

    $("#kill-script-btn").on("click", function(){
      socket.send(JSON.stringify({
        "command": "kill",
        "robot": $("#terminal-output").attr("data-robot-id"),
        "message": "kill user script"
      }));

      return false;
    });

    $("[class*=script-btn]").toggleClass("disabled", false);
  }
};

// store the current contents of the code editor in localstorage so the user
// doesn't lose their work if they refresh the page or logout.
var cache_script = function(){
  var editor = ace.edit("editor");
  var user_script = editor.getValue();
  localStorage.setItem("cached_user_script_" + username, user_script);
};

// cahches the user script after every interval of millis.
var schedule_user_script_caching = function(millis){
  window.setInterval(function(){
    cache_script();
  }, millis);
};

// Run the required setup functions once the document has completed rendering.
$(function(){
  init_video_stream();
  init_code_editors();
  init_robot_terminal();
  init_buttons();
  schedule_user_script_caching(10000);
});
