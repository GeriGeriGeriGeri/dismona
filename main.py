import discord
import subprocess
import re
# Python 3.5.2 にて動作を確認
# MySQLdb をインポート
import MySQLdb
client = discord.Client()

# データベース接続とカーソル生成
# 接続情報はダミーです。お手元の環境にあわせてください。
connection = MySQLdb.connect(
    host='localhost', user='root', passwd='laksjd', db='dismona', charset='utf8')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS dismona.id (id VARCHAR(20), address VARCHAR(50));")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

INDB = "aaa"

#message.author.name がユーザー名

@client.event
async def on_message(message):
    # 「/register」で始まるか調べる
    if message.content.startswith("/register"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author.name:
            # メッセージを書きます
            if message.author.name != INDB:
                m = "@" + message.author.name + " さんのアカウントを作成しますね！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, m)
                cmd = "monacoin-cli getaddressesbyaccount " + message.author.name + ""
                rut  =  subprocess.check_output( cmd.split(" ") )
                print ('Creating ' + message.author.name + "'s account..")
                print ("---1---")
                #cursor.execute("insert into dismona.id(id,address) values('message_author', address);")
                resultaddress = rut.decode()
                resultmore = resultaddress.replace('[', '')
                resultmore2 = resultmore.replace(']', '')
                resultmore3 = resultmore2.replace('"', '')
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
                #DEBUG FIN
                print ("---3---")
                cursor.execute("INSERT INTO dismona.id('id', 'address') VALUES ('" + message.author.name + "', '" + resultmore3 + "' )")
                print ("---4---")
                print ('----MYSQL COMMAND START----')
                print ("INSERT INTO dismona.id('id', 'address') VALUES ('" + message.author.name + "', '" + resultmore3 + "' )")
                print ('----MYSQL COMMAND END----')
                print ("---5---")
                m = "@"+ message.author.name + " ,Created your account succefully! your address is " + resultmore3 + " enjoy!"
                print ("---6---")
                await client.send_message(message.channel, m)

            else:
                m = "すみませんがそのアカウント名はすでにこのシステムに登録されているようです。。"
                await client.send_message(message.channel, m)
                print ("failed to create" + message.author.name + "'s account..")

            
            
client.run("NDA5MDkwMTE4OTU2MDg5MzQ0.DVZidQ.1MTSYLrrPL2bNeLMXFVQDPc25Mg")

cursor = conn.cursor()


# https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f
# https://qiita.com/komeiy/items/d6b5f25bf1778fa10e21
#