function notify(message, title){
  $("#notification").remove();
  msg = $("<div>").append(message).attr("id","notification");
  $("#notification-dialog").append(msg);
  if (title){
    $("#ui-dialog-title-notification-dialog").html(title);
  }
  else{
    $("#ui-dialog-title-notification-dialog").html("Notification Message");
  }
  $("#notification-dialog").dialog("open");
}

function run_instance_response(data){
  if (data.success != "true"){
    notify("There was an error with your request: " + data.error, "Error");
  }
  else{
    notify("Success! Instance id of: " + data.instance_id, "Notification");
  }
}

function post_run_instance(image_id){
  var type = $("#" + image_id + "-type").val();
  var key = $("#" + image_id + "-key").val();
  notify("Request sent <br/>Image:" + image_id + " <br/>Type: " + type + " <br/>Key: " + key + "<br/>Please wait...","Notification");
  $.post("/runpost", {'image_to_run':image_id, 'key_to_use':key, 
                              'instance_type':type}, run_instance_response,
                              "json"); 
}

function append_key_list(name){
  var item = $("<li>").html(name);
  $("#existing-keys").append(item);
}

function add_key_response(data){
  if (data.success != "true"){
    notify("There was an error with your request: " + data.error, "Error");
  }
  else{
    notify("Success! The key as been added");
    append_key_list(data.name);
  }
}

function terminal_response(data){
  if (data.success != "true"){
    notify("There was an error with your request: " + data.error, "Error");
  }
  else{
    notify("Success! A terminal has been opened.");
  }
}
function post_terminal_instance(ip, key){
  notify("Opening terminal...", "Notification");
  $.post("/viewpost", {'keyname':key,"public_ip":ip},terminal_response, "json");
}

function post_add_key(){
  var name = $("#keypair_name").val();
  notify("Adding key with name " + name  + ". Please wait...");
  $.post("/addkeypairpost", {'keyname':name}, add_key_response, "json");
}

function setup_notification_dialog(){
    var confirmed = function(){
      $("#notification-dialog").dialog("close");
    };

    var dialogOpts = {
      autoOpen: false,
      draggable: true,
      hide: 'fold',
      position: 'center',
      modal: true,
      buttons: {
        "Close": confirmed
      }
    };

    $("#notification-dialog").dialog(dialogOpts);
}

function init_euca(){
  setup_notification_dialog();
  $("#keypair_button").button();
}
