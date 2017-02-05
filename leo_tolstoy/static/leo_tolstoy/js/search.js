$(document).ready(function(){

$('#main_submit').click(function(){

    $('#search_help').html('Пожалуйста ждите...');

});

$('#submit_but').click(function(){

    $('#search_hint').html('Пожалуйста ждите...');

});


$('.note').parent().css('cursor','pointer');

$('.note').parent().mouseover(function(){

    var number = $(this).children().text().split('[')[0];
    var language = $(this).text().split(number)[0];
    $(this).children().removeClass('hidden');
    if ($('#oldnew').css('display') == 'inline-block'){
        $(this).children('span.orig').addClass('hidden');
        $(this).children('span.reg').removeClass('hidden');
    }
    else{
        $(this).children('span.reg').addClass('hidden');
        $(this).children('span.orig').removeClass('hidden');
    }

});

$('.note').parent().mouseout(function(){

    $(this).children().addClass('hidden');
    if ($('#oldnew').css('display') == 'inline-block'){
        $(this).children('span.orig').addClass('hidden');
        $(this).children('span.reg').removeClass('hidden');
    }
    else{
        $(this).children('span.reg').addClass('hidden');
        $(this).children('span.orig').removeClass('hidden');
    }

});


var pages = $(".page_num");
console.log(pages);
$('body').append('<nav class="hidden-xs col-sm-2" id="myScrollspy"><ul id="nav_pages" '+
'class="nav nav-pills nav-stacked" data-spy="affix" data-offset-top="400"></ul></nav>');

$.each(pages, function(index, value){
   var page_id = $(pages[index]).text();
   console.log(page_id, typeof(page_id));
   $('#nav_pages').append('<li><a href="#'+page_id+'">'+page_id+'</a></li>');
});


$('#myglyphicon').click(function(){
    $('#myform').toggle();
    $('#myglyphicon').hide();
});


$('#clickme').click(function(){
    $('#myform').toggle();
    var row_html = 'Спасибо';
    $('#thanks').append(row_html);
});


$('#show_search').click(function(){
    $('#extra_search').toggle();
    if ($('#footer').hasClass('navbar-fixed-bottom')){
        $('#footer').removeClass('navbar-fixed-bottom');
    }
    else {
        $('#footer').addClass('navbar-fixed-bottom');
    }

    $('#search_form').toggle();

});

var cen3040 = [];
var cen5060 = [];
var cen70 = [];
var cen80 = [];
var cen90 = [];

$(".checkbox_year").each(function(i, obj){

    var ch_year = $(this).text().replace(/\s+/g, ''); /* real years */
    if (ch_year.charAt(1) == 9){
        cen90.push(ch_year);
    };
    if (ch_year.charAt(2) == 3 || ch_year.charAt(2) == 4){
        cen3040.push(ch_year);
    };
    if (ch_year.charAt(2) == 5 || ch_year.charAt(2) == 6){
        cen5060.push(ch_year);
    };

    if (ch_year.charAt(2) == 7 ){
        cen70.push(ch_year);
    };
    if (ch_year.charAt(2) == 8){
        cen80.push(ch_year);
    };

});

for (var i=0; i<cen3040.length; i++){
        $(".checkbox_year").each(function(){

            if ($(this).val() == cen3040[i]){ /* substring! */
                $(this).parents('.col-sm-3').css('display', 'block');
            }

        });
};

$('#but3040').click(function(){

    $(".checkbox_year").each(function(){
        $(this).parents('.col-sm-3').css('display', 'none');
    });

    for (var i=0; i<cen3040.length; i++){
        $(".checkbox_year").each(function(){

            console.log($(this).val(), cen3040[i]);
            if ($(this).val() == cen3040[i]){ /* substring! */
                console.log("3040 =>",$(this).val());
                $(this).parents('.col-sm-3').css('display', 'block');
            }

        });
    };
});


$('#but5070').click(function(){

    $(".checkbox_year").each(function(){
        $(this).parents('.col-sm-3').css('display', 'none');
    });

    for (var i=0; i<cen5060.length; i++){
        $(".checkbox_year").each(function(){

            if ($(this).val() == cen5060[i]){ /* substring! */
                $(this).parents('.col-sm-3').css('display', 'block');
            }
        });
    };

});

$('#but70').click(function(){

    $(".checkbox_year").each(function(){
        $(this).parents('.col-sm-3').css('display', 'none');
    });

    for (var i=0; i<cen70.length; i++){
        $(".checkbox_year").each(function(){

            if ($(this).val() == cen70[i]){ /* substring! */

                $(this).parents('.col-sm-3').css('display', 'block');
            }

        });
    };
});


$('#but80').click(function(){

    $(".checkbox_year").each(function(){
        $(this).parents('.col-sm-3').css('display', 'none');
    });

    for (var i=0; i<cen80.length; i++){
        $(".checkbox_year").each(function(){

            if ($(this).val() == cen80[i]){ /* substring! */

                $(this).parents('.col-sm-3').css('display', 'block');
            }

        });
    };
});

$('#but90').click(function(){

    $(".checkbox_year").each(function(){
        $(this).parents('.col-sm-3').css('display', 'none');
    });

    for (var i=0; i<cen90.length; i++){
        $(".checkbox_year").each(function(){

            if ($(this).val() == cen90[i]){ /* substring! */

                $(this).parents('.col-sm-3').css('display', 'block');
            }

        });
    };
});

});
