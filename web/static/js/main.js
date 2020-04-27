
$.fn.removeClassPrefix = function(prefix) {
    this.each(function(i, el) {
	var classes = el.className.split(" ").filter(function(c) {
	    return c.lastIndexOf(prefix, 0) !== 0;
	});
	el.className = $.trim(classes.join(" "));
    });
    return this;
};

function getInterfaceColor() {
    return $('body').attr('class').replace('interface-', '');
}

$('a.page-scroll').bind('click', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
	scrollTop: $($anchor.attr('href')).offset().top
    }, 1500, 'easeInOutExpo');
    event.preventDefault();
});

$("#togglebutton").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function freeModal(title, body, buttons) {
    $('#freeModal .modal-header h4').html(title);
    $('#freeModal .modal-body').html(body);
    $('#freeModal .modal-footer').html('<button type="button" class="btn btn-Smile" data-dismiss="modal">Go</button>');
    if (buttons === 0) {
	$('#freeModal .modal-footer').hide();
    } else if (typeof buttons != 'undefined') {
	$('#freeModal .modal-footer').html(buttons);
	$('#freeModal .modal-footer').show();
    }
    $('#freeModal').modal('show');
}

function globalModal(hash, modal_size) {
    if (hash == 'donate') {
	window.location.href = "/donate/";
	return;
    }
    if (hash == 'about') {
	window.location.href = "/about/";
	return;
    }
    if (typeof modal_size == 'undefined') {
	if (hash == 'tutorialaddcard'
	    || hash == 'aboutllsif'
	    || hash == 'aboutsukutomo'
	   ) {
	    modal_size = 'lg'
	}
    }
    $.get('/ajax/modal/' + hash +
	  '/?interfaceColor=' + getInterfaceColor(), function(data) {
	      $('#modal .modal-content').html(data);
	      $('#modal .modal-dialog').removeClass('modal-lg');
	      $('#modal .modal-dialog').removeClass('modal-sm');
	      if (typeof modal_size != 'undefined') {
		  $('#modal .modal-dialog').addClass('modal-' + modal_size);
	      }
	      $('#modal').modal('show');
	      modalHandler();
	  });
}

function updateActivities() {
    $('[href="#imgur"]').off('click');
    $('[href="#imgur"]').click(function(e) {
	e.preventDefault();
	freeModal('<br>', '<img src="http://i.imgur.com/' + $(this).data('imgur') + '.png" class="img-responsive">');
	return false;
    });
    $('.activity .message.need-to-autolink').each(function() {
	$(this).html(Autolinker.link($(this).html(), { newWindow: true, stripPrefix: true } ));
	$(this).removeClass('need-to-autolink');
    });
    $('.likeactivity').off('submit');
    $('.likeactivity').submit(function(e) {
	e.preventDefault();
	$(this).ajaxSubmit({
	    context: this,
	    success: function(data) {
		if (data == 'liked') {
		    $(this).find('input[type=hidden]').prop('name', 'unlike');
		} else {
		    $(this).find('input[type=hidden]').prop('name', 'like');
		}
		var value = $(this).find('button[type=submit]').html();
		$(this).find('button[type=submit]').html($(this).find('button[type=submit]').attr('data-reverse'));
		$(this).find('button[type=submit]').attr('data-reverse', value);
	    },
	    error: function() {
		alert('Oops! Something bad happened. Try again.');
	    }
	});
    });
    $.each(['markhot', 'removehot', 'bump', 'drown'], function(_, btn) {
	$('a[href="#' + btn + '"]').unbind('click');
	$('a[href="#' + btn + '"]').click(function(e) {
	    e.preventDefault();
	    var button = $(this);
	    $.ajax({
		type: 'POST',
		url: '/ajax/' + btn + '/',
		data: {
		    'activity': button.closest('form').data('activity-id'),
		},
		success: function(data) {
		    button.text('OK');
		},
		error: genericAjaxError,
	    });
	    return false;
	});
    });
}

function genericAjaxError() {
    alert('Oops! Something bad happened. Try again.');
}

function isStaffFromStatus(status) {
    return status == 'STAFF' || status == 'DATABASE';
}

