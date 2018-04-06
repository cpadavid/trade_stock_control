$("#list").load("homeIndex.html", null, initPagination);

var initPagination = function() {
	$("#pagination").pagination(30, { //資料數目
    num_edge_entries: 2, //兩側頁碼數目   
    num_display_entries: 3, //中間顯示的頁碼數目   
    current_page:0, //目前頁, 預設是0   
    ellipse_text:"...", //省略的頁碼用什麼表現, 預設是"..."   
    callback: pageselectCallback, //回傳資料   
    items_per_page: 10, //每頁呈現筆數   
    prev_show_always: true, //是否顯示上一頁按鈕   
    next_show_always: true, //是否顯示下一頁按鈕   
    prev_text: "prev", //上一頁呈現文字   
    next_text: "next" //下一頁呈現文字   
	});
};

function pageselectCallback(page_index, jq){   
    page_end=page_index+10;   
    $("#list li").hide();   
    for($i=page_index; $i<page_end; $i++){   
        $("#list li").eq($i).show();   
    }      
    return false;   
}
