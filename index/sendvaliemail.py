# coding=utf-8
import smtplib

from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
def sendmail(ToMail,UId):
	HOST = "smtp.ym.163.com"
	SUBJECT = "欢迎注册牛犊云(NCloud)(请不要回复此邮件)"
	TO = ToMail
	FROM = "yun@niuduz.com"
	Toname = ToMail.split('@')
	html = """
			<table align="center" width="650">
				<tr>
					<td><h1 style="color:#40AA53">牛犊云</h1></td>
				</tr>
				<tbody style="display:block;border:1px solid #D1FFD1;border-top:5px solid #40AA53;">
					<tr>
						<td><p style="padding:20px">%s,您好</p></td>
					</tr>
					<tr>
						<td><p style="padding:10px 0 10px 20px;">欢迎您注册成为<span style="font-weight:700">牛犊云</span>会员！</p></td>
					</tr>	
					<tr>
						<td><p style="padding:10px 0 0 20px;">以下您注册邮箱的验证码：</p></td>
					</tr>
					<tr>
						<td><p style="font-weight:700;padding:0 0 0 20px">%s</p></td>
					</tr>
					<tr>
						<td><p style="margin:20px;padding:15px 0 20px 0;border-top:1px solid #717171">想了解更多信息,请访问 <a href="">http://www.niuduz.com</a></p></td>
					</tr>
				</tbody>			
			</table>
	""" % (Toname[0],UId)
	#msg = MIMEMultipart('alternative')
	#html_part = MIMEText(html,'html')
	#html_part.set_charset('gbk')
	#msg.attach(html_part)
	msg  = MIMEText(html,'html','utf-8')
	msg["Accept-Language"] = "zh-CN"
	msg["Accept-Charset"] = "ISO-8859-1,utf-8"
	msg['Subject'] = SUBJECT
	msg['From'] = r"%s <yun@niuduz.com>" % Header("NCloud","utf-8")
	msg['To'] = TO
	try:
		server = smtplib.SMTP()
		server.connect(HOST,"25")
		server.login("yun@niuduz.com","Niuduz.com")
		server.sendmail(FROM,TO,msg.as_string())
		server.quit()
	except Exception, e:
		print "shibai："+str(e)
