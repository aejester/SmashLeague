import discord
import sqlite3
import random

conn = sqlite3.connect("database.db")
c = conn.cursor()

donn = sqlite3.connect("matches.db")
d = donn.cursor()

TOKEN = "NTU4NDAyOTU1MjA5MDgwODMz.D3WVJQ.eFS9vyKIwgXTwozO6cYHi_13akM"
alphabet = "abcdefghijklmnopqrstuvwxyz"

client = discord.Client()

(top_low, top_high) = (4000000, 4999999)
(mid_low, mid_high) = (3000000, 3999999)
(low_low, low_high) = (2000000, 2999999)
(lowest_low, lowest_high ) = (1000000, 1999999)


def recur(gsp):
    if int(gsp) > top_high:
        increase()
        recur(gsp)

def increase():
    top_high += 1000000
    top_low += 1000000
    mid_high += 1000000
    mid_low += 1000000
    low_high += 1000000
    low_low += 1000000
    lowest_high += 1000000

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("------------")

top_queue = []
mid_queue = []
low_queue = []
lowest_queue = []

@client.event
async def on_message(message):
    prefix = "!"
    if message.author == client.user:
        return
    if not message.content.startswith(prefix):
        return
    arr = message.content.split(" ")
    command = arr[0].replace(prefix, "")
    args = []
    for i in range(1, len(arr)):
        args.append(arr[i])
    if command == "signup":
        x = "INSERT INTO `users` VALUES ('{}', '{}', '{}', {}, {})".format(message.author.name, message.author.id, "none", 0, 0.0)
        print(x)
        c.execute(x)
        conn.commit()
        await client.send_message(message.author, """
        Below, use the following commands:
        `!username <name>` - no spaces or special characters. you can use this as many times as you want.
        `!gsp <number>` - this determines your initial *Smash League* rank. if this changes at any point, come back and re-do this command. do not use commas in number
        """)
    if command == "username":
        c.execute("UPDATE users SET name='{}' WHERE id='{}'".format(args[0], message.author.id))
        conn.commit()
        await client.send_message(message.author, "Updated username to: `{}`".format(args[0]))
    if command == "gsp":
        c.execute("UPDATE users SET gsp='{}' WHERE id='{}'".format(args[0], message.author.id))
        conn.commit()
        recur(args[0])
        await client.send_message(message.author, "Updated your GSP to: `{}`".format(args[0]))
    if command == "q":
        c.execute("SELECT * FROM users WHERE id='{}'".format(message.author.id))
        user = c.fetchall()
        (name, id, gsp, mmr, winrate) = user[0]
        gsp = int(gsp)
        if gsp < lowest_high:
            usr = await client.get_user_info(lowest_queue[len(lowest_queue)-1])
            await client.send_message(message.channel, """{} has joined the __lowest__ queue. Players in the queue: **{}**.""".format(usr, len(mid_queue)))
            lowest_queue.append(id)
            print(lowest_queue)
            if len(lowest_queue) >= 2:
                (id, player1, player2, winner) = d.execute("SELECT TOP 1 * FROM `matches` ORDER BY id DESC LIMIT 1")[0]
                user1 = await client.get_user_info(lowest_queue[0])
                user2 = await client.get_user_info(lowest_queue[1])
                name = ""
                for i in range(0, 3):
                    name += alphabet[random.randint(0, len(alphabet)-1)]
                pas = ""
                for i in range(0, 3):
                    pas += alphabet[random.randint(0, len(alphabet)-1)]
                await client.send_message(user1, """
                Your match is against `{}`!
                You are __creating__ the match.
                The match name is `{}`
                The match password is `{}`

                When reporting, use: `!report {} win/loss`
                Ony 1 player needs to report.
                """.format(user2.name, name, pas))  
                await client.send_message(user2, """
                Your match is against `{}`!
                You are __joining__ the match.
                The match name is `{}`
                The match password is `{}`

                When reporting, use: `!report {} win/loss`
                Ony 1 player needs to report.
                """.format(user1.name, name, pas))   
                x = "INSERT INTO `matches` VALUES ('{}', '{}', '{}')".format(user1.id, user2.id, "none")
                d.execute(x)
                d.commit() 
        else:
            if gsp < low_high:
                low_queue.append(user)
                usr = await client.get_user_info(low_queue[len(low_queue)-1])
                await client.send_message(message.channel, """{} has joined the __low__ queue. Players in the queue: **{}**.""".format(usr, len(low_queue)))
                if len(low_queue) == 2:
                    (id, player1, player2, winner) = d.execute("SELECT TOP 1 * FROM `matches` ORDER BY id DESC LIMIT 1")[0]
                    user1 = await client.get_user_info(low_queue[0])
                    user2 = await client.get_user_info(low_queue[1])
                    name = ""
                    for i in range(0, 3):
                        name += alphabet[random.randint(0, len(alphabet)-1)]
                    pas = ""
                    for i in range(0, 3):
                        pas += alphabet[random.randint(0, len(alphabet)-1)]
                    await client.send_message(user1, """
                    Your match is against `{}`!
                    You are __creating__ the match.
                    The match name is `{}`
                    The match password is `{}`

                    When reporting, use: `!report {} win/loss`
                        Ony 1 player needs to report.
                    """.format(user2.name, name, pas))  
                    await client.send_message(user2, """
                    Your match is against `{}`!
                    You are __joining__ the match.
                    The match name is `{}`
                    The match password is `{}`

                    When reporting, use: `!report {} win/loss`
                        Ony 1 player needs to report.
                    """.format(user1.name, name, pas)) 
                    x = "INSERT INTO `matches` VALUES ('{}', '{}', '{}')".format(user1.id, user2.id, "none")
                    d.execute(x)
                    d.commit()
            else:
                if gsp < mid_high:
                    mid_queue.append(user)
                    usr = await client.get_user_info(mid_queue[len(mid_queue)-1])
                    await client.send_message(message.channel, """{} has joined the __mid__ queue. Players in the queue: **{}**.""".format(usr.name, len(mid_queue)))
                    if len(mid_queue) == 2:
                        (id, player1, player2, winner) = d.execute("SELECT TOP 1 * FROM `matches` ORDER BY id DESC LIMIT 1")[0]
                        user1 = await client.get_user_info(mid_queue[0])
                        user2 = await client.get_user_info(mid_queue[1])
                        name = ""
                        for i in range(0, 3):
                            name += alphabet[random.randint(0, len(alphabet)-1)]
                        pas = ""
                        for i in range(0, 3):
                            pas += alphabet[random.randint(0, len(alphabet)-1)]
                        await client.send_message(user1, """
                        Your match is against `{}`!
                        You are __creating__ the match.
                        The match name is `{}`
                        The match password is `{}`

                        When reporting, use: `!report {} win/loss`
                        Ony 1 player needs to report.
                        """.format(user2.name, name, pas, (id+1))) 
                        await client.send_message(user2, """
                        Your match is against `{}`!
                        You are __joining__ the match.
                        The match name is `{}`
                        The match password is `{}`

                        When reporting, use: `!report {} win/loss`
                        Ony 1 player needs to report.
                        """.format(user1.name, name, pas, (id+1)))
                        x = "INSERT INTO `matches` VALUES ('{}', '{}', '{}')".format(user1.id, user2.id, "none")
                        d.execute(x)
                        d.commit()
                else:
                    if gsp < top_high:
                        top_queue.append(user)
                        usr = await client.get_user_info(top_queue[len(top_queue)-1])
                        await client.send_message(message.channel, """{} has joined the __top__ queue. Players in the queue: **{}**.""".format(usr, len(mid_queue)))
                        if len(top_queue) == 2:
                            (id, player1, player2, winner) = d.execute("SELECT TOP 1 * FROM `matches` ORDER BY id DESC LIMIT 1")[0]
                            user1 = await client.get_user_info(top_queue[0])
                            user2 = await client.get_user_info(top_queue[1])
                            name = ""
                            for i in range(0, 3):
                                name += alphabet[random.randint(0, len(alphabet)-1)]
                            pas = ""
                            for i in range(0, 3):
                                pas += alphabet[random.randint(0, len(alphabet)-1)]
                            await client.send_message(user1, """
                            Your match is against `{}`!
                            You are __creating__ the match.
                            The match name is `{}`
                            The match password is `{}`

                            When reporting, use: `!report {} win/loss`
                            Ony 1 player needs to report.
                            """.format(user2.name, name, pas, (id+1)))  
                            await client.send_message(user2, """
                            Your match is against `{}`!
                            You are __joining__ the match.
                            The match name is `{}`
                            The match password is `{}`

                            When reporting, use: `!report {} win/loss`
                            Ony 1 player needs to report.
                            """.format(user1.name, name, pas, (id+1))) 
                            x = "INSERT INTO `matches` VALUES ('{}', '{}', '{}')".format(user1.id, user2.id, "none")
                            d.execute(x)
                            d.commit()
    if command == "report":
        matchid = int(args[0])
        winloss = args[1]
        id = message.author.id
        x = "SELECT * FROM `matches` WHERE id = '{}'".format(matchid)
        (id, player1, player2, winner) = d.execute(x)[0]
        y = "SELECT * FROM `players` WHERE id = '{}'".format(id)
        (name, id, sap, mmr, winrate) = c.execute(y)[0]
        if name == player1 or name == player2:
            if winloss == "w" or winloss == "win":
                x = "UPDATE `matches` SET winner='{}' WHERE id='{}'".format(name, matchid) 
                d.execute(x)
                d.commit()
            elif winloss == "l" or winloss == "loss":
                await client.send_message(message.author, "Only the winner can report matches.")
           

client.run(TOKEN)