$(document).ready(function(){

  $("#signupForm").submit(function(event){
    username =$("#username").val()
    email =$("#email").val()
    password=$("password").val()
    confirm_password = $("#confirm_password").val()

    if ( (username == null || "") || (email == null || "") || ( password == null || "" ) || ( confirm_password == null || "") ){
      return $("#error").text("please fill all fields").fadeIn(500).delay(5000).slideUp(500)
    }

    if(password != confirm_password){
      return $("#confirm_error").text("Passwords dont match")
    }
    $.post('/signup',
    {
      username:username,
      email:email,
      password:password
    },
    function(data){
      if (data.email_err){
        return  $("email_error").text(data.email_err).fadeIn(500).delay(5000).slideUp(500)
      }
      if(data.username_err){
        return  $("username_error").text(data.username_err).fadeIn(500).delay(5000).slideUp(500)
      }
      if(data.success == true){
        window.location.replace('/')
      }
    });
    event.preventDefault()
  })

});
