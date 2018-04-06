function stockTableTdClick(event, row) {
    $('html,body').animate({
        scrollTop: $("#editStock").offset().top}, 
    'slow');
   
    var rowData = row.children;
    var isSuperUser = ($('meta[name=isSuperUser]').attr("content") == 'True');
    console.log('Is Super User');
    console.log($("#isSuperUser"));
    console.log(isSuperUser);
    console.log(typeof isSuperUser);
    $('#editStockId').val(rowData[0].innerHTML.replace(/\s/g, ''));
    $('#editStockItemNo').val(rowData[1].innerHTML.replace(/\s/g, ''));
    $('#editStockDesc').val(rowData[2].innerHTML.replace(/\s/g, ''));
    $('#editStockType').val(rowData[3].innerHTML.replace(/\s/g, ''));
    // $('#editStockColor').val(rgb2hex(rowData[4].style['background']));
    $('#editStockColor').val(rowData[4].innerHTML.replace(/\s/g, ''));
    $('#editStockSize').val(rowData[5].innerHTML.replace(/\s/g, ''));
    $('#editStockQty').val(rowData[6].innerHTML.replace(/\s/g, ''));
    if (isSuperUser) {
        $('#editStockCost').val(rowData[7].innerHTML.replace(/\s/g, ''));
        $('#editStockPrice').val(rowData[8].innerHTML.replace(/\s/g, ''));
    } else {
        $('#editStockStaffPrice').val(rowData[7].innerHTML.replace(/\s/g, ''));
    }
    
}

var hexDigits = new Array
        ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"); 

function rgb2hex(rgb) {
    rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}

function hex(x) {
    return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
}