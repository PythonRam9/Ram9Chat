import json
import datetime
import random
from flask import request, Flask

with open('msg_storage.json') as json_file:
  msg_storage = json.load(json_file)

app = Flask('app')

def salt_make(LENGTH):
  chars = "abcdefghijklmnopqrstuvwxyz1234567890"
  char_list = [random.choice(chars) for i in range(LENGTH)]
  salt = "".join(char_list)
  return salt

@app.route('/')
def main():
  return render_templatev('main_page.html')

@app.route('/v1/api/send')
def hello_world():
  room_id = request.args.get('id')
  Name = request.args.get('n')
  Message = request.args.get('m')
  Date = str(datetime.datetime.today())[0:-10]
  gen_id = salt_make(5)
  good = ''
  while good == '':
    if gen_id in msg_storage['rooms']:
      gen_id = salt_make(5)
    else:
      good = True
  msg_storage['rooms'][f'{room_id}'][f'{Name}|{Date}|{gen_id}'] = Message
  with open('msg_storage.json', 'w') as fp:
    json.dump(msg_storage, fp)
  return 'if u are seeing this, ur request might have went through, maybe not'

@app.route('/room')
def chat_room():
  room_id = request.args.get('id')
  messages = ''
  for message_info, message in reversed(msg_storage['rooms'][f'{room_id}'].items()):
    messages += f'<strong>{message_info.split("|")[0]}</strong> | <strong>{message_info.split("|")[1]}</strong><br>{message}<br><br>'

  return f'''<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<style>
body {{
	text-align: center;
	background-color: #fffcec;
}}
.settings {{
	position: fixed;
	top: 10px;
	right: 10px;
}}
.glow {{
	font-size: 80px;
	color: #fff;
	text-align: center;
	animation: glow 1s ease-in-out infinite alternate
}}
@-webkit-keyframes glow {{
	from {{
		text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #e60073, 0 0 40px #e60073, 0 0 50px #e60073, 0 0 60px #e60073, 0 0 70px #e60073
	}}
	to {{
		text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6
	}}
}}
</style>

<h1 class="glow">Ram9-Chat</h1>
<br>
<input type="text" id="msg" placeholder="Message">
<button type="button" onclick="send_message()">Send Message</button>
<button class="settings" type="button" onclick="settings()">Settings</button>
<br>
<br>

{messages}

<script>
function send_message() {{
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", ("https://chat.webhooks.repl.co/v1/api/send?n=" + (document.cookie.split("=")[1]) + "&m=" + document.getElementById("msg").value), false);
	xmlHttp.send(null);
	window.location.reload(true);
}};

function settings() {{
	window.location.replace("https://chat.webhooks.repl.co/settings");
}};

function set_up() {{
	if(document.cookie.length < 2) {{
		window.location.replace("https://chat.webhooks.repl.co/settings")
	}}
}};
window.onload = set_up();
</script>'''

@app.route('/settings')
def settings():
  return render_template('account_setup.html')

@app.route('/v1/api/create')
def create_room():
  try:
    Name = request.args.get('n')
    gen_id = salt_make(5)
    good = ''
    while good == '':
      if gen_id in msg_storage['rooms']:
        gen_id = salt_make(5)
      else:
        good = True
    msg_storage['rooms'][f'{gen_id}'] = Name
    with open('msg_storage.json', 'w') as fp:
      json.dump(msg_storage, fp)
    return 'success'
  except:
    return 'faliure'

@app.route('/setup')
def priv():
  return render_template('create_room.html')

app.run(host='0.0.0.0', port=8080)
