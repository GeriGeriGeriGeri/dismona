import discord
import subprocess
# Python 3.5.2 にて動作を確認
# MySQLdb をインポート
import MySQLdb
client = discord.Client()

# データベース接続とカーソル生成
# 接続情報はダミーです。お手元の環境にあわせてください。
connection = MySQLdb.connect(
    host='localhost', user='root', passwd='laksjd', db='dismona', charset='utf8')
cursor = connection.cursor()

def res_cmd(cmd):

  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]
# エラー処理（例外処理）
cursor.execute("DROP TABLE IF EXISTS 'dismona_id'")
cursor.execute("""CREATE TABLE IF NOT EXISTS 'dismona_id' (
'id' int(11) NOT NULL,
'name' varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # 「/register」で始まるか調べる
    if message.content.startswith("/register"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            if authorname != INDB:
                m = "@" + message.author.name + " さんのアカウントを作成しますね！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, m)
            # subprocess.check_output(["monacoin-cli getaddressesbyaccount" + message.author.name + ])
                print ('Creating ' + message.author.name + "'s account..")
                cursor.execute("INSERT INTO dismona_id VALUES (authorname, res_cmd(cmd))")
                m = "Created your account succefully! your address is <address>enjoy!"
                await client.send_message(message.channel, m)

            else:
                m = "すみませんがそのアカウント名はすでにこのシステムに登録されているようです。。"
                await client.send_message(message.channel, m)
                print ("failed to create" + message.author.name + "'s account..")
                
            
            
client.run("NDA5MDkwMTE4OTU2MDg5MzQ0.DVZidQ.1MTSYLrrPL2bNeLMXFVQDPc25Mg")
connection.commit()
connection.close()
cur.close
con.close


# https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f
# https://qiita.com/komeiy/items/d6b5f25bf1778fa10e21