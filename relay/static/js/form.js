//beginning on main function
$(function() 
{
    $('#garage_form_row').hide();
    removeClass();
    
    $('#left_door,#right_door').on("click", function () 
    {
        removeClass();
        $('#garage_form_row').show();
        $('#which_door').val(this.id);
    });
    
    $('#sub_gar_btn').on("click", function () 
    {
        removeClass();
        d = $('#which_door').val();
        p = $('#pwd').val();
        if(parseInt(d.length)==0 || parseInt(p.length)==0)
        {
            $("#message").addClass("alert alert-danger");
            $("#message").html('Your password is empty or you are not opening a door.').fadeIn('fast').delay(5000).fadeOut('fast');
            
            return false;
        }
        
        //do ajax stuff
        $.ajax(
        {
            url:'/garage_door/', 
            data:$('#garage_form').serialize(),
            type:'POST',
            success: function(result)
            {
                if(result.error)
                {
                    $("#message").addClass("alert alert-danger");
                }
                else
                {
                    successClass();
                }
                $("#message").html(result.msg).fadeIn('fast').delay(5000).fadeOut('fast');
                
                //console.log(result.error)
            },
            error: function(error)
            {
                console.log(error);
            }
        });
        //after ajax call
        
        $('#which_door').val("");
        $('#pwd').val("");
        $('#garage_form_row').hide();
    });    
    
    $('#on_btn').on("click", function () 
    {
        removeClass();
        $.ajax(
        {
            url: "/relay_on/", success: function(result)
            {
                successClass();
                $("#message").html('Lamp is '+result).fadeIn('fast').delay(5000).fadeOut('fast');
            }
        });
    });
    
    $('#off_btn').on("click", function () 
    {
        removeClass();
        $.ajax(
        {
            url: "/relay_off/", success: function(result)
            {
                successClass();
                $("#message").html('Lamp is '+result).fadeIn('fast').delay(5000).fadeOut('fast');
            }
        });                
    });

    $('#camera').on("click", function () 
    {
        removeClass();
        $.ajax(
        {
            url: "/camera/", success: function(result)
            {
                successClass();
                $("#message").html(result.msg).fadeIn('fast').delay(5000).fadeOut('fast');
                var img = '<img src="/static/'+result.pic+'">';
                $('#showimage').append(img);
                $('#showimage').fadeIn('fast').delay(5000).fadeOut('fast');;
            }
        });                
    });    
           
    $('#forgot').on("click", function () 
    { 
        $('#usertable').show();
    });
    
    function removeClass()
    {
        $("#message").removeClass();
        $('#showimage').empty();
		$('#showimage').hide();
		$('#garage_form_row').hide();
        $('#usertable').hide();
    }
    
    function successClass()
    {
        $("#message").addClass("alert alert-success");
    }
});//end of main function