function avatarStatus() {
    $('.avatar_wrapper').each(function() {
	if (typeof $(this).attr('data-user-status') != 'undefined') {
	    $(this).popover({
		title: '<span style="color: ' + $(this).css('color') + '">' + $(this).attr('data-user-status') + '</span>',
		content: '<small style="color: #333">School Idol Tomodachi ' + (isStaffFromStatus($(this).attr('data-user-raw-status')) ? 'Staff' : 'Donator') + '</small>',
		html: true,
		placement: 'bottom',
		trigger: 'hover',
	    });
	}
    });
}

function modalHandler() {
    $('[data-toggle=ajaxmodal]').unbind('click');
    $('[data-toggle=ajaxmodal]').click(function(e) {
	e.preventDefault();
	globalModal($(this).attr('href').replace('#', '').replace('Modal', ''), $(this).data('modal-size'));
    });
}

function formloaders() {
    $('button[data-form-loader=true]').click(function(e) {
	$(this).html('<i class="flaticon-loading"></i>');
	$(this).unbind('click');
	$(this).click(function(e) {
	    e.preventDefault();
	    return false;
	});
    });
}

var alert_displayed = false;

function loadiTunesData(song, successCallback, errorCallback) {
    var itunes_id = song.find('[href="#play"]').data('itunes-id');
    var errorCallback = typeof errorCallback == 'undefined' ? function() {} : errorCallback;
    $.ajax({
	"url": 'https://itunes.apple.com/lookup',
	"dataType": "jsonp",
	"data": {
	    "id": itunes_id,
	    "country": "JP",
	},
	"error": function (jqXHR, textStatus, message) {
	    errorCallback();
	    if (alert_displayed == false) {
		alert('Oops! The song previews don\'t seem to be work anymore. Please contact us and we will fix this.');
		alert_displayed = true;
	    }
	},
	"success": function (data, textStatus, jqXHR) {
	    if (data['results'].length == 0) {
		errorCallback();
		alert('Oops! This song preview (' + song.find('.song_name').text() + ') doesn\'t seem to be valid anymore. Please contact us and we will fix this.');
	    } else {
		successCallback(data);
	    }
	}
    });
}

function loadNotifications(callbackOnLoaded) {
    var usernamebutton = $('[href="#navbarusername"]');
    $.get('/ajax/notifications/', function(data) {
	usernamebutton.popover({
	    container: $('nav.navbar ul.navbar-right'),
	    html: true,
	    placement: 'bottom',
	    content: data,
	    trigger: 'manual',
	});
	usernamebutton.on('shown.bs.popover', function () {
	    $('a[href="#loadmorenotifications"]').unbind('click');
	    $('a[href="#loadmorenotifications"]').click(function(e) {
		e.preventDefault();
		usernamebutton.popover('destroy');
		loadNotifications();
		return false;
	    });
	});
	usernamebutton.popover('show');
	if (typeof callbackOnLoaded != 'undefined') {
	    callbackOnLoaded();
	}
    });
}

function notificationsHandler() {
    var usernamebutton = $('[href="#navbarusername"]');
    $('[href="#notifications"]').click(function(e) {
	e.preventDefault();
	var button = $(this);
	button.html('<i class="flaticon-loading"></i>');
	loadNotifications(function() {
	    button.closest('li').remove();
	});
	return false;
    });
    $('body').on('click', function (e) {
	if ($(e.target).data('toggle') !== 'popover'
	    && $(e.target).parents('.popover.in').length === 0) {
	    usernamebutton.popover('hide');
	}
    });
}

$(document).ready(function() {
    var hash = window.location.hash.substring(1);
    if (hash.indexOf("Modal") >= 0) {
	globalModal(hash.replace('Modal', ''));
    }

    modalHandler();

    if ($('#notifications').length > 0) {
	$('#notifications').popover('show');
	// dismiss on click on navbar
	$('nav').on('click', function (e) {
	    if ($(e.target).data('toggle') !== 'popover'
		&& $(e.target).parents('.popover.in').length === 0) {
		$('#notifications').popover('hide');
	    }
	});
    }

    $('.switchLanguage').click(function(e) {
	e.preventDefault();
	$('#switchLanguage').find('select').val($(this).attr('data-lang'));
	$('#switchLanguage').submit();
    });

    updateActivities();
    avatarStatus();

    notificationsHandler();

    formloaders();
});

