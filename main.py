#!/usr/bin/python3
import discord
import subprocess
import re
import time
import math
import random
import json
import requests
import decimal
from decimal import (Decimal, ROUND_DOWN)
import apim
import sqlite3
from datetime import datetime

def round_down5(value):
	value = Decimal(value).quantize(Decimal('0.00001'), rounding=ROUND_DOWN)
	return value
# データベースファイルのパス
dbpath = '../dismona.sqlite'
connection = sqlite3.connect(dbpath)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()

# SELECT
cursor.execute('SELECT * FROM rainregistered ORDER BY rainid')

# 全件取得は cursor.fetchall()
rainall = cursor.fetchall()
rainall = str(rainall)
pattern = r'([0-9]+\.?[0-9]*)'
rainall = re.findall(pattern,rainall)

client = discord.Client()
currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

cmda = "monacoin-cli walletpassphrase 0124 32140800"
ruta  =  subprocess.check_output( cmda.split(" ") )
print(ruta)
# データベース接続とカーソル生成
# 接続情報はダミーです。お手元の環境にあわせてください。
#connection = MySQLdb.connect(
#   host='localhost', user='root', passwd='laksjd', db='dismona', charset='utf8')
#cursor = connection.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS dismona.id (id VARCHAR(20), address VARCHAR(50));")


i = "0"
r = requests.get('https://api.coinmarketcap.com/v1/ticker/monacoin/?convert=JPY')
for coin in r.json():
	print(coin["price_jpy"])
	monaprice = coin["price_jpy"]



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print(currenttime)
	print('------')
	await client.change_presence(game=discord.Game(name='/help'))
@client.event

async def on_reaction_add(reaction, user):
	print("reaction has been added")
	print(reaction)
	print("message")
	print(reaction.message)
	print("emoji")
	print(reaction.emoji)
	print("reaction-channel")
	print(reaction.message.channel)
	print("reaction-channel-id")
	print(reaction.message.channel.id)
	print("message-content")
	print(reaction.message.content)
	print("message-author")
	print(reaction.message.author.id)
	print("reaction-by")
	print(user.id)
	print("emoji-hash")
	print(hash(reaction.emoji))
	print("emoji-str")
	print(str(reaction.emoji))
