var $ = jQuery;
var card_num;

$(document).ready(function() {

	$(".dropdown-menu li a").click(function(){
	  var selText = $(this).text();
	  card_num = $(this).attr('card_num');
	  $('#payment_form .card-num').val(card_num);
	  $('#payment_form_custom .card-num').val(card_num);
	  $(this).parents('.btn-group').find('.dropdown-toggle .user-name').text(selText);
	});

	$("form :input").on("keypress", function(e) {
		return e.keyCode != 13;
	});

	text = $('#consumer-card-1').text();

	var selectedValue = text;
	$('.dropdown-menu  > li > a:contains("'+selectedValue+'")').parent('li').addClass("active");
	$('.dropdown-menu  > li > a:contains("'+selectedValue+'")').trigger('click');

   $('#testTransaction .btn-retry').click(function() {
	  $('.ajax-mainform-wrapper').show();
	  $('.ajax-response-wrapper').hide();
	  $('.error-notifications').empty();
	//  $('#id_amount').val('');
	  $(this).hide();
	  $('.btn-pay').show();
   });

   $('#testCustomTransaction .btn-retry').click(function() {
	  $('.ajax-mainform-wrapper').show();
	  $('.ajax-response-wrapper').hide();
	  $('.error-notifications').empty();
	  //$('#testCustomTransaction #id_amount').val('');
	  $(this).hide();
	  $('.btn-pay').show();
	 // $('#merchant-name').val('');
	  //$('#location').val('');
   });

   $('#payment_form_custom #merchant-name').change(function(){
		merchantUuid = $(this).val().replace(' ','-').toLowerCase();
		$('#payment_form_custom #merchant-id').val(merchantUuid);
   });

   $('div.btn-run-test-custom').click(function() {
	   $("label[for = id_amount]").text("Amount");
	  $('#testCustomTransaction .ajax-mainform-wrapper').show();
	  $('#testCustomTransaction .ajax-response-wrapper').hide();
	  $('#testCustomTransaction .error-notifications').empty();
	  $('#testCustomTransaction #merchant-name').val('');
	  $('#testCustomTransaction #id_amount').val('');
	  $('#testCustomTransaction .btn-pay').show();
	  $('#testCustomTransaction .btn-retry').hide();
	   $('#testCustomTransaction .btn-cancel').text('Cancel');
   });

   $('div.btn-run-test').click(function() {
	  if (!card_num) {
		alert("Please choose consumer account.");
		return false;
	  }
	  $('#testTransaction .btn-pay').show();
	  $('#testTransaction .btn-retry').hide();
	  $('#testTransaction .btn-cancel').text('Cancel');
	  $('#myModalLabel').html($(this).attr('title'));
	  id = $(this).attr('id');
	  $('#payment_form .scenario-run-id').val(id);
	  $('#id_amount').val('');
	  $('#testTransaction .ajax-mainform-wrapper').show();
	  $('#testTransaction .ajax-response-wrapper').hide();
	  $('#testTransaction .error-notifications').empty();
	  url = $('.imageCache .cache-'+id).attr('src');

	  name = $(this).attr('data-name');
	  location_ = $(this).attr('data-location');
	  $('#testTransaction .modal-wrapper').css('background-image', 'url("' + url + '")');
	  $('#testTransaction .name').html(name);
	  $('#testTransaction .location').html(location_);
	  $('#testTransaction .scenario-block-footer').attr('class','').addClass('scenario-block-footer-'+id).addClass('scenario-block-footer');
   });

   $("#testTransaction .btn-pay").click(function() {

		var message = "";
		card_number = $('.card-num').val().trim();
		amount = $('#payment_form #id_amount').val();

		ajax_request = true;

		if (!card_number) {
			message = "Please provide card number.";
			ajax_request = false;
		} else if (!amount) {
			message = "Please provide amount.";
			ajax_request = false;
		}

		if (!ajax_request) {
			$('#testTransaction .error-notifications').empty().append('<div class="alert alert-warning text-center">'+message+'</div>');
			return false;
		} else {
			$('#testTransaction .error-notifications').empty();
		}

		var start_time = new Date().getTime();

		$.ajax({
			data: $("#payment_form").serialize(),
			type: "POST",
			url: "/besim/home",
			success: function(response) {
				$('#testTransaction .please-wait').hide();
				$("#testTransaction .btn-pay").removeClass('disabled');
				$('#testTransaction .ajax-mainform-wrapper').hide();
				$('#testTransaction .ajax-response-wrapper').show();
				console.log(response);
				var obj = $.parseJSON(response);
				data = obj.data;
				flag = data.flag;
				end_time = new Date().getTime();
				response_time = (end_time - start_time) / 1000;
				processing_time = data.time/1000;

				if (flag == true) {
					processingTime = '';

					processingTime = '<div class="response-time">Processing time: ' + processing_time + ' seconds.</div>';

					msg = '<h2> Thank You.</h2><div class="response-time">Response time: ' + response_time + ' seconds.</div>';
					msg += processingTime;

					$('#testTransaction .ajax-response-wrapper').empty().append(msg);
					$('#testTransaction .btn-cancel').text('Close');
					$('#testTransaction .btn-retry').hide();
				} else {
					processingTime = '';
					serverMsg = '<div class="server-response-error-msg">' + data.msg + '</div>';

					processingTime = '<div class="response-time">Processing time: ' + processing_time + ' seconds.</div>';

					msg = '<h2> Your transaction was declined!</h2>' + serverMsg + processingTime +'<div class="response-time">Response time: ' + response_time + ' seconds.</div>';
					$('#testTransaction .ajax-response-wrapper').empty().append(msg);
					$('#testTransaction .btn-retry').show();
				}

				$('#testTransaction .btn-cancel').show();
				$('#testTransaction .btn-pay').hide();
            },
			beforeSend: function(xhr) {
				$("#testTransaction .btn-pay").addClass('disabled');
				$('#testTransaction .please-wait').show();
			},
			error : function(xhr,errmsg,err) {
				$('#testTransaction .please-wait').hide();
				$("#testTransaction .btn-pay").removeClass('disabled');
				$('#testTransaction .ajax-mainform-wrapper').hide();
				$('#testTransaction .ajax-response-wrapper').show();
				$('#testTransaction .btn-retry').show();
				$('#testTransaction .btn-pay').hide();
			//	$('.ajax-response-wrapper').empty().append('<h2>' + xhr.status+ ' error from server side!</h2>');
			}
        });

		return false;
    });


	$("#testCustomTransaction .btn-pay").click(function() {

		var message = "";

		card_number = $('.card-num').val().trim();
		amount = $('#payment_form_custom #id_amount').val();
		merchant = $('#payment_form_custom #merchant-name').val();

		ajax_request = true;

		if (!merchant) {
			message = "Please provide merchant.";
			ajax_request = false;
		} else if (!card_number) {
			message = "Please provide card number.";
			ajax_request = false;
		} else if (!amount) {
			message = "Please provide amount.";
			ajax_request = false;
		}

		if (!ajax_request) {
			$('#testCustomTransaction .error-notifications').empty().append('<div class="alert alert-warning text-center">'+message+'</div>');
			return false;
		} else {
			$('#testCustomTransaction .error-notifications').empty();
		}

		var start_time = new Date().getTime();

		$.ajax({
			data: $("#payment_form_custom").serialize(),
			type: "POST",
			url: "/besim/home",
			success: function(response) {
				$('#testCustomTransaction .please-wait').hide();
				$("#testCustomTransaction .btn-pay").removeClass('disabled');
				$('#testCustomTransaction .ajax-mainform-wrapper').hide();
				$('#testCustomTransaction .ajax-response-wrapper').show();
				console.log(response);
				var obj = $.parseJSON(response);
				data = obj.data;
				flag = data.flag;
				end_time = new Date().getTime();
				response_time = (end_time - start_time) / 1000;
				processing_time = data.time/1000;

				if (flag == true) {
					msg = '<h2> Thank You.</h2><div class="response-time">Response time: ' + response_time + ' second.</div>';

					processingTime = '<div class="response-time">Processing time: ' + processing_time + ' second.</div>';

					msg += processingTime;

					$('#testCustomTransaction .ajax-response-wrapper').empty().append(msg);
					$('#testCustomTransaction .btn-cancel').text('Close');
					$('#testCustomTransaction .btn-retry').hide();
				} else {

					serverMsg = '<div class="server-response-error-msg">' + data.msg + '</div>';
					processingTime = '<div class="response-time">Processing time: ' + processing_time + ' second.</div>';

					msg = '<h2> Your transaction was declined!</h2>' + serverMsg + processingTime +'<div class="response-time">Response time: ' + response_time + ' second.</div>';

					$('#testCustomTransaction .ajax-response-wrapper').empty().append(msg);
					$('#testCustomTransaction .btn-retry').show();
				}

				$('#testCustomTransaction .btn-cancel').show();
				$('#testCustomTransaction .btn-pay').hide();
            },
			beforeSend: function(xhr) {
				$("#testCustomTransaction .btn-pay").addClass('disabled');
				$('#testCustomTransaction .please-wait').show();
			},
			error : function(xhr,errmsg,err) {
				$('#testCustomTransaction .please-wait').hide();
				$("#testCustomTransaction .btn-pay").removeClass('disabled');
				$('#testCustomTransaction .ajax-mainform-wrapper').hide();
				$('#testCustomTransaction .ajax-response-wrapper').show();
				$('#testCustomTransaction .btn-retry').show();
				$('#testCustomTransaction .btn-pay').hide();
			}
        });

		return false;
    });
   });
