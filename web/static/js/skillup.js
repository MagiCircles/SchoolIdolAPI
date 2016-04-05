
$(document).ready(function() {
    $('[name="delete"]').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var ownedcard = button.closest('figure');
	var ownedcard_id = ownedcard.data('ownedcard-id');
	var skill_area = ownedcard.closest('.skill-area');
	$.ajax({
	    method: 'GET',
	    url: '/ajax/deletecard/' + ownedcard_id + '/',
	    success: function(data) {
		ownedcard.remove();
		if (skill_area.find('figure').length == 0) {
		    skill_area.remove();
		}
	    },
	    error: genericAjaxError,
	});
	return false;
    });
    $('[name="skillup"]').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var ownedcard = button.closest('figure');
	var ownedcard_id = ownedcard.data('ownedcard-id');
	var skill_area = ownedcard.closest('.skill-area');
	var skill_level = skill_area.data('skill-level');
	var skill_td = ownedcard.closest('td');
	$.ajax({
	    method: 'POST',
	    url: '/ajax/albumbuilder/editcard/' + ownedcard_id + '/',
	    data: { skill: parseInt(skill_level) + 1 },
	    success: function(data) {
		ownedcard.detach();
		if (skill_area.find('figure').length == 0) {
		    skill_area.remove();
		}
		var new_skill_area = skill_td.find('.skill-area[data-skill-level="' + data['skill'] + '"]');
		if (new_skill_area.length == 0) {
		    var new_skill_area = $('<div class="skill-area" data-skill-level="' + data['skill'] + '"><h4 class="fontx1-5 text-center"><i class="flaticon-skill"></i> ' + message_skill_level + ' <b>' + data['skill'] + '</b></h4>');
		    var current_skill_areas = skill_td.find('.skill-area');
		    var i = 0;
		    var flag = false;
		    while (i < current_skill_areas.length) {
			if (parseInt(current_skill_areas.eq(i).data('skill-level')) < data['skill']) {
			    new_skill_area.insertBefore(current_skill_areas[i]);
			    flag = true;
			    break;
			}
			i++;
		    }
		    if (!flag) {
			new_skill_area.prependTo(skill_td);
		    }
		}
		ownedcard.appendTo(new_skill_area);
		if (data['skill'] == 8) {
		    ownedcard.find('[name="skillup"]').remove();
		}
		if (data['stored'] == 'Deck') {
		    var flaticon_present = ownedcard.find('.flaticon-present');
		    flaticon_present.removeClass();
		    flaticon_present.addClass('flaticon-deck');
		    ownedcard.find('.stored-in').text(message_in_deck);
		}
	    },
	    error: genericAjaxError,
	});
	return false;
    });
});
