var curIndex = 0;
var time = 800;
var slideTime = 2000;
var adTxt = $("#stage-items>li>div>.layout-wrapper");
var adImg = $("#stage-items>li>div>.ad_img");
var int = setInterval("autoSlide()", slideTime);
$("#banner_ctr>ul>li[class!='first-item'][class!='last-item']").click(function () {
    show($(this).index("#banner_ctr>ul>li[class!='first-item'][class!='last-item']"));
    window.clearInterval(int);
    int = setInterval("autoSlide()", slideTime);
});
function autoSlide() {
    curIndex + 1 >= $("#stage-items>li").size() ? curIndex = -1 : false;
    show(curIndex + 1);
}
function show(index) {
    $.easing.def = "easeOutQuad";

    $("#stage-items>li").eq(curIndex).css("display","none");
	//var aa = $("#stage-items>li").eq(curIndex).attr("banner_ctr");
	//alert(aa);
    setTimeout(function () {
		var data_bg = $("#stage-items>li").eq(curIndex).attr("data-bg");
		var back = "url('/static/images/index/"+data_bg+"')";
		$(".timeline-bg").css("background-image",back);
        $("#stage-items>li").eq(index).stop(false, true).fadeIn(time);
		//$(this).css('display','none');
        //adTxt.eq(index).children("p").css({ paddingTop: "50px", paddingBottom: "50px" }).stop(false, true).animate({ paddingTop: "0", paddingBottom: "0" }, time);
        adTxt.eq(index).css({ top: "0", opacity: "0" }).stop(false, true).animate({ top: "170px", opacity: "1" }, time);
    }, 200)
    curIndex = index;
}