
$("a[href^='#']").on('click', function(e) {
    e.preventDefault();
    var hash = this.hash;
    if (hash != '') {
	$('html, body').animate({
	    scrollTop: $(hash).offset().top
	}, 300, function(){
	    window.location.hash = hash;
	});
    }
});

$(document).ready(function() {
    $('[data-toggle="popover"]').popover();

    $(".link-details a[href^='#']").hide();
    $(".link-stars a[href^='#']").hover(function(e) {
	$(".link-details a[href^='#']").hide();
	$(".link-details a[href=" + $(this).attr('href') + "]").show();
    });

    $('.link-stars-side a .name').hide();
    $('.link-stars-side a .btn').hover(function() {
	$('.link-stars-side a .name').hide();
	$(this).parent().find('.name').show();
    }, function() {
	$(this).parent().find('.name').hide();
    });

    $('.mainhome').css('min-height', $(window).height() - $('.navbar-Smile').height());

    $('.link-stars-side').hide();
    $(window).scroll(
	function () {
	    if (($(window).scrollTop() + $(window).height())
		>= $("#home").height() + $('.bg-Rainbow-1').height() + $('.navbar-Smile').height()) {
		$('.link-stars-side').show();
	    } else {
		$('.link-stars-side').hide();
	    }
	    if ($('#activities').html() == ''
		&& ($(window).scrollTop() + $(window).height())
		>= $("#home").height() + $('.navbar-Smile').height() - $('.social-section').height()) {
		$('#activities').text('Loading...');
		$.get('/ajax/activities/', function(data) {
		    $('#activities').html(data);
		    loadMoreActivities($('#activities'));
		});
	    }
	});
    $('.navbar-fixed-top').on('activate.bs.scrollspy', function () {
	var currentItem = $(".nav li.active > a").attr('href');
	if (currentItem == '#page-top') {
	    $('.navbar-fixed-top').fadeOut();
	} else {
	    $('.navbar-fixed-top').fadeIn();
	}
    })
});
