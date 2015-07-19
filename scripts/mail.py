import smtplib
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_message(_text, bom ):
	msg = MIMEMultipart()
	msg['From'] = 'python <python@python.com'
	msg['To'] = 'James Hammond <james.hammond@bentham.co.uk>'
	msg['Subject'] = 'BOM Changed'				
	textPart = MIMEText(_text + str(bom)+".", 'plain')
	msg.attach(textPart)		
	server = smtplib.SMTP('mail.bentham.co.uk')
	server.sendmail('python <python@python.com','James Hammond <james.hammond@bentham.co.uk>',msg.as_string())
	return