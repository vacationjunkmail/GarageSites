$(document).ready(function() 
{
  $('.bulb-light').click(function() 
  {
    $('body').toggleClass('night');
    var body_class = $('body').attr('class');
    var route = 'relay_on';
    if (body_class != 'night')
    {
      route = 'relay_off';
    }

    $.ajax(
    {
      url: "/"+route+"/", success: function(result)
      {
        $("#light_title").text('Light '+result[0]);
      }
    });
        

  });
});