@client.event
async def on_message(message):
	currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	towrite = "" + message.author.name + " said " + message.content + ". userid: " + message.author.id + " channel id: " + message.channel.id + " currenttime: " + currenttime + "\n"
	file = open('/home/raspi0124/alllog.txt', 'a')  #追加書き込みモードでオープン
	file.writelines(towrite)
	print(towrite)
	rainnotify = "425766935825743882"
	rainnotify = client.get_channel('425766935825743882')
	# 「/register」で始まるか調べる
	if message.content.startswith("/register"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		# 送り主がBotだった場合反応したくないので
		if client.user != message.author.name:
			# メッセージを書きます
			m = "<@" + message.author.id + "> さんのアカウントを作成しますね！"
			# メッセージが送られてきたチャンネルへメッセージを送ります
			await client.send_message(message.channel, m)
			cmd = "monacoin-cli getnewaddress " + message.author.id + ""
			rut  =  subprocess.check_output( cmd.split(" ") )
			print ('Creating <' + message.author.id + ">s account.. user ID ")
			print ("---1---")
			#cursor.execute("insert into dismona.id(id,address) values('message_author', address);")
			resultaddress = rut.decode()
			resultmore = resultaddress.replace('[', '')
			resultmore2 = resultmore.replace(']', '')
			resultmore3 = resultmore2.replace('"', '')
			resultmore4 = resultmore3.replace("\n", "")
			resultmore5 = resultmore4.replace(" ", "")
			print ("---2---")
			#DEBUG
			print ("---decoded---")
			print (resultaddress)
			print ("-----------------")
			print ("---address---")
			print(resultaddress)
			print ("----------------")
			print ("---resultmoreaddress---")
			print (resultmore3)
			print ("------------------------------")
			print ("---removednaddress---")
			print (resultmore4)
			print("-------------------------------")
			print ("---removedsaddress---")
			print (resultmore5)
			print("-------------------------------")
			#DEBUG FIN
			print ("---3---")
			#cursor.execute("INSERT INTO dismona.id(id, address) VALUES ('" + message.author.id + "', '" + resultmore5 + "' )")
			print ("---4---")
			#print ('----MYSQL COMMAND START----')
			#print ("INSERT INTO dismona.id(id, address) VALUES ('" + message.author.id + "', '" + resultmore5 + "' )")
			#print ('----MYSQL COMMAND END----')
			print ("---5---")
			currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
			m = "<@" + message.author.id + ">, successfully created an account for you! Your new address is " + resultmore5 + ", enjoy!\n(message created on " + currenttime + ")"
			print ("---6---")
			await client.send_message(message.channel, m)

	if message.content.startswith("/rera"):
			# データベース接続とカーソル生成
		username = message.author.id

		# エラー処理（例外処理）
		try:
		# INSERT
			cmd = "monacoin-cli getbalance " + username + ""
			rut  =  subprocess.check_output( cmd.split(" ") )
			balance = rut.decode()
			if balance > "0.01":
				fee = "0.01"
				cursor.execute("INSERT INTO rainregistered (rainid) VALUES (?)", (username,))
				cmd = "monacoin-cli move "  + message.author.id + " fee " + fee + ""
				ruta  =  subprocess.check_output( cmd.split(" ") )
				print(ruta)
				m = "Success"
				await client.send_message(message.channel, m)
			else:
				m = "Not enough balance to take fee. Please note that fee of 0.01mona will be charged for registering rain.(only once.)"
				await client.send_message(message.channel, m)
		except sqlite3.Error as e:
			print('sqlite3.Error occurred:', e.args[0])
			m = "DB error. DB might removed or you already signed up."
			await client.send_message(message.channel, m)

		# 保存を実行（忘れると保存されないので注意）
		connection.commit()


	if message.content.startswith("/balance"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		# 送り主がBotだった場合反応したくないので
		if client.user != message.author.name:
			# メッセージを書きます
				m = "<@" + message.author.id + "> さんの残高チェック中.."
			# メッセージが送られてきたチャンネルへメッセージを送ります
				await client.send_message(message.channel, m)
				cmd = "monacoin-cli getbalance " + message.author.id + ""
				rut  =  subprocess.check_output( cmd.split(" ") )
				balance = rut.decode()
				currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
				m = "<@" + message.author.id + ">, you currently have  " + balance + " mona!\n(message created on " + currenttime + ")"
				print ("---6---")
				await client.send_message(message.channel, m)
	if message.content.startswith("/deposit"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		# 送り主がBotだった場合反応したくないので
		if client.user != message.author.name:
			# メッセージを書きます
				m = "<@" + message.author.id + "> アドレスを確認中..."
			# メッセージが送られてきたチャンネルへメッセージを送ります
				await client.send_message(message.channel, m)
				cmd = "monacoin-cli getaddressesbyaccount " + message.author.id + ""
				rut  =  subprocess.check_output( cmd.split(" ") )
				address = rut.decode()
				address2 = address.replace('[', '')
				address3 = address2.replace(']', '')
				address3 = address2.replace('\n', '')
				currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
				m = "<@" + message.author.id + ">, the following are your deposit addresses:" + address3 + "\n(message created on " + currenttime + ")"
				await client.send_message(message.channel, m)
	if message.content.startswith("/list"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		# 送り主がBotだった場合反応したくないので
		if client.user != message.author.name:
			# メッセージを書きます
				m = "<@" + message.author.id + "> アドレスを確認中..."
			# メッセージが送られてきたチャンネルへメッセージを送ります
				await client.send_message(message.channel, m)
				cmd = "monacoin-cli getaddressesbyaccount " + message.author.id + ""
				rut  =  subprocess.check_output( cmd.split(" ") )
				address = rut.decode()
				address2 = address.replace('[', '')
				address3 = address2.replace(']', '')
				currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
				m = "<@"+ message.author.id + ">,your address is" + address3 + " \n Created message at " + currenttime + ""
				await client.send_message(message.channel, m)
	if message.content.startswith("/withdraw"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		#getbalance
		cmda = "monacoin-cli getbalance " + message.author.id + ""
		ruta  =  subprocess.check_output( cmda.split(" ") )
		balancea = ruta.decode()
		#okikae
		rmessage = message.content.replace('/withdraw', '')
		print(rmessage)
		pattern = r'([+-]?[0-9]+\.?[0-9]*)'
		print(re.findall(pattern,rmessage))
		withdrawinfo = re.findall(pattern,rmessage)
		print(withdrawinfo[0])
		withdrawamount = withdrawinfo[0]
		rmessage = rmessage.replace(withdrawamount, '')
		withdrawto = rmessage.replace(' ', '')
		fee = "0.005"
		rewithdrawamount = float(withdrawamount) - float(fee)
		rewithdrawamount = str(rewithdrawamount)
		print("--withdrawto--")
		print(withdrawto)
		print("--withdrawamount--")
		print(withdrawamount)
		print("--rewithdrawamount--")
		print(rewithdrawamount)
		if withdrawamount >= "0.01":
			if balancea >= "0":
				if balancea >= "0.01":
					await client.add_reaction(message, '👌')
					cmd = "monacoin-cli sendfrom " + message.author.id + " " + withdrawto + " " + rewithdrawamount + ""
					rut  =  subprocess.check_output( cmd.split(" ") )
					cmd = "monacoin-cli move " + message.author.id + " fee " + fee + ""
					ruta  =  subprocess.check_output( cmd.split(" ") )
					print(rut)
					rut = rut.decode()
					m = "<@" + message.author.id + ">, " + rewithdrawamount + "mona has been withdrawn to " + withdrawto + ". Transaction details can be found here: https://mona.chainsight.info/tx/" + rut + "\n(message created on " + currenttime + ")"
					await client.send_message(message.channel, m)
					cmda = "monacoin-cli getbalance " + message.author.id + ""
					ruta  =  subprocess.check_output( cmda.split(" ") )
					balancea = ruta.decode()
					if balancea <= "0":
						defo = "0"
						amounttosendback = float(defo) - float(balancea)
						print("--amounttosendback--")
						print(amounttosendback)
						amounttosendback = str(amounttosendback)


						cmd = "monacoin-cli move fee "  + message.author.id + " " + amounttosendback + ""
						ruta  =  subprocess.check_output( cmd.split(" ") )
						print(ruta)

				else:
					m = "<@" + message.author.id + "> sorry, failed to complete your request: you do not have enogh mona for withdraw. \n please note that the minimum withdraw amount is 0.01mona.(message created on " + currenttime + ")"
					await client.send_message(message.channel, m)
			else:
				m = "<@" + message.author.id + ">sorry, failed to complete your request: you do not have any mona at all!(message created on " + currenttime + ")"
				await client.send_message(message.channel, m)
		else:
			m = "<@" + message.author.id + "> sorry, failed to complete your request: you do not have enogh mona for withdraw. \n please note that the minimum withdraw amount is 0.01mona.(message created on " + currenttime + ")"
			await client.send_message(message.channel, m)
	if message.content.startswith("/rain"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		cmda = "monacoin-cli getbalance " + message.author.id + ""
		ruta  =  subprocess.check_output( cmda.split(" ") )
		balancea = ruta.decode()
		await client.add_reaction(message, '👌')
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		message2 = message.content.replace('/rain ', '')
		pattern = r'([+-]?[0-9]+\.?[0-9]*)'
		raininfo = re.findall(pattern,message2)
		print("--numbertorain--")
		print(raininfo[0])
		print("--amounttorain--")
		print(raininfo[1])
		sum = float(raininfo[1]) / float(raininfo[0])
		print(sum)
		sum = round(sum,6)
		print(sum)
		sum = str(sum)
		cursor.execute('SELECT * FROM rainregistered ORDER BY rainid')

		# 全件取得は cursor.fetchall()
		rainall = cursor.fetchall()
		print(rainall)
		rainall = str(rainall)
		pattern = r'([0-9]+\.?[0-9]*)'
		rainall = re.findall(pattern,rainall)
		print(rainall)
		if balancea >= raininfo[1]:
			if raininfo[1] > "0.01":
				if sum > "0.001":
					m = "you will rain " + sum + "mona to " + raininfo[0] + " people."
					await client.send_message(message.channel, m)
					sum = str(sum)
					numbertosend = raininfo[0]
					numbertosend = int(numbertosend)
					maxrain = len(rainall)
					print(maxrain)
					m = "Rain started by <@" + message.author.id + "> at #" + message.channel.name + ""
					await client.send_message(rainnotify, m)
					for var in range(0, numbertosend):
						tosend = random.randrange(maxrain)
						print(tosend)
						print("--rondomfinish--")
						tosend = int(tosend)
						tosend = rainall[tosend]
						tosend = str(tosend)
						print("--startcommand--")
						cmd = "monacoin-cli move " + message.author.id + " " + tosend + " " + sum + ""
						rut  =  subprocess.check_output( cmd.split(" ") )
						print(rut)
						m = "Raining" + sum + "mona to <@" + tosend + ">.."
						await client.send_message(rainnotify, m)
					m = "finished raining " + sum + "mona to " + raininfo[0] + "people! total amount was " + raininfo[1] + "mona! Rained by <@" + message.author.id + ">"
					await client.send_message(message.channel, m)
					m = "finished raining " + sum + "mona to " + raininfo[0] + "people! total amount was " + raininfo[1] + "mona! Rained by <@" + message.author.id + ">"
					await client.send_message(rainnotify, m)
					print(rut)
				else:
					m = "負荷軽減のため1人当たりのrainが0.001mona以下になるrainは制限しています。"
			else:
				m = "Due to Server load, it is not allowed to make total amount of rain less then 0.01."
				await client.send_message(message.channel, m)
		else:
			m = "not enough fund.. double check amount to rain."
			await client.send_message(message.channel, m)
	if message.content.startswith("/ban"):
		username = message.author.id
		banallow = ["326091178984603669", "294470458013908992"]
		noban = ["326091178984603669", "294470458013908992"]
		if username in banallow:
			message2 = message.content
			pattern = r'([+-]?[0-9]+\.?[0-9]*)'
			tipinfo = re.findall(pattern,message2)
			print(tipinfo[0])
			banto = tipinfo[0]
			if banto not in noban:
				cursor.execute("INSERT INTO baned (banedid) VALUES (?)", (banto,))
				connection.commit()
				cursor.execute("INSERT INTO baned (banfromid) VALUES (?)", (username,))
				m = "<@" + username + ">ユーザー <@" + banto + "> をおみくじの使用からBANしました。"
				await client.send_message(message.channel, m)
			else:
				m = "このユーザーをBANすることは禁止されています。"
		else:
			m = "You are not allowed to do that!"
			await client.send_message(message.channel, m)

	if message.content.startswith("/tip"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		message2 = message.content.replace('/tip', '')
		print (message2)
		pattern = r'([+-]?[0-9]+\.?[0-9]*)'
		print(re.findall(pattern,message2))
		tipinfo = re.findall(pattern,message2)
		print(tipinfo[0])
		print(tipinfo[1])
		cmd = "monacoin-cli getbalance " + message.author.id + ""
		rut  =  subprocess.check_output( cmd.split(" ") )
		balance = rut.decode()
		num2 = 100000000
		balance = float(balance) * float(num2)
		print ("balance")
		print(balance)
		tipto = tipinfo[0]
		tipamount = tipinfo[1]
		print("tipamount")
		print(tipamount)
		tipamount = float(tipamount) * float(num2)
		print("multiplyed tipamount")
		print(tipamount)
		minimumtip = "1"
		minimumtip = float(minimumtip)
		if tipamount <= balance:
			if tipamount >= minimumtip:
				try:
					username = message.author.id
					tipamount = float(tipamount) / float(num2)
					tipamount = str(tipamount)
					cmd2 = "monacoin-cli move " + message.author.id + " " + tipto + " " + tipamount + ""
					rut2  =  subprocess.check_output( cmd2.split(" ") )
					m = "<@" + message.author.id + "> sent " + tipamount + " mona to <@" + tipto + ">!\n(message created on " + currenttime + ")"
					await client.send_message(message.channel, m)
					cursor.execute("INSERT INTO tiped (id) VALUES (?)", (username,))
					connection.commit()
					cursor.execute("INSERT INTO tiped (id) VALUES (?)", (tipto,))
				except subprocess.CalledProcessError as e:
					eout = e.output.decode()
					m = "<@" + message.author.id + ">, sorry, failed to complete your request: <@" + tipto + "> is not yet registered.\n(message created on " + currenttime + ")"
					await client.send_message(message.channel, m)
			else:
				m = "<@" + message.author.id + ">, sorry, failed to complete your request: your tip must meet the minimum of 10 watanabe (0.00000010 Mona).\n(message created on " + currenttime + ")"
				await client.send_message(message.channel, m)
		else:
			m = "<@"+ message.author.id + ">, sorry, failed to complete your request: you do not have enough Mona in your account, please double check your balance and your tip amount.\n(message created on " + currenttime + "\n DEBUG: tipamount:" + tipamount + " balance:" + balance + " "
			await client.send_message(message.channel, m)
	if message.content.startswith("/admin info"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		cmd = "monacoin-cli getinfo"
		rut  =  subprocess.check_output( cmd.split(" ") )
		cmd2 = "monacoin-cli getbalance"
		rut2 = subprocess.check_output( cmd2.split(" "))
		cmd3 = "monacoin-cli listaccounts"
		rut3 = subprocess.check_output( cmd3.split(" "))
		cmd4 = "monacoin-cli listtransactions"
		rut4 = subprocess.check_output( cmd4.split(" "))
		getinfo = rut.decode()
		getbalance = rut2.decode()
		listaccounts = rut3.decode()
		listtransactions = rut4.decode()
		if message.author.id == "326091178984603669":
			m = "Verfifying.. wait a monemt"
			await client.send_message(message.channel, m)
			m = "Successfully verified you as an admin, here is the info you requested:"
			await client.send_message(message.channel, m)
			m = "```getinfo result: " + getinfo + "\n```"
			await client.send_message(message.channel, m)
			time.sleep(1)
			m = "```getbalance result: " + getbalance + "\n```"
			await client.send_message(message.channel, m)
			time.sleep(1)
			m = "```listaccounts result: " + listaccounts + "\n```"
			await client.send_message(message.channel, m)
			time.sleep(1)
			m = "```listtransactions result: " + listtransactions +"\n ```"
			await client.send_message(message.channel, m)
			time.sleep(1)
		else:
			m = "Haha, you don't have permission to do that! Your request has been logged and reported to the admin! (but the admin probably won't care about it, so don't worry.)"
			await client.send_message(message.channel, m)
	if message.content.startswith("/adminc"):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		if message.author.id == "326091178984603669":
			await client.add_reaction(message, '👌')
			message2 = message.content.replace('/adminc', '')
			print(message2)
			cmd = "monacoin-cli" + message2 + ""
			rut = subprocess.check_output( cmd.split(" "))
			result = rut.decode()
			await client.send_message(message.channel, result)
		else:
			m = "sorry, but you are not allowed to do that!"
			await client.send_message(message.channel, m)
	if message.content.startswith('/members'):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		for server in client.servers:
			for member in server.members.id:
				print (member)
				list_of_ids = [m.id  for m in server.members]
				print(list_of_ids)
	if message.content.startswith('/adminregister'):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		if message.author.id == "326091178984603669":
			message2 = message.content.replace('/adminregister', '')
			message3 = message2.replace(' ', '')
			print(message3)
			cmd = "monacoin-cli getnewaddress " + message3 + ""
			rut = subprocess.check_output( cmd.split(" "))
			address = rut.decode()
			m = "issued account for <@" + message3 + ">. address is " + address + "."
			await client.send_message(message.channel, m)
		else:
			m = "sorry, but you are not allowed to do that!"
			await client.send_message(message.channel, m)
	if message.content.startswith('/adminbalance'):
		cmda = "monacoin-cli walletpassphrase 0124 10"
		ruta  =  subprocess.check_output( cmda.split(" ") )
		print(ruta)
		await client.add_reaction(message, '👌')
		if message.author.id == "326091178984603669":
			message2 = message.content.replace('/adminbalance', '')
			message3 = message2.replace(' ', '')
			print(message3)
			cmd = "monacoin-cli getbalance " + message3 + ""
			rut = subprocess.check_output( cmd.split(" "))
			balance = rut.decode()
			m = "<@" + message3 + "> 's balance are " + balance + "mona."
			await client.send_message(message.channel, m)
		else:
			m = "sorry, but you are not arrowed to do that!"
			await client.send_message(message.channel, m)
	if message.content.startswith("/image"):
		await client.add_reaction(message, '👌')
		with open('../image.jpg', 'rb') as f:
			await client.send_file(message.channel, f)


	if message.content.startswith("/hello"):
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		m = "こんにちは! <@" + message.author.id + "> さん！"
		await client.send_message(message.channel, m)
		await client.add_reaction(message, '👌')
	if message.content.startswith("/love"):
		def love():
			kuji = ["0", "1", "2", "3", "1", "2", "7", "1", "2", "3", "1", "2", "3", "2", "3", "2", "0", "0"]
			result = random.choice(kuji)
			return result
		kuji = ["うーん。。お断りさせていただきます", "お友達から初めましょう", "。。。", "お友達から初めましょう。", "あなたのことなんか大っ嫌い!", "お友達で居ましょう。", "うーん。。お断りさせていただきます", "自分もあなたのことが好きでした"]
		result = love()
		print("result")
		print(result)
		result = int(result)
		m = kuji[result]
		print("m")
		print(m)
		if result == "7":
			await client.add_reaction(message, '👌')
		await client.send_message(message.channel, m)

	if message.content == "/help":
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		embed = discord.Embed(title="Monage Discord Edition - Help")
		embed.set_footer(text=" Created message at | " + currenttime + "")
		embed.add_field(name="/help", value=" ヘルプを表示します")
		embed.add_field(name="/register", value="あなたの財布を新しく作成します <Create your address>")
		embed.add_field(name="/deposit - /list", value="あなたの所有しているアドレスを一覧表示します <List all address you have generated>")
		embed.add_field(name="/withdraw ``<amount to withdraw> <address to send>``", value="指定されたmonaを指定されたアドレスに送ります <Withdraw specified amount of Mona available to specified address>")
		embed.add_field(name="/tip ``<User to send Mona> <amount to tip> <Comment (optional)>``", value="指定されたmonaを指定されたユーザーに送ります <Tip specified amount of mona to specified user>")
		embed.add_field(name="/rain ``<number of people to tip> <total amount to tip>``", value=" 指定された金額のmonaをランダムに配ります。<Tip specified amount to random multiple people. You can choose the number of people to tip (Currently for admin only due to technical difficulties.)>")
		embed.add_field(name="/rera", value="rain受け取りに参加します。手数料は0.01monaです。 <Sign up to be a rain-reciever. fee is 0.01 mona currently, and might go up.>")
		embed.add_field(name="/omikuzi", value="おみくじ。おまけでmonaもらえます<Let see how fortunate you are! You can also get some mona!>")
		embed.add_field(name="/credit", value="クレジットを表示。 <Show credit>")
		await client.send_message(message.channel, embed=embed)
	if message.content == "/omikuzi" or message.content == "/omikuji":
		username = message.author.id
		cursor.execute('SELECT id FROM gived')
		# 全件取得は cursor.fetchall()
		gived = cursor.fetchall()
		print("gived")
		print(gived)
		gived = str(gived)
		cursor.execute('SELECT banedid FROM baned')
		baned = cursor.fetchall()
		cursor.execute('SELECT * FROM tiped')
		tiped = cursor.fetchall()
		print(tiped)
		tiped = str(tiped)
		pattern = r'([0-9]+\.?[0-9]*)'
		tiped = re.findall(pattern,tiped)
		print("banned")
		print(baned)
		print("tiped")
		print(tiped)
		baned = str(baned)
		cmd = "monacoin-cli getbalance " + username + ""
		balance = subprocess.check_output( cmd.split(" "))
		minlimit = "0.001"
		balance = str(balance)
		balance = re.findall(pattern,balance)
		await client.add_reaction(message, '👌')
		if username not in gived:
			if username not in baned:
				if username in tiped:
					def omikuji():
						kuji = ["0", "1", "2", "3", "1", "2", "7", "1", "2", "3", "1", "2", "3", "2", "3", "2", "0", "0"]
						result = random.choice(kuji)
						return result
					kuji = ["凶", "小吉", "中吉", "大吉", "凶", "小吉", "中吉", "超大吉"]
					result = omikuji()
					print("result")
					print(result)
					result = int(result)
					print("result2")
					print(result)
					resultp = kuji[result]
					print("resultp")
					print(resultp)
					resultp = str(resultp)
					result = float(result) + float("1")
					result = int(result)
					result = str(result)
					m = "貴方の今日の運勢は" + resultp + "です!\n0.000" + result + "Mona送りますね！"
					await client.send_message(message.channel, m)
					cursor.execute("INSERT INTO gived (id) VALUES (?)", (username,))
					m = "/tip <@" + username + "> 0.000" + result + " おみくじtipです！次挑戦できるのは日本時間で明日です！"
					await client.send_message(message.channel, m)
					connection.commit()
				else:
					m = "スパム対策のためにTipした、またはされたことのないひとはおみくじを実行することができません。。だれかにtipするかtipされてからもう一回実行おねがいします\nTo prevent spamming, user who never tip or tiped by someone before are not allowed to execute omikuji. please tip someone or get tiped by someone using /tip command."
					await client.send_message(message.channel, m)
			else:
				cursor.execute('SELECT banfromid FROM baned WHERE banedid = ' + username + '')
				banfromid = cursor.fetchall()
				banfromid = str(banfromid)
				m = "You are not allowed to /omikuzi! \n Detail:You are baned by <@" + banfromid + ">"
				await client.send_message(message.channel, m)
		else:
			m = "すでに今日におみくじをされているようです。。明日戻ってきてね！"
			await client.send_message(message.channel, m)


	if message.content.startswith("/credit"):
		await client.add_reaction(message, '👌')
		currenttime = (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		m = "```-----------------------------------------------------------------------------------  \
		\n このプログラムは以下の方たちの協力によって完成しました。この場にて改めて感謝します。(敬称略) \
		\n ---開発、制作--- \
		\n raspi0124 \
		\n ---開発協力--- \
		\n はるまど(Gitlabの提供。勝手にモナオクのgitlab使っちゃってすみませんm(_ _)m) \
		\n kakarichyo(クローズドアルファにおけるテスト) \
		\n ポテト(クローズドアルファにおけるテスト) \
		\n MGQ(アドバイス) \
		\n Discordサーバー 「MGQ club」のみなさん(テスト全般) \
		\n 人畜無害 (rainコマンドに関する助言) \
		\n W.S Wsans(W.S 笑サンズ) (Discord.pyについてのアドバイス) \
		\n ぱい (Discord.pyについてのアドバイス \
		\n Monageと遊ぶ鯖に参加してくださった皆さん(テスト) \
		\n lae(アドバイス,英語文法監修) \
		\n 両親(匿名にしておきます) \
		\n ---使用させていただいたプログラム--- \
		\n Python \
		\n Discord.py \
		\n Sublime Text3 \
		\n Nano \
		\n Gitlab \
		\n Ubuntu \
		\n ---その他--- \
		\n 脇山P (WordPressプラグイン、monage作成の際に頂いたmonaをVPS代にありがたくつぎ込ませてもらっています。) \n Created message at " + currenttime + "\
		\n ----------------------------------------------------------------------------------- \
		```"
		await client.send_message(message.channel, m)
client.run("NDA5MDkwMTE4OTU2MDg5MzQ0.DVZidQ.1MTSYLrrPL2bNeLMXFVQDPc25Mg")
connection.close()
# https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f
# https://qiita.com/komeiy/items/d6b5f25bf1778fa10e21
