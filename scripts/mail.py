import json


#def send_message(_text, bom ):
email = {"from": "accounts@bentham.co.uk","to": ["jameshammond@bentham.co.uk"],"bcc": ["david.hammond@bentham.co.uk"],"subject": "Test","html" : " some mesage ", "replyTo ": "jameshammond@bentham.co.uk"}
json_email = json.dumps (email)

print (json_email)