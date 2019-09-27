$(document).ready(function(){


  $("#edit").click(function(){
    $("#edit").hide()
    $("#user_biom").slideToggle(300)
    $("#edit-bio").slideToggle(300)
    $("#close").show()
  })
  $("#close").click(function(){
    $("#close").hide()
    $("#user_biom").slideToggle(300)
    $("#edit-bio").slideToggle(300)
    $("#edit").show()
  })

  $("#edit-bio").submit(function(event){
    $.post('/profile/edit/bio/'+$("#user_id").val()+'',
    {
      changeBio:$("#changeBio").val()
    },
    function(data){
      if(data.passed){
        $("#msg").text(data.passed)
        $("#my_msg").fadeIn(200).delay(2000).fadeOut(200)
        $("#change-bio").val(data.success)
        $("#user_biom").text(data.success)
        $("#close").hide()
        $("#user_biom").slideToggle(300)
        $("#edit-bio").slideToggle(300)
        $("#edit").show()
      }
    }

    )
    event.preventDefault()
  });
  $("#new_password").click(function(){
    $("#after-pwd").slideDown(700)
  })

   $("#new_password_confirm").click(function(){
     $("#after-pwd_conf").fadeIn(700)
   })
   $("#change-password").submit(function(event){
    
     $.post('/profile/change/pwd/'+$("#user_id").val()+'',
      {
        former_password:$('#former_password').val(),
        new_password:$('#new_password').val(),
        confirm_new_password:$('#new_password_confirm').val()
      },
      function(data){
        if(data.invalid){
            $('#pwd_error').text(data.invalid)
            $("#former_password").css({'border':'solid 1px red','border-width':'0 0 1px 0'})
        }else{
            $('#pwd_error').text('')
          $("#former_password").css({'border':'solid 1px white','border-width':'0 0 1px 0'})
        }
        if (data.notmatch){
          $("#pwd_conf_error").text(data.notmatch)
          $('#new_password_confirm').css({'border':'solid 1px red','border-width':'0 0 1px 0'})
        }else {
          $("#pwd_conf_error").text('')
          $('#new_password_confirm').css({'border':'solid 1px white','border-width':'0 0 1px 0'})

        }
        if(data.equalToOld){
          $("#main_error").text(data.equalToOld)
          $("#former_password").css({'border':'solid 1px red','border-width':'0 0 1px 0'})
          $("#new_password").css({'border':'solid 1px red','border-width':'0 0 1px 0'})
        }else{
          $("#main_error").text('')
          $("#former_password").css({'border':'solid 1px white','border-width':'0 0 1px 0'})
          $("#new_password").css({'border':'solid 1px white','border-width':'0 0 1px 0'})
        }
        if(data.changed){
          $("#msg").text(data.changed)
          $("#my_msg").fadeIn(200).delay(2000).fadeOut(200)
          $('#former_password').val("")
          $('#new_password').val("")
          $('#new_password_confirm').val("")
          $("#after-pwd").hide()
           $("#after-pwd_conf").hide()

        }
      });
      event.preventDefault()
   });


   $("#new-bio").submit(function(event){

     $.post('/profile/bio/'+$("#user_id").val()+'',
     {
       bio:$('#bio').val()
     },
     function(data){
       if(data.success){
         $('#final_bio').text(data.success)
         $("#new-bio").hide()
       }
     });
     event.preventDefault()
   });

});
