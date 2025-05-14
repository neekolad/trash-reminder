from datetime import datetime
from email.message import EmailMessage
import subprocess
import time
import os

# Load environment variables from .env file
# basic .env parser without external libraries
def load_env(path="/home/nikola/projects/trash-can/.env"):
	env = {}
	with open(path) as f:
		for line in f:
			# print(line)
			if '=' in line and not line.startswith('#'):
				key, val = line.strip().split('=', 1)
				env[key] = val
	return env

env = load_env()
print("ENV:",  env)

# Read from .env
recipients = env.get('EMAIL_RECIPIENTS', '').split(',')
sender_name = os.getenv('EMAIL_SENDER_NAME', 'Homeserver')
sender_address = os.getenv('EMAIL_SENDER_ADDRESS')

def techo(s):
	dt = datetime.now()
	dt_clean = dt.strftime("%d-%m-%Y %H:%M:%S")
	return print("[" + dt_clean + "] " + str(s))

def send_mail(message, subject, recepients=None):
	# techo(f"RECEPIENTS: {recipients}")
	if recepients is None:
		raise Exception("No recepients were passed to a function!")

	for recepient in recepients:
		msg = EmailMessage()
		msg['Subject'] = subject
		msg['From'] = f'{sender_name} <{sender_address}>'
		msg['To'] = recepient
		msg.add_alternative(f"{message}", subtype='html')

		# Send message using msmtp
		process = subprocess.Popen(
			['msmtp', '-a', 'gmail', msg['To']],
			stdin=subprocess.PIPE,
		)
		process.communicate(msg.as_bytes())
		time.sleep(2)

def make_message(body, color):
	message = f"""
		<html>
		  <body>
			<h1 style="color:{color};">{body}</h1>
			<br>
			<hr>
			<p style="font-size:14px; color:gray;">Poslato: {day}. {month} {year} - {the_time}</p>
		  </body>
		</html>
		"""
	return message


today = datetime.now()
weekday = today.weekday()
weekday_name = today.strftime("%A")
day = today.strftime("%d")
month = today.strftime("%B")
year = today.strftime("%Y")
the_time = today.strftime("%H:%M:%S")
weeknumber = today.isocalendar()[1]
# techo(f"{today.weekday()}, {weeknumber}")


if weekday == 0 and weeknumber % 2 == 1: # check if its monday AND odd week number, if so - send message for recycle bin
	text = "♻️ Izbaci kantu za recikliranje ♻️"
	color = "darkgreen"
	message = make_message(text, color)
	techo(f"Today is {weekday_name}, sending mail ({', '.join(recipients)}) to put the recycle bin on the street!")
	send_mail(message, "Podsetnik za kantu za djubre", recipients)

elif weekday == 2: 	# check if its wednesday, if so - send message for regular bin
	text = "🗑️ Izbaci obicnu kantu za djubre 🗑️"
	color = "darkblue"
	message = make_message(text, color)
	techo(f"Today is {weekday_name}, sending mail ({', '.join(recipients)}) to put the regular trash can on the street!")
	send_mail(message, "Podsetnik za kantu za djubre", recipients)

else:	# dont send anything just log that we are not sending any mails
	techo(f"Today is {weekday_name}, no mails are being sent..")



# test cron */5 * * * * python3.12 /home/nikola/projects/trash-can/trashcan.py 1>> /home/nikola/projects/trash-can/trashcan.log 2>&1 &
# live cron 30 20 * * * python3.12 /home/nikola/projects/trash-can/trashcan.py 1>> /home/nikola/projects/trash-can/trashcan.log 2>&1 &