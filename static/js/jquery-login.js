document.onkeydown = function (e) {
var theEvent = window.event || e;
var code = theEvent.keyCode || theEvent.which;
if (code == 13) {
$("#login").click();
$("#reg").click();
}
} 
$(function(){
	if(($.browser.msie&&($.browser.version == "8.0")) ||($.browser.msie&&($.browser.version == "7.0"))){
		window.location.href='/browsers/'
	}
	$("#UserEmail").focus(function(){
		$("#msg").remove();
	});
	$("#user").focus(function(){
		$("#msg").remove();
	});	
	$("#pass").focus(function(){
		$("#msg").remove();
	});
	$("#EmailCode").focus(function(){
		$("#msg").remove();
	});
	$("#valicode").focus(function(){
		$("#msg").remove();
	});
	 var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
	$("#login").click(function(){
                 var user = $("#user").val();
		var pass = $('#pass').val();
		var LoginType = $('.type').val();
		//var originator = $('#originator').val();
		if(user==""){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的用户名</div></div>');
			//$("#ym").focus();
			return false;
		}
		if(pass==""){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的密码</div></div>');
			//$("#hdip").focus();
			return false;		
		}
                        var params =  {"user":user,"pass":pass};
                        var ParamsToStr = JSON.stringify(params);
		$.ajax({
			type: "POST",
			url: "/api/",
			dataType: "json",
			data: {"method":'GET',"action":"login","params":ParamsToStr},
			beforeSend: function(){
				//$('<div id="msg" />').addClass("loading").html("正在登录...").css("color","#999").appendTo('.sub');
				//$("#yz").css("display","none");
				$('<div id="loading" />').html("<div class=\"load\">正在登录...<\/div>").appendTo('body');
			},			
			success: function(data){
				if(data.code != 0){
					$("#msg").remove();
					$(".home-logo").after('<div id="msg"><div class="msgcon">'+data.msg+'</div></div>');
				}else{
                                                        window.location.href = '/'+data.region+'/home/';
                                                }
			}
		});
	});
	$("#ConfireEmail").click(function(){
		$("#EmailCode").val('');
		var UserEmail = $("#UserEmail").val();
		if(UserEmail==""){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的邮箱地址</div></div>');
			//$("#UserEmail").focus();
			return false;
		}
		if (!reg.test(UserEmail)){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">请输入正确的邮箱格式</div></div>');
			return false;
		}
		$("#ConfireEmail").hide();

		$.ajax({
				type: "POST",
				url: "/account/?action=EmailCode",
				dataType: "text",
				data: {"UserEmail":UserEmail},
				beforeSend: function(){
						//$('<div id="msg" />').addClass("loading").html("正在登录...").css("color","#999").appendTo('.sub');
						//$("#yz").css("display","none");
						$('<div id="loading" />').html("<div class=\"load\">正在登录...<\/div>").appendTo('body');
				},
				success: function(data){
						if(data=='0'){
								$("#msg").remove();
								$(".home-logo").after('<div id="msg"><div class="msgcon">用户名已存在，请重新输入用户名</div></div>');
						}
						if(data=='1'){
								$("#EmailCode").show();
								$("#ConfireEmail").hide();
								$("#msg").remove();
								$(".home-logo").after('<div id="msg"><div class="msgcon">请登陆邮件查看验证码</div></div>');
						}
				}
		});	
	})
$("#reg").click(function(){
        var UserEmail = $("#UserEmail").val();
        var pass = $("#pass").val();
		var EmailCode = $("#EmailCode").val();
		var valicode = $("#valicode").val();
        //var originator = $('#originator').val();
        if(UserEmail==""){
			$("#msg").remove()
            $(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的邮箱地址</div></div>');
            //$("#UserEmail").focus();
            return false;
        }
		if (!reg.test(UserEmail)){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">请输入正确的邮箱格式</div></div>');
			return false;
		}
        if(pass==""){
			$("#msg").remove();
            $(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的密码</div></div>');
            //$("#pass").focus();
            return false;
        }
		var passlength = pass.length;
		if (passlength < 6){
			$("#msg").remove();
			$(".home-logo").after('<div id="msg"><div class="msgcon">您输入的密码不能小于6位</div></div>');
			return false;
		}
		
        if(EmailCode==""){
			$("#msg").remove();
            $(".home-logo").after('<div id="msg"><div class="msgcon">请输入您的邮箱验证码</div></div>');
            //$("#UserEmail").focus();
            return false;
        }
        $.ajax({
                type: "POST",
                url: "/account/?action=reg",
                dataType: "text",
                data: {"UserEmail":UserEmail,"pass":pass,"EmailCode":EmailCode,"valicode":valicode},
                beforeSend: function(){
                        //$('<div id="msg" />').addClass("loading").html("正在登录...").css("color","#999").appendTo('.sub');
                        //$("#yz").css("display","none");
                        $('<div id="loading" />').html("<div class=\"load\">正在登录...<\/div>").appendTo('body');
                },
                success: function(data){
                        if(data=='0'){
							$("#msg").remove();
							$(".home-logo").after('<div id="msg"><div class="msgcon">用户名已存在，请重新输入用户名</div></div>');
                        }
                        if(data=='1'){
                            window.location.href='/shj1/home'
                        }
						if(data=='2'){
							$("#msg").remove();
							$(".home-logo").after('<div id="msg"><div class="msgcon">验证码不正确</div></div>');
						}
						if(data=='3'){
							$("#msg").remove();
							$(".home-logo").after('<div id="msg"><div class="msgcon">邮箱验证码不正确</div></div>');
						}
						if(data=='4'){
							$("#msg").remove();
							$(".home-logo").after('<div id="msg"><div class="msgcon">邮箱验证码与邮箱不统一</div></div>');	
						}
                }
        });
        });
})