(function () {
    var s = document.createElement('script'); s.async = true;
    s.type = 'text/javascript';
      s.src = '//' + disqus_shortname + '.disqus.com/count.js';
    (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
}());


// *****************************************
// *****************************************
// *****************************************
// *****************************************
// *****************************************


function injectStyles(rule) {
  var div = $("<div />", {
    html: '&shy;<style>' + rule + '</style>'
  }).appendTo("body");
}

function ordinal_suffix_of(i) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

function aprilFoolsGame() {
    let today = new Date();
    // Check it\'s april 1st
    if ($('[href="/edit/"]').length > 0 && (today.getMonth() + 1) == 4 && today.getDate() == 1) {

        let animals = [
            'https://i.imgur.com/Qt2Ces8.png',
            'https://i.imgur.com/yrtCeon.png',
            'https://i.imgur.com/QCezaSD.png',
            'https://i.imgur.com/Ng26Duz.png',
            'https://i.imgur.com/REBy2Nu.png',
        ];
        let biganimals = [
            'https://i.schoolido.lu/cards/transparent/1484idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/1386idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/1166idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/1136idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/1070idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/navi_1022_t.png',
            'https://i.schoolido.lu/cards/transparent/629idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/382idolizedTransparent.png',
            'https://i.schoolido.lu/cards/transparent/83idolizedTransparent.png',
        ];
        function ra() {
            return animals[Math.floor(Math.random() * animals.length)];
        }
        function bra() {
            return biganimals[Math.floor(Math.random() * animals.length)];
        }
        let conf = {
            'startImage': 'https://i.imgur.com/zPN1Jse.png',
            'startText': '<div class="speech-bubble">WE ARE THE REAL IDOLS!<br><br><small>I mean, look at us. We\'re all fluffy and cuddly. We don\'t understand your obsession for μ\'s and Aqours, so today, we\'re taking over School Idol Tomodachi and turning it into School Idol ZOO!</small></p></div><br><quote class="fontx1-5">Uh oh. Looks like School Idol Tomodachi is in trouble 😰<br><br>If you want to save our community, you\'ll have  to find all the animal heads hidden around the website.<br><br>The first 3 who find all the animals will get a shoutout on Twitter!</quote>',
            'startButton': 'Find all the animals',
            'takeOverDivs': function() {
                $('.panel-heading h1.margin-novertical').text('School Idol ZOO');
                $('.navbar-brand').text('School Idol ZOO');
                $('.talking-character').css('background-image', 'url(\'' + bra() + '\')');
                $('#idols').html(biganimals.map(url => '<img src="' + url + '" alt="animal" style="width: 25%;" />').join(' '));
            },
            'hiddenAfterDivs': [
                ['.navbar-brand', ra(), 'School Idol ZOO is the new name of our site!'],
                ['[href="https://www.patreon.com/db0company"]', ra(), 'Our 3 idol devotees are showcases on the homepage!'],
                ['.statistics', ra(), 'Check the statistics of the cards!'],
                ['.flaticon-date', ra(), 'Check the release dates of the cards!'],
                ['[href="/links/"]', ra(), 'We have a handy list of external links~'],
                ['[for="id_sub_unit"]', ra(), 'Filter cards by sub unit!'],
                ['.card .flaticon-world', ra(), 'Filter for cards in worldwide version!'],
                ['[data-attribute="All"]', ra(), 'Filter for cards with the "All" attribute!'],
                ['.song', ra(), 'Have you checked out our songs page?'],
                ['[for="id_is_daily_rotation"]', ra(), 'Filter songs based on rotation!'],
                ['.event', ra(), 'Have you checked our events page?'],
                ['#event-title', ra(), 'Open any event\'s details!'],
                ['#contest-page .btn-xl', ra(), 'Try School Idol Contest!'],
                ['.song .attribute', ra(), 'Open the details of any song!'],
                ['[for="id_song_ranking"]', ra(), 'Try to add or edit event participations!'],
                ['[alt="Love Live! School Idol Trivia"]', ra(), 'Have you tried School Idol Trivia?'],
                ['[alt="Love Live! School Idol Memory"]', ra(), 'Have your tried School Idol Memory?'],
                ['#ur_pairs', ra(), 'Wait for the UR pairs page to fully load!'],
                ['#morefilters [for="id_status"]', ra(), 'Did you know that you can look for users with a special status in the leaderboard?'],
                ['.panel-default', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['[href="/discussion/sukutomo/"]', ra(), 'Have you checked the discussions?'],
                ['[href="#donate"].page-scroll.btn-link', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['#communityartists', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['[src="//i.schoolido.lu/static/honoka.png"]', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['#donate', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['[href="//i.schoolido.lu/static/postcards/4NHR4Bu.jpg"]', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['[href="https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/issues/new"]', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['[href="https://www.reddit.com/user/db0company"]', ra(), 'Make sure you wait for the about page to fully load... A bunch of things to find there!'],
                ['.home-section', ra(), 'We have a handy list of external links~'],
                ['.flaticon-scoreup', ra(), 'The new SSR Mari is a Score Up!'],
                ['.card .flaticon-skill', ra(), 'Try to filter for special cards only...'],
                ['[for="id_stored"]', ra(), 'You can filter cards by cards you own, added to your wish list, etc...'],
                ['[name="left"]', ra(), 'Try School Idol Contest!'],
                ['[name="right"]', ra(), 'Try School Idol Contest!'],
                ['[href="/user/Nyaaaaa/"]', ra(), 'Our 3 idol devotees are showcases on the homepage!'],
                ['.bg-Rainbow-3.home-section', ra(), 'We have a handy list of external links~'],
                ['[href$="/participations/"]', ra(), 'Try to add or edit event participations!'],
                ['#customize', ra(), 'Check your settings!'],
                ['#addlink', ra(), 'Check your settings!'],
                ['.jumbotron [href="/addaccount/"]', ra(), 'Check your settings!'],
                ['[for="id_location"]', ra(), 'Check your settings!'],
                ['[href="/urpairs/"]', ra(), 'The new Hanayo SSR is so cute! Looks like she\'s paired with Umi!'],
            ],
            'toFind': 'animals',
            'endText': '<div class="speech-bubble end">Thank you so much!<br>You saved School Idol Tomodachi!</div><br><div class="fontx1-5">Uwaaah, that was close! The animals were really angry and all over the place!<br><br>But thanks to you, our lovely community is back and we can keep loving our favorite idols from μ\'s, Aqours, and all the other groups!<br><br><div class="alert alert-info"><h3>Do you think you found all the animals before everyone else?</h3><br>Message us on <a href="https://twitter.com/schoolidolu/">Twitter</a> or <a href="http://discord.gg/UC32mbA">Discord</a> and if you made it to the top 3, you\'ll get a shoutout!</div></div><br><br><div class="text-center">' + animals.map(url => '<img src="' + url + '" alt="animal" />').join(' ') + '</div>',
            'endImage': 'https://i.imgur.com/V4uld5h.png',
        };

        let css = '.speech-bubble {\
	position: relative;\
	background: #CC9947;\
	border-radius: .4em;\
    color: white;\
    padding: 40px 10px;\
    text-align: center;\
    font-size: 1.5em;\
}\
\
.speech-bubble:after {\
	content: \'\';\
	position: absolute;\
	right: 0;\
	top: 50%;\
	width: 0;\
	height: 0;\
	border: 47px solid transparent;\
	border-left-color: #CC9947;\
	border-right: 0;\
	border-bottom: 0;\
	margin-top: -23.5px;\
	margin-right: -47px;\
}\
.speech-bubble.end {\
    background: #e6006f;\
    padding: 50px;\
}\
.speech-bubble.end:after {\
    border-left-color: #e6006f;\
}\
.aprilFoolsPopup {\
    position: fixed;\
    z-index: 3000;\
    bottom: 20px;\
    left: 20px;\
    max-width: 100%;\
    background-color: rgba(255, 255, 255, 0.95);\
    border-radius: 10px;\
    padding: 20px 30px;\
    border: 2px solid white;\
    box-shadow: 0px 0px 30px 2px rgba(0, 0, 0, 0.2);\
}\
';
        injectStyles(css);

        let gameDismissed = localStorage['aprilFoolDismissed' + today.getYear()] || false;
        let gameEnded = localStorage['aprilFoolEnded' + today.getYear()] || false;
        if (gameDismissed || gameEnded) {
            return;
        }
        conf.takeOverDivs();
        function gameStartedPop() {
            let totalFound = 0;
            let onPage = 0;
            let hintable = [];
            $.each(conf.hiddenAfterDivs, function(i, d) {
                let wasFound = localStorage['aprilFoolFound' + today.getYear() + '' + i] || false;
                if (wasFound) {
                    totalFound += 1;
                } else {
                    if ($(d[0]).length > 0) {
                        onPage += 1;
                        let toClick = $('<a href="#" class="padding10"><img src="' + d[1] + '" alt="to find" /></a>');
                        toClick.click(function(e) {
                            e.preventDefault();
                            toClick.remove();
                            localStorage['aprilFoolFound' + today.getYear() + '' + i] = true;
                            totalFound += 1;
                            $('.aprilFoolsPopup .found').text(totalFound);
                            onPage -= 1;
                            $('.aprilFoolsPopup .hint').html(getHint());
                            if (totalFound == totalToFind) {
                                // End of game!
                                localStorage['aprilFoolEnded' + today.getYear()] = true;
                                let modalEndContent = $('\
<div class="row">\
<div class="col-md-6 col-xs-8">\
<p class="endText">' + conf.endText + '</p>\
</div>\
<div class="col-md-6 col-xs-4">\
<img src="' + conf.endImage + '" alt="April fools" class="img-responsive" />\
</div>\
</div>\
');
                                freeModal('April fools!', modalEndContent, 0, 'lg');
                                $('#freeModal').on('hidden.bs.modal', function() {
                                    location.reload();
                                });
                            }
                            return false;
                        });
                        $(d[0]).first().after(toClick);
                    } else { // not on page
                        hintable.push(d[2])
                    }
                }
            });
            function getHint() {
                let showHint = localStorage['aprilFoolShowHint' + today.getYear()] || false;
                if (!showHint) {
                    return '?';
                } else {
                    if (onPage > 0) {
                        return (': I see ' + onPage + ' ' + conf.toFind + '!');
                    } else {
                        let hintCounter = parseInt(localStorage['aprilFoolShowHint' + today.getYear()]) || 0;
                        if (hintCounter >= 5) {
                            localStorage['aprilFoolShowHint' + today.getYear()] = 0;
                            return ': ' + hintable[Math.floor(Math.random() * hintable.length)];
                        } else {
                            localStorage['aprilFoolShowHint' + today.getYear()] = hintCounter + 1;
                            return ': Nothing to see here...';
                        }
                    }
                }
            }


            let totalToFind = conf.hiddenAfterDivs.length;

            let popup = $('<div class="aprilFoolsPopup">\
You found <span class="found">' + totalFound + '</span> / <span>' + totalToFind + '</span> ' + conf.toFind + '<br>\
<a href="#getHint" class="a-nodifference fontx0-8"><i class="flaticon-idolized"></i> Hint<span class="hint">' + getHint() + '</span></a>\
</div>');
            popup.find('[href="#getHint"]').click(function(e) {
                e.preventDefault();
                let showHint = localStorage['aprilFoolShowHint' + today.getYear()] || false;
                if (showHint) {
                    localStorage.removeItem('aprilFoolShowHint' + today.getYear());
                    popup.find('.hint').html(getHint());
                } else {
                    localStorage['aprilFoolShowHint' + today.getYear()] = true;
                    popup.find('.hint').html(getHint());
                }
                return false;
            });
            $('body').append(popup);
        }

        let gameStarted = localStorage['aprilFoolStarted' + today.getYear()] || false;
        if (gameStarted) {
            gameStartedPop();
        } else {
            let buttons = '<div class="text-center">\
<a href="#play" class="btn btn-Smile btn-xl">' + conf.startButton + '</a><br>\
<a href="#dismiss" class="btn btn-link-muted">Not interested</a></div>';
            let modalContent = $('\
<div class="row">\
<div class="col-md-8 col-xs-8">\
<p>' + conf.startText + '<br><br><br>' + buttons + '</p>\
</div>\
<div class="col-md-4 col-xs-4">\
<img src="' + conf.startImage + '" alt="April fools" class="img-responsive" />\
</div>\
</div>\
');
            modalContent.find('[href="#dismiss"]').click(function(e) {
                e.preventDefault();
                localStorage['aprilFoolDismissed' + today.getYear()] = true;
                location.reload();
                return false;
            });
            modalContent.find('[href="#play"]').click(function(e) {
                e.preventDefault();
                localStorage['aprilFoolStarted' + today.getYear()] = true;
                gameStarted = true;
                gameStartedPop();
                $('#freeModal').modal('hide');
                return false;
            });
            freeModal('April fools!', modalContent, 0, 'lg');
        }
    }
}

$(document).ready(function() {
    aprilFoolsGame();
});
