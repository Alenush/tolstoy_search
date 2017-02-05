/**
 * Created by alenush on 09.10.16.
 */
$(document).ready(function(){

/* Page up button  */

var amountScrolled = 300;

$(window).scroll(function() {
	if ( $(window).scrollTop() > amountScrolled ) {
		$('a.back-to-top').fadeIn('slow');
	} else {
		$('a.back-to-top').fadeOut('slow');
	}
});
/* animation to up button */
$('a.back-to-top').click(function() {
	$('html, body').animate({
		scrollTop: 0
	}, 700);
	return false;
});

$('#search_letters').click(function() {
        $('#letters_search').css('display','block');
        $('#search_texts').css('display', 'none');
});
$('#search_text').click(function() {
        $('#letters_search').css('display','none');
        $('#search_texts').css('display', 'block');
});

if($("#search_text").attr("checked") == 'checked'){
    $('#search_big_input').attr('readonly', false);
};
if($("#search_letters").attr("checked") == 'checked'){
    $('#search_big_input').attr('readonly', true);
};

$('#search_meta').click(function(){
    console.log('META!');
    $('#search_hint').text('Поиск по метаданным');
    $('#search_big_input').attr('readonly', true);
});
$('#search_txt').click(function(){
    console.log('TEXTS');
    $('#search_hint').text('Поиск по текстам');
    $('#search_big_input').attr('readonly', false);
});


});
