
$(document).ready(function () {  

    var vis = $('#alert1').attr('visible')
    
    if(vis == -1){
        
    } else if (vis == 1){
        $('#alerts').css('height', '40px');
        $('#alert1').css('height', '40px');
        $('#alert1').css('visibility', 'visible');
        $('#alert1').hide(2000, function(){
            //$('#alerts').css('height', '0px');
        })
        
        //$('#alert1').css('visibility', 'visible')
        //$('#alert1').hide(2000)
        //$('#alert1').hide()
        //$('#alert2').attr('visibility') = 'hidden'
    } else{
        //$('#alert2').css('visibility', 'visible')
        //$('#alert2').hide(2000)
    }

    (function(){  
        var insertOptions = function(data, id) {  
            var result = new Array();  
            $.each(data, function(i, item){  
                result.push(item.name);  
            });  
            //alert(result.toString()); 
            console.log(result.toString());
            $('#search-com').autocomplete({  
                source: result  
            });  
        }  

        $('#search-com').keyup(function(){  
            var right_id = "search-com";  
            var url = "/search-com";//+$("#search-com").val();  
            var skeyword = $("#search-com").val();

            if(skeyword.length > 0){
                $.get({
                    url: url,
                    data: {"s": skeyword},
                    success: function (data) {
                        console.log(typeof(data));
                        insertOptions(eval(data), right_id);
                    }

                });
            }
        });  

    })();  
}); 