function hidePanes(){
	$(".pane-content").hide();
}

function initializePanes(){
	$("#about-content").show();
	$(".logistics-schedule-pane").show();
	$(".faq-general-pane").show();
	$(".apply-content").show();
	$(".sponsor-content").show();
	$(".team-content").show();
	$(".footer-content").show();
	$(".schedule-content").show();
}

$(document).ready(function(){
	console.log("%cArchHacks says: You should apply :)", "color: red; font-size: large;");
	var FIREFOX = /Firefox/i.test(navigator.userAgent);
	if (FIREFOX) {
		$("#archhacks-countdown-wrapper").hide();
	}
	var CHROME = /Chrome/i.test(navigator.userAgent);
	
	setCountdownInfo();
	window.setInterval(function(){
		setCountdownInfo();
	}, 1000);
	var position = $(window).scrollTop();
	$('#header-wrapper').removeClass("fixed-header").addClass("hidden-header");
	if (position > 0) {
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
	}
	else{
		$('#stickybar-wrapper').removeClass("fixed-stickynav").addClass("hidden-stickynav");
	}
	$(".sticky-button").removeClass("filled-button")
	if (position >= applypane_header && position < aboutpane_header) {
		$("#sticky-button-apply").addClass("filled-button");
	}
	if (position >= aboutpane_header && position < schedulepane_header) {
		$("#sticky-button-about").addClass("filled-button");
	}
	if (position >= schedulepane_header && position < sponsorpane_header) {
		$("#sticky-button-schedule").addClass("filled-button");
	}
	if (position >= sponsorpane_header && position < teampane_header) {
		$("#sticky-button-sponsor").addClass("filled-button");
	}
	if (position >= teampane_header && position < faqpane_header) {
		$("#sticky-button-team").addClass("filled-button");
	}
	if (position > faqpane_header) {
		$("#sticky-button-faq").addClass("filled-button");
	}

	var appjumppane = $(".app-jump-pane").offset().top;

	var aboutpane = $('#about-page').offset().top;
	var aboutpane_header = $("#about-page-header").offset().top;

	var applypane = $("#apply-pane").offset().top;
	var applypane_header = $("#apply-page-header").offset().top;

	var schedulepane = $("#schedule-pane").offset().top;
	var schedulepane_header = $("#schedule-page-header").offset().top;

	var sponsorpane = $("#sponsor-pane").offset().top;
	var sponsorpane_header = $("#sponsor-page-header").offset().top;

	var teampane = $("#team-pane").offset().top;
	var teampane_header = $("#team-page-header").offset().top;

	var faqpane = $("#faq-pane").offset().top;
	var faqpane_header = $("#faq-page-header").offset().top;

	$(".event > .event-description").hide();
	$(".event > .event-description").addClass("hidden");
	$(".event").click(function(){
		var this_hidden = $(this).find(".event-description").hasClass("hidden");
		$(".event-description").hide();
		$(".event-description").addClass("hidden");
		if (this_hidden === true){
			$(this).find(".event-description").show();
			$(this).find(".event-description").removeClass("hidden");
		}
		else {
			$(this).find(".event-description").hide();
			$(this).find(".event-description").addClass("hidden");
		}
	});
	$(window).scroll(function(){
		position = $(window).scrollTop();

		appjumppane = $(".app-jump-pane").offset().top;

		aboutpane = $('#about-page').offset().top;
		aboutpane_header = $("#about-page-header").offset().top;

		applypane = $("#apply-pane").offset().top;
		applypane_header = $("#apply-page-header").offset().top;

		schedulepane = $("#schedule-pane").offset().top;
		schedulepane_header = $("#schedule-page-header").offset().top;

		sponsorpane = $("#sponsor-pane").offset().top;
		sponsorpane_header = $("#sponsor-page-header").offset().top;

		teampane = $("#team-pane").offset().top;
		teampane_header = $("#team-page-header").offset().top;

		faqpane = $("#faq-pane").offset().top;
		faqpane_header = $("#faq-page-header").offset().top;

		$(window).resize(function(){
			position = $(window).scrollTop();

			appjumppane = $(".app-jump-pane").offset().top;

			aboutpane = $('#about-page').offset().top;
			aboutpane_header = $("#about-page-header").offset().top;

			applypane = $("#apply-pane").offset().top;
			applypane_header = $("#apply-page-header").offset().top;

			schedulepane = $("#schedule-pane").offset().top;
			schedulepane_header = $("#schedule-page-header").offset().top;

			sponsorpane = $("#sponsor-pane").offset().top;
			sponsorpane_header = $("#sponsor-page-header").offset().top;

			teampane = $("#team-pane").offset().top;
			teampane_header = $("#team-page-header").offset().top;

			faqpane = $("#faq-pane").offset().top;
			faqpane_header = $("#faq-page-header").offset().top;
		});

		if (position > 0) {
			$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		} else {
			$('#stickybar-wrapper').removeClass("fixed-stickynav").addClass("hidden-stickynav");
		}

		$(".sticky-button").removeClass("filled-button")
		if (position >= applypane_header && position < aboutpane_header) {
			$("#sticky-button-apply").addClass("filled-button");
		}
		if (position >= aboutpane_header && position < schedulepane_header) {
			$("#sticky-button-about").addClass("filled-button");
		}
		if (position >= schedulepane_header && position < sponsorpane_header) {
			$("#sticky-button-schedule").addClass("filled-button");
		}
		if (position >= sponsorpane_header && position < teampane_header) {
			$("#sticky-button-sponsor").addClass("filled-button");
		}
		if (position >= teampane_header && position < faqpane_header) {
			$("#sticky-button-team").addClass("filled-button");
		}
		if (position > faqpane_header) {
			$("#sticky-button-faq").addClass("filled-button");
		}
	})

	$("#sticky-button-about, #sticky-line-text-about, .footer-click-about").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: aboutpane_header + 1}, 500);
	});
	$("#sticky-button-apply, #sticky-line-text-apply, .footer-click-apply").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: applypane_header + 1}, 500);
	});
	$("#sticky-button-schedule, #sticky-line-text-schedule, .footer-click-schedule").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: schedulepane_header + 1}, 500);
	});
	$("#sticky-button-sponsor, #sticky-line-text-sponsor, .footer-click-sponsor").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: sponsorpane_header + 1}, 500);
	});
	$("#sticky-button-team, #sticky-line-text-team, .footer-click-team").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: teampane_header + 1}, 500);
	});
	$("#sticky-button-faq, #sticky-line-text-faq, .footer-click-faq").click(function(){
		$('#stickybar-wrapper').addClass("fixed-stickynav").removeClass("hidden-stickynav");
		$('html, body').animate({scrollTop: faqpane_header + 1}, 500);
	});
	$(".stickybar-logo, #footer-logo").click(function(){
		$('html, body').animate({scrollTop: 0}, 500);
	});

	hidePanes();
	initializePanes();

	$(".faq-general-click").addClass('faq-bold');
	$(".logistics-schedule-click").click(function(){
		$(".logistics-map-pane").hide();
		$(".logistics-schedule-pane").show();
	});

	$(".logistics-map-click").click(function(){
		$(".logistics-schedule-pane").hide();
		$(".logistics-map-pane").show();
	});

	$(".faq-general-click").click(function(){
		unboldOthers();
		$(".faq-general-click").addClass('faq-bold');
		$(".faq-pane").hide();
		$(".faq-general-pane").show();
	});

	$(".faq-registration-click").click(function(){
		unboldOthers();
		$(".faq-registration-click").addClass('faq-bold');
		$(".faq-pane").hide();
		$(".faq-registration-pane").show();
	});

	$(".faq-hacking-click").click(function(){
		unboldOthers();
		$(".faq-hacking-click").addClass('faq-bold');
		$(".faq-pane").hide();
		$(".faq-hacking-pane").show();
	});

	$(".faq-logistics-click").click(function(){
		unboldOthers();
		$(".faq-logistics-click").addClass('faq-bold');
		$(".faq-pane").hide();
		$(".faq-logistics-pane").show();
	});

	function unboldOthers(){
		$('.faq-click').removeClass('faq-bold');
	}
	$('#welcome-volunteerjump').click(function(){
		var volunteer = window.open("/volunteer", '_blank');
		//if (volunteer){
		//	volunteer.focus();
		//}
	});
	$('#mobile-welcome-jump-button').click(function(){
		$('html, body').animate({scrollTop: appjumppane}, 500);
	});
	$('#data-vis-jump').click(function(){
		window.open('/application-stats', '_blank');
	});
	var hasBeenHidden = false;
	if($(window).width() < 1024){
		$(".homepage-pane").hide();
		hasBeenHidden = true;
		$("#apply-page-header").click(function(){
			$("#apply-pane").show();
		});
		$("#about-page-header").click(function(){
			$("#about-page").show();
		});
		$("#schedule-page-header").click(function(){
			$("#schedule-pane").show();
		});
		$("#sponsor-page-header").click(function(){
			$("#sponsor-pane").show();
		});
		$("#team-page-header").click(function(){
			$("#team-pane").show();
		});
		$("#faq-page-header").click(function(){
			$("#faq-pane").show();
		});
	}
	$(window).resize(function(){
		if(($(window).width() < 1024) && !(hasBeenHidden)){
			$(".homepage-pane").hide();
			hasBeenHidden = true;
			$("#apply-page-header").click(function(){
				$("#apply-pane").show();
			});
			$("#about-page-header").click(function(){
				$("#about-page").show();
			});
			$("#schedule-page-header").click(function(){
				$("#schedule-pane").show();
			});
			$("#sponsor-page-header").click(function(){
				$("#sponsor-pane").show();
			});
			$("#team-page-header").click(function(){
				$("#team-pane").show();
			});
			$("#faq-page-header").click(function(){
				$("#faq-pane").show();
			});
		}
		if($(window).width() >= 1024){
			$(".homepage-pane").show();
			hasBeenHidden = false;
		}
		$(".sticky-button").removeClass("filled-button")
		if (position >= applypane_header && position < aboutpane_header) {
			$("#sticky-button-apply").addClass("filled-button");
		}
		if (position >= aboutpane_header && position < schedulepane_header) {
			$("#sticky-button-about").addClass("filled-button");
		}
		if (position >= schedulepane_header && position < sponsorpane_header) {
			$("#sticky-button-schedule").addClass("filled-button");
		}
		if (position >= sponsorpane_header && position < teampane_header) {
			$("#sticky-button-sponsor").addClass("filled-button");
		}
		if (position >= teampane_header && position < faqpane_header) {
			$("#sticky-button-team").addClass("filled-button");
		}
		if (position > faqpane_header) {
			$("#sticky-button-faq").addClass("filled-button");
		}

		position = $(window).scrollTop();

		aboutpane = $('#about-page').offset().top;
		aboutpane_header = $("#about-page-header").offset().top;

		applypane = $("#apply-pane").offset().top;
		applypane_header = $("#apply-page-header").offset().top;

		schedulepane = $("#schedule-pane").offset().top;
		schedulepane_header = $("#schedule-page-header").offset().top;

		sponsorpane = $("#sponsor-pane").offset().top;
		sponsorpane_header = $("#sponsor-page-header").offset().top;

		teampane = $("#team-pane").offset().top;
		teampane_header = $("#team-page-header").offset().top;

		faqpane = $("#faq-pane").offset().top;
		faqpane_header = $("#faq-page-header").offset().top;
	});
	function closeOtherPanes(){
		$('.homepage-pane').hide("slide", { direction: "up" }, 200);
	}
})