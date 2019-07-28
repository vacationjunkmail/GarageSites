//beginning on main function
$(function() 
{
	$('#garage_form_row').hide();
	//$('#usertable').hide();
	removeClass();
	
	$('#left_door,#right_door').on("click", function(event) 
    {
		event.preventDefault();
        //removeClass();
        $('#garage_form_row').show();
        $('#which_door').val(this.id);
        //$("#"+this.id+"_image").attr("src","/static/images/garage_clipart_empty_garage.png");
    });
    
    $('#sub_gar_btn').on("click", function () 
    {
        d = $('#which_door').val();
        p = $('#pwd').val();
        if(parseInt(d.length)==0 || parseInt(p.length)==0)
        {
			d2 = d.replace("_"," ");
            $("#message").addClass("alert alert-danger");
            $("#message").html('Your password is empty and the '+d2+' will not open.').fadeIn('fast').delay(5000).fadeOut('fast');
            
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
                    var image_state = $("#"+d+"_image").attr("src");
                    var image_regex = /close_/g;
                    if(image_state.match(image_regex))
                    {
						$("#"+d+"_image").attr("src","/static/images/open_garage.png");
					}
					else
					{
						$("#"+d+"_image").attr("src","/static/images/close_garage.png");
					}					
                }
                $("#message").html(result.msg).fadeIn('fast').delay(5000).fadeOut('fast');               
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
	
	$("#forgot").click(function(event){
		//$("p").toggle();
		event.preventDefault();
		$('#usertable').toggle();
	});
	
    $('#camera').on("click", function (event) 
    {
		$('#camera').hide();
		event.preventDefault();
        removeClass();
        $("#message").html('Taking Photo').addClass("alert alert-info");
        $.ajax(
        {
            url: "/camera/", success: function(result)
            {
				removeClass();
                successClass();
                $("#message").html(result.msg).fadeIn('fast').delay(6000).fadeOut('fast');
                var img = '<img src="/static/'+result.pic+'">';
                $('#showimage').append(img);
                $('#showimage').fadeIn('fast').delay(8000).fadeOut('fast');
                $('#camera').show();
            }
        });                
    });	
	function successClass()
	{
		$("#message").addClass("alert alert-success");
	}

	function removeClass()
	{
		$("#message").removeClass();
		$('#showimage').empty();
		$('#showimage').hide();
		$('#garage_form_row').hide();
		$('#usertable').hide();
	}

});



