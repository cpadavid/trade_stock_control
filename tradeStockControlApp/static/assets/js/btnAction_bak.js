$('#newStockBtn').click(function () {
	jQuery.support.cors = true;

	$.ajax(
		{
			type: "GET",
			url: 'http://127.0.0.1:8000/tradeStockControlApp/helloList/',
			data: "{}",
			// contentType: "application/json; charset=utf-8",
			// dataType: "json",
			dataType: "html",
			success: function (data, status, jqXHR) {

				alert('success');
				alert(data);
				alert(status);
				alert(jqXHR);
				/*
				$.each(data, function (i, theItem) {
					var combo = document.getElementById("cboFastBikes");
					var option = document.createElement("option");
					option.text = theItem.toString();
					option.value = theItem.toString();
					try {
						//alert('success add combo');
						combo.add(option, null); // Other browsers
					}
					catch (error) {
						alert('error found');
						combo.add(option); // really old browser
					}

				});
				*/
			},
			error: function (data, status, jqXHR) {
				alert('error');
				alert(data);
				/*
				alert('error trapped in error: function(msg, url, line)');
				alert('msg = ' + msg + ', url = ' + url + ', line = ' + line);
				*/

			}
		});

	alert('button click');

});