$(document).ready(function(){
  $('#loginForm').submit(function(event){
    email = $("#email").vall()
    password = $("#password").val()

    if ((email == null || "") || (password == null || "") ){
    return $("#error").text("Please fill all fields").fadeIn(500).delay(5000).slideUp(500)
    }

    $.post('/login',
    {
      email:email,
      password:password,
    },
    function(data){
      if(data.success == true){
        window.location.replace('/')
      }
      if(data.success == false){
          return $("#error").text('Invalid email or password').fadeIn(500).delay(5000).slideUp(500)
      }
    });
    event.preventDefault()
  });
});
