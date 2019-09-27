$(document).ready(function(){

  $("#signupForm").submit(function(event){
    username =$("#username").val()
    email =$("#email").val()
    password=$("#password").val()
    confirm_password = $("#confirm_password").val()
    $.post('/signup',
    {
      username:username,
      email:email,
      password:password,
      confirm_password :confirm_password
    },
    function(data){
      if(data.pwd_err){
        $("#password_error").text(data.pwd_err).fadeIn(500)
        $("#password").css('border','1px solid red')
        $("#confirm_password").css('border','1px solid red')
      }else{
        $("#confirm_password").css('border','1px solid lightgray')
        $("#password").css('border','1px solid lightgray')
      }
      if (data.email_err){
        console.log('lsjalsdjalkdjaslkdjaskldjlaksjklasjdklasjkldjaskl');
        $("#email_error").text(data.email_err).fadeIn(500).delay(5000).slideUp(500)
        $("#email").css({'border':'solid 1px red'})
      }else{
        $("#email").css({'border':'solid 1px lightgray'})
      }
       if(data.username_err){
        $("#error").hide()
        $("#username_error").text(data.username_err).fadeIn(500).delay(5000).slideUp(500)
        $("#username").css({'border':'solid 1px red'})

      }else{
        $("#username").css({'border':'solid 1px lightgray'})
      }
      if(data.awesome){
        window.location.replace('/login')
      }
    });
    event.preventDefault()
  })

});
