$(document).ready(function () {  
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