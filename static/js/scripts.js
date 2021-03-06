
function message(status, shake=false, id="") {
  if (shake) {
    $("#"+id).effect("shake", {direction: "right", times: 2, distance: 8}, 250)
  } 
  document.getElementById('feedback').innerHTML = status
  $("#feedback").show().delay(2000).fadeOut()
}

function error(type) {
  $("."+type).css("border-color", "#E14448")
}

function showred(type) {
  $("#"+type).css("border-color", "#E14448");
}

var login = function() {
  $.post({
    type: "POST",
    url: "/",
    data: {"username": $("#login-user").val(), 
           "password": $("#login-pass").val()},
    success: function(response){
      var status = JSON.parse(response)['status']
      if (status === 'Login successful') {location.reload()}
      else {error('login-input')}}
  })
}

var submitqa = function() {
    $.post({
      type: "POST",
      url: "/addqa",
      data: {"question": $("#question").val(), 
             "answer": $("#answer").val(),
             "filename": $("#imgname").text()},
      success: function(response) {
        var status = JSON.parse(response)['status']
        if (status === 'QA successful') {location.reload()}
        else {message(status, shake=false, id="question"); showred('question') ;showred('answer')}
      }
    })
}



$(document).ready(function() {


  
  $(document).on("click", "#login-button", login)
  $(document).on("click", "#qa-button", submitqa)
  $(document).keypress(function(e) {if(e.which === 13) {login()}})
  $(document).keypress(function(e) {if(e.which === 13) {submitqa()}})
  
  $(document).on("click", "#signup-button", function() {
    $.post({
      type: "POST",
      url: "/signup",
      data: {"username": $("#signup-user").val(), 
             "password": $("#signup-pass").val(), 
             "email": $("#signup-mail").val()},
      success: function(response) {
        var status = JSON.parse(response)['status']
        if (status === 'Signup successful') {location.reload()}
        else {message(status, shake=true, id="signup-box")}
      }
    })
  })


  // $(document).on("click", "#qa-button", function() {
  //   $.post({
  //     type: "POST",
  //     url: "/addqa",
  //     data: {"question": $("#question").val(), 
  //            "answer": $("#answer").val(),
  //            "filename": $("#imgname").text()},
  //     success: function(response) {
  //       var status = JSON.parse(response)['status']
  //       if (status === 'QA successful') {location.reload()}
  //       else {message(status, shake=false, id="question"); showred('question') ;showred('answer')}
  //     }
  //   })
  // })

  $(document).on("click", "#next-button", function() {
    $.post({
      type: "GET",
      url: "/"
       
    });

	window.location = '/';

  })

  $(document).on("click", "#faq-button", function() {
    $.post({
      type: "GET",
      url: "/faq"
       
    });

	window.location = '/faq';

  })


  $(document).on("click", "#save", function() {
    $.post({
      type: "POST",
      url: "/settings",
      data: {"username": $("#settings-user").val(), 
             "password": $("#settings-pass").val(), 
             "email": $("#settings-mail").val()},
      success: function(response){
        message(JSON.parse(response)['status'])
      }
    })
  })
})
