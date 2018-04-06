// Django ajax setup for Cross Site Request Forgery protection
// using jQuery
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


// Button Action
$('#newStockBtn').click(function () {
	jQuery.support.cors = true;
    
	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/newStock/',
			data: JSON.stringify({
				"itemNo": $('#newStockItemNo').val(), 
				"desc": $('#newStockDesc').val(), 
				"color": $('#newStockColor').val(), 
				"size": $('#newStockSize').val(), 
				"type": $('#newStockType').val(), 
				"cost": $('#newStockCost').val(), 
				"price": $('#newStockPrice').val(), 
				"qty": $('#newStockQty').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
				alert("New Stock Success !");
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});

});

$('#checkStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/checkStock/',
			data: JSON.stringify({
				"checkItemNo": $('#checkStockItemNo').val(),
				"checkDesc": $('#checkStockDesc').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('#sellStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/sellStock/',
			data: JSON.stringify({
				"stockId": $('#editStockId').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
                alert("Sell Stock Success !");
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});


$('#packStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/packStock/',
			data: JSON.stringify({
				"stockId": $('#editStockId').val(),
				"quantity": $('#updateStockQty').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
                alert("Pack Stock Success !");
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('#refillStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/refillStock/',
			data: JSON.stringify({
				"stockId": $('#editStockId').val(),
				"quantity": $('#updateStockQty').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
                alert("Refill Stock Success !");
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('#editStockBtn').click(function () {
	jQuery.support.cors = true;

    var isSuperUser = ($('meta[name=isSuperUser]').attr("content") == 'True');
    var cost = 0;
    var price = 0;
    if (isSuperUser) {
        cost = $('#editStockCost').val();
        price = $('#editStockPrice').val();
    } else {
        cost = 0;
        price = $('#editStockStaffPrice').val();
    }
    
	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/editStock/',
			data: JSON.stringify({
				"stockId": $('#editStockId').val(),
				"itemNo": $('#editStockItemNo').val(), 
				"desc": $('#editStockDesc').val(), 
				"color": $('#editStockColor').val(), 
				"size": $('#editStockSize').val(), 
				"type": $('#editStockType').val(), 
				"cost": cost, 
				"price": price
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#stockTableDiv").html(jqObj.find('#stockTable'));
                alert("Edit Stock Success !");
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('#calcStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/calcStock/',
			data: JSON.stringify({
				"fromDate": $('#reportFromDate').val(),
				"toDate": $('#reportToDate').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data) {
                console.log(data);
                respData = $.parseJSON(data);
                $("#rptSales").val(respData.salesResult);
                $("#rptCost").val(respData.costResult);
                $("#rptProfit").val(respData.profitResult);
                $("#rptStockValue").val(respData.stockValueResult);
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('#genInvoiceStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/genInvoiceStock/',
			data: JSON.stringify({
				"fromDate": $('#reportFromDate').val(),
				"toDate": $('#reportToDate').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, code, xhr) {
                var blob = new Blob([data]);
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download=xhr.getResponseHeader('PDF-NAME');
                link.click();
			},
			error: function (data) {
                console.log(data)
			}
		});
});

$('#checkInStoreOrderHistBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/checkInStoreOrderHist/',
			data: JSON.stringify({
				"telNo": $('#checkPhoneNo').val(),
				"orderNo": $('#checkOrderNo').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                var jqObj = jQuery(data);
                $("#inStoreOrderTableDiv").html(jqObj.find('#inStoreOrderTable'));
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});

$('input[id^="sendInvoiceBtn"]').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/sendInvoice/',
			data: JSON.stringify({
				"telNo": $(this).parents('tr').find('#telNo')[0].innerHTML,
				"orderNo": $(this).parents('tr').find('#orderNo')[0].innerHTML,
                "email": $(this).parents('tr').find('#email')[0].innerHTML
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {
                respData = $.parseJSON(jqXHR.responseText);
                alert(respData.message);
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});


$('#genOrderHistStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "POST",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/genOrderHistExcel/',
			data: JSON.stringify({
				"fromDate": $('#getOrderHistFromDate').val(),
				"toDate": $('#getOrderHistToDate').val()
			}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			dataType: "html",
			success: function (data, code, xhr) {
                alert("Success");
                var blob = new Blob([data]);
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download=xhr.getResponseHeader('XLSX-NAME');
                link.click();
                
			},
			error: function (data) {
                respData = $.parseJSON(data.responseText);
                alert(respData.message);
			}
		});
});


