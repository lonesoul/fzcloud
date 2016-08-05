$(function(){
	/* 上菜单 */
	$(".hasSub").click(function(e){
		if($(this).hasClass("hover")){
			$(this).removeClass("hover").find(".topSub").hide();
			e.stopPropagation(); 
			}
			else{
			$(this).addClass("hover").find(".topSub").show();
			$(this).siblings().removeClass("hover").find(".topSub").hide();
			e.stopPropagation(); 
			}
		});
	
	/* 左导航 */
	$(".leftMenu li:first").click(function(){
			$(this).addClass("current").siblings().removeClass("current");
			$(".subMenu").animate({left:"-142px"},"slow").find(".pushIcon").hide();
			$(".rightCon").animate({"margin-left":"68px"},"slow");
		})
 	var currentLi=$(".leftMenu li:not(:first)")
   currentLi.click(function(){
        if ($(this).hasClass("current")==false) {
            $(".leftMenu li").removeClass("current");
            $(this).addClass("current");
        }
        var selId = $(this).attr("rel");
        $(".subMenu ul").css("display","none");
        $(".subMenu ul#"+selId).css("display","block");
		$(".subMenu").animate({left:"68px"},"slow")
					 .find(".pushIcon").show().removeClass("pullIcon").css("right","0");
		$(".rightCon").animate({"margin-left":"278px"},"slow");
    });

	if(currentLi.hasClass("current")){
		var selId = $(".current").attr("rel");
		$(".subMenu ul#"+selId).css("display","block");
		$(".subMenu").css("left","68px").find(".pushIcon").show().removeClass("pullIcon").css("right","0");
		$(".rightCon").css("margin-left","278px")
		}
	
	$(".pushIcon").click(function(){
		 if($(this).hasClass("pullIcon")){
			 $(this).removeClass("pullIcon").css("right","0");
			 $(".subMenu").animate({left:"68px"},"slow");
			 $(".rightCon").animate({"margin-left":"278px"},"slow");
			 }
		else{
			 $(".subMenu").animate({left:"-142px"},"slow");
			 $(".rightCon").animate({"margin-left":"68px"},"slow");
			 $(this).addClass("pullIcon").css("right","-18px");
			}
		});
	
		
	$('.circle').each(function() {
		var total=$(this).next(".num").find("i").text();
		var curNum=$(this).find('span').text();
        var num = 360/total*curNum;
        if (num<=180) {
            $(this).find('.rightArea').css('transform', "rotate(" + num + "deg)");
        } else {
            $(this).find('.rightArea').css('transform', "rotate(180deg)");
            $(this).find('.leftArea').css('transform', "rotate(" + (num - 180) + "deg)");
        };
    });

	//关闭产品menu
	$(document).click(function(e){  
        $(".select-box").removeClass("open");
		$(".hasSub").removeClass("hover");
		$(".topSub").hide(); 
	});	
		
})

/* 概览环形 */
var  paper =  null;
function init(b,n,m,c){
	//初始化Raphael画布 
	this.paper = Raphael(b, 116, 116); 
	//进度比例，0到1
	//需要注意，下面的算法不支持画100%，要按99.99%来画 
	var percent = n/m	, 
		drawPercent = percent >= 1 ? 0.9999 : percent; 
	
	//r1是内圆半径，r2是外圆半径 
	var r1 = 52, r2 = 58, PI = Math.PI, 
		p1 = { 
			x:58,  
			y:116 
		}, 
		p4 = { 
			x:p1.x, 
			y:p1.y - r2 + r1 
		}, 
		p2 = {  
			x:p1.x + r2 * Math.sin(2 * PI * (1 - drawPercent)), 
			y:p1.y - r2 + r2 * Math.cos(2 * PI * (1 - drawPercent)) 
		}, 
		p3 = { 
			x:p4.x + r1 * Math.sin(2 * PI * (1 - drawPercent)), 
			y:p4.y - r1 + r1 * Math.cos(2 * PI * (1 - drawPercent)) 
		}, 
		path = [ 
			'M', p1.x, ' ', p1.y, 
			'A', r2, ' ', r2, ' 0 ', percent > 0.5 ? 1 : 0, ' 1 ', p2.x, ' ', p2.y, 
			'L', p3.x, ' ', p3.y, 
			'A', r1, ' ', r1, ' 0 ', percent > 0.5 ? 1 : 0, ' 0 ', p4.x, ' ', p4.y, 
			'Z' 
		].join(''); 
	
	//用path方法画图形，由两段圆弧和两条直线组成 
	this.paper.path(path) 
		.attr({"stroke-width":0, "fill":c}); 
	
}

//tab标签
function setTab(name,cursel,n){
    for(i=1;i<=n;i++){
        var menu=document.getElementById(name+i);
        var con=document.getElementById("con-"+name+"-"+i);
        menu.className=i==cursel?"hover":"";
        con.style.display=i==cursel?"block":"none";
    }
}
