import discord
import sqlite3
import random

conn = sqlite3.connect("database.db")
c = conn.cursor()

TOKEN = ""
alphabet = "abcdefghijklmnopqrstuvwxyz"

client = discord.Client()

top_low, top_high = 4000000, 4999999
mid_low, mid_high = 3000000, 3999999
low_low, low_high = 2000000, 2999999
lowest_low, lowest_high = 1000000, 1999999

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
        c.execute("INSERT INTO users VALUES ({}, {}, {}, {}, {}".format(message.author.name, message.author.id, "", 0, 0.0))
        conn.commit()
        await client.send_message(message.author, """
        Below, use the following commands:
        `!username <name>` - no spaces or special characters. you can use this as many times as you want.
        `!gsp <number> - this determines your initial *Smash League* rank. if this changes at any point, come back and re-do this command. do not use commas in number
        """)
    if command == "username":
        c.execute("UPDATE users SET name='{}' WHERE id={}".format(args[0], message.author.id))
        conn.commit()
        await client.send_message(message.author, "Updated username to: `{}`".format(args[0]))
    if command == "gsp":
        c.execute("UPDATE users SET gsp='{}' WHERE id={}".format(args[0], message.author.id))
        conn.commit()
        await client.send_message(message.author, "Updated your GSP to: `{}`".format(args[0]))
    top_queue = []
    mid_queue = []
    low_queue = []
    lowest_queue = []
    if command == "q":
        c.execute("SELECT * FROM users WHERE id='{}'".format(message.author.id))
        user = c.fetchall()
        gsp = user.gsp
        if gsp < lowest_high:
            lowest_queue.append(user)
            if len(lowest_queue) == 2:
                user1 = client.get_user_info(lowest_queue[0])
                user2 = client.get_user_info(lowest_queue[1])
                name = ""
                for i in range(0, 3):
                    name += alphabet[random.randint(0, len(alphabet))]
                pas = ""
                for i in range(0, 3):
                    pas += alphabet[random.randint(0, len(alphabet))]
                client.send_message(user1, """
                Your match is against `{}`!
                You are __creating__ the match.
                The match name is `{}`
                The match password is `{}`
                """.format(user2.user.name, name, pas))  
                client.send_message(user2, """
                Your match is against `{}`!
                You are __joining__ the match.
                The match name is `{}`
                The match password is `{}`
                """.format(user1.user.name, name, pas))    
        else:
            if gsp < low_high:
                low_queue.append(user)
                if len(low_queue) == 2:
                    user1 = client.get_user_info(low_queue[0])
                    user2 = client.get_user_info(low_queue[1])
                    name = ""
                    for i in range(0, 3):
                        name += alphabet[random.randint(0, len(alphabet))]
                    pas = ""
                    for i in range(0, 3):
                        pas += alphabet[random.randint(0, len(alphabet))]
                    client.send_message(user1, """
                    Your match is against `{}`!
                    You are __creating__ the match.
                    The match name is `{}`
                    The match password is `{}`
                    """.format(user2.user.name, name, pas))  
                    client.send_message(user2, """
                    Your match is against `{}`!
                    You are __joining__ the match.
                    The match name is `{}`
                    The match password is `{}`
                    """.format(user1.user.name, name, pas)) 
            else:
                if gsp < mid_high:
                    mid_queue.append(user)
                    if len(mid_queue) == 2:
                        user1 = client.get_user_info(mid_queue[0])
                        user2 = client.get_user_info(mid_queue[1])
                        name = ""
                        for i in range(0, 3):
                            name += alphabet[random.randint(0, len(alphabet))]
                        pas = ""
                        for i in range(0, 3):
                            pas += alphabet[random.randint(0, len(alphabet))]
                        client.send_message(user1, """
                        Your match is against `{}`!
                        You are __creating__ the match.
                        The match name is `{}`
                        The match password is `{}`
                        """.format(user2.user.name, name, pas))  
                        client.send_message(user2, """
                        Your match is against `{}`!
                        You are __joining__ the match.
                        The match name is `{}`
                        The match password is `{}`
                        """.format(user1.user.name, name, pas)) 
                else:
                    if gsp < top_high:
                        top_queue.append(user)
                        if len(top_queue) == 2:
                            user1 = client.get_user_info(top_queue[0])
                            user2 = client.get_user_info(top_queue[1])
                            name = ""
                            for i in range(0, 3):
                                name += alphabet[random.randint(0, len(alphabet))]
                            pas = ""
                            for i in range(0, 3):
                                pas += alphabet[random.randint(0, len(alphabet))]
                            client.send_message(user1, """
                            Your match is against `{}`!
                            You are __creating__ the match.
                            The match name is `{}`
                            The match password is `{}`
                            """.format(user2.user.name, name, pas))  
                            client.send_message(user2, """
                            Your match is against `{}`!
                            You are __joining__ the match.
                            The match name is `{}`
                            The match password is `{}`
                            """.format(user1.user.name, name, pas)) 
        
           

client.run(TOKEN)