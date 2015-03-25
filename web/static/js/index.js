
$("a[href^='#']").on('click', function(e) {
    e.preventDefault();
    var hash = this.hash;
    if (hash != '' && hash.indexOf('Modal') < 0) {
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
    $('.home-section').css('min-height', $(window).height());

    $('.link-stars-side').hide();
    $(window).scroll(
	function () {
	    if (($(window).scrollTop() + $(window).height())
		>= $("#home").height() + $('.bg-Rainbow-1').height() + $('.navbar-Smile').height()
		&& ($(window).scrollTop() + $(window).height())
		<= $("#home").height() + $('.navbar-Smile').height() + $('#links').height() + 100) {
		$('.link-stars-side').show();
	    } else {
		$('.link-stars-side').hide();
	    }
	    if ($('#activities .activities').html() == ''
		&& ($(window).scrollTop() + $(window).height())
		>= $("#home").height() + $('.navbar-Smile').height() + $('#links').height()) {
		$('#activities .activities').text('Loading...');
		$.get('/ajax/activities/', function(data) {
		    $('#activities .activities').html(data);
		    loadMoreActivities($('#activities .activities'));
		});
		if ($('#myactivities').length > 0) {
		    $('#myactivities .activities').text('Loading...');
		    $.get('/ajax/feed/', function(data) {
			$('#myactivities .activities').html(data);
			loadMoreActivities($('#myactivities .activities'), undefined, true);
		    });
		}
	    }
	    if (($(window).scrollTop() + $(window).height())
		>= $(".mainhome").height() - $('.mainhome .events').height() + $('.navbar-Smile').height() && !$('.mainhome .events').hasClass('loaded')) {
		$('.mainhome .events').addClass('loaded');
		$.getJSON('http://schoolido.lu/contest/json/current', function(data) {
		    if (data['current'] == true) {
			var event = $('.mainhome .events .event').first();
			event.css('background-image', 'url(\'/static/currentcontest.png\')');
			event.find('span').text(data['name']);
			event.find('small').text(data['begin'] + ' ' + data['end']);
			event.attr('href', '/contest/contest');
		    }
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
