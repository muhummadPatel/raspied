var init_video_stream = function(){
  // Setup the WebSocket connection and start the player
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

var init_code_editors = function(){
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  editor.getSession().setMode("ace/mode/python");
  editor.getSession().setTabSize(4);
  editor.getSession().setUseSoftTabs(true);

  if($("#terminal-output").length > 0){
    var terminal_output = ace.edit("terminal-output");
    terminal_output.setTheme("ace/theme/monokai");
    terminal_output.setReadOnly(true);
    terminal_output.setShowPrintMargin(false);
    terminal_output.getSession().setMode("ace/mode/text");
    terminal_output.getSession().setTabSize(4);
    terminal_output.getSession().setUseSoftTabs(true);
  }
};

var init_buttons = function(){
  $("#download-script-btn").click(function(){
    var editor = ace.edit("editor");
    var user_script = editor.getValue();

    var blob = new Blob([user_script], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "raspied_script.py");
  });

  $("#new-script-btn").click(function(){
    var editor = ace.edit("editor").session;
    editor.setValue($("#boilerplate-data").html());
  });
};

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
      console.log("SENT KILL SIGNAL");

      return false;
    });

    $("[class*=script-btn]").toggleClass("disabled", false);
  }
};

$(function(){
  init_video_stream();
  init_code_editors();
  init_robot_terminal();
  init_buttons();
});
