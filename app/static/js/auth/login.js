$(document).ready(function(){
  $('#loginForm').submit(function(event){
    email = $("#email").vall()
    password = $("#password").val()

    if ((email == null || "") || (password == null || "") ){
      $("#error").text("Please fill all fields").fadeIn(500).delay(5000).slideUp(500)
    }

    $.post('/login',
    {
      email:email,
      password:password,
    },
    function(data){
      if(data.success == true){
        window.replace.location('/')
      }
      if(data.success == false){
        $("#error").text('Invalid email or password').fadeIn(500).delay(5000).slideUp(500)
      }
    });
    event.preventDefault()
  });
});
