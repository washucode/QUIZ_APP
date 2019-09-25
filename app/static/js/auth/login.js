$(document).ready(function(){
  $('#loginForm').submit(function(event){
    email = $("#email").val()
    password = $("#password").val()

    $.post('/login',
    {
      email:email,
      password:password,
    },
    function(data){
      if(data.imeanguka){
        $("#error").text('Invalid email or password').fadeIn(500).delay(5000).slideUp(500)
      }
      if(data.awesome){
        window.location.replace('/')
      }

    });
    event.preventDefault()
  });
});
