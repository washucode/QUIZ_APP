$(document).ready(function(){
  $("#signupForm").submit(function(event){
    username =$("#username").val()
    email =$("#email").val()
    password=$("#password").val()
    confirm_password = $("#confirm_password").val()

    if ( (username == null || " ") || (email == null || " ") || ( password == null || " " ) || ( confirm_password == null || " ") ){
       $("#error").text("please fill all fields")
    }
    else if(password != confirm_password){
      $("#error").hide()
      $("#confirm_error").text("Passwords dont match")
    }

    $.post('/signup',
    {
      username:username,
      email:email,
      password:password
    },
    function(data){
      if (data.email_err){
        $("#error").hide()
        $("email_error").text(data.email_err).fadeIn(500).delay(5000).slideUp(500)
      }
      else if(data.username_err){
        $("#error").hide()
        $("username_error").text(data.username_err).fadeIn(500).delay(5000).slideUp(500)
      }
      else if(data.success == true){
        window.location.replace('/')
      }
      else{
        window.location.replace('/signup')
      }
    });
    event.preventDefault()
  })
});
