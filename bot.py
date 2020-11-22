import discord
from discord.ext import commands
import pandas as pd

# Client (our bot)
client = commands.Bot(command_prefix='!buddy ')

# Help command


@client.command(pass_context=True)
async def h(context):
    """
    Gives advanced Description of various commands
    """

    myEmbed = discord.Embed(title="*BotBuddy* - Not a Dating Bot!",
                            description="*I am a simple bot that helps you connect with prospective friends to hang out with on the server.", color=0x00ff00)
    myEmbed.set_thumbnail(
        url="https://imgur.com/a/TxgknJ6")
    myEmbed.add_field(name="Find buddies", value="```!buddy find <name> <activity> <Description>```This command adds you to the buddy list and fetches a list of people with similar interests to your inbox.", inline=False
                      )
    myEmbed.add_field(name="Delete your request", value="```!buddy delete```This command deletes your entry if you no longer want to share your information.", inline=False
                      )
    myEmbed.add_field(name="Commend a User", value="```!buddy commend <Discord_ID#xxxx>```This command deletes your entry if you no longer want to share your information.", inline=False
                      )
    await context.channel.send(embed=myEmbed)


# find "{name-0} {activity-1} {Description-2}"
@client.command(name='find')
async def find(context, *, message):
    """
    Adds you to the database and sends a DM with friends with same interests - Use !buddy h for more info and proper syntax
    """

    author_id = context.message.author
    temp = message
    arr = temp.split()
    if(len(arr) != 3):
        await context.message.channel.send("Please enter the information in the correct format")
        return
    print(message)  # Troubleshooting
    print(arr)  # Troubleshooting
    name = arr[0]
    des = arr[2]
    activity = arr[1].lower()
    # Checking for correct format of blood group
    valid_activities = {"csgo", "valorant", "among us",
                        "karaoke", "fortnite", "music jam", "reading", "hackathon", "netflix", "science", "others"}
    if(activity in valid_activities):
        file = discord.File("./assets/csgo.png", filename="image.png")
        myEmbed = discord.Embed(title=name, color=0x00ff00)
        myEmbed.set_thumbnail(url="attachment://image.png")
        myEmbed.add_field(name="Description", value=des)
        myEmbed.add_field(name="Activity", value=activity)
        myEmbed.set_footer(text='has been added to our database.')
        await context.message.channel.send(file=file, embed=myEmbed)

        # Checking for compatible users in friends.csv
        df = pd.read_csv('./friends.csv', index_col=0)
        booleans = []
        for bg in df.activity:
            if (bg == activity):
                booleans.append(True)
            else:
                booleans.append(False)
        df1 = df[booleans]
        comp = df1.values.tolist()

        # Adding the interested recipient in the friends.csv file
        df = pd.read_csv('./friends.csv', index_col=0)
        df = df.append({"user_id": (author_id), "name": (name), "description":
                        (des), "activity": (activity)}, ignore_index=True)
        df.to_csv('./friends.csv')

        # Sending an embed with the required data as a DM to the author
        if(comp):
            embed1 = discord.Embed(
                title='These people can be your friends', thumbnail="./logo.png")
            for i in range(len(comp)):
                embed1.add_field(
                    name=f'Name: {comp[i][1]}', value=f'> Discord ID: {comp[i][0]}\n> Activity: {comp[i][2]}\n> Description: {comp[i][3]}', inline=False)
            await context.message.author.send(embed=embed1)
            await context.message.author.send("Drop them a DM to ask if they can wanna hang out with you!")
        else:
            await context.message.author.send("There is currently no one with similar interests in the server. Check back later.")
    else:
        await context.message.channel.send("Please enter the information in the correct format, you can use the following activities for now:")
        myEmbed = discord.Embed(title="Activities", color=0x00ff00)
        myEmbed.add_field(name="Counter Strike", value="```csgo```")
        myEmbed.add_field(name="Valorant", value="```valorant```")
        myEmbed.add_field(name="Among Us", value="```among us```")
        myEmbed.add_field(name="Karaoke", value="```karaoke```")
        myEmbed.add_field(name="Fortnite", value="```fortnite```")
        myEmbed.add_field(name="Music Jam", value="```music jam```")
        myEmbed.add_field(name="Reading", value="```reading```")
        myEmbed.add_field(name="Participate in Hackathons",
                          value="```hackathon```")
        myEmbed.add_field(
            name="Watch/Discuss Netflix or other shows", value="```netflix```")
        myEmbed.add_field(name="Science Stuff", value="```science```")
        myEmbed.add_field(
            name="Others (Provide a proper description)", value="```others```")
        await context.message.channel.send(embed=myEmbed)


@client.command(name='delete')
async def delete(context, *, message):
    """
    Deletes all your entries in the database for a specific Activity
    """
    temp = message
    author = context.message.author
    df = pd.read_csv('./friends.csv', index_col=0)
    newdf = df[(df['activity'] != message) & (df['user_id'] != str(author))]
    newdf.to_csv('./friends.csv')
    await context.message.channel.send(f"All the entries made by "+str(author)+" of activity ```" + message+"``` have been deleted.")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('I can help you find buddies'))
    print('Bot is online')

    df2 = pd.DataFrame({"user_id": ['xxx#1234'], "name": ['Test', ], "activity": [
                       'act1'], "description": ['random info']})
    df2.to_csv('./friends.csv')

# Run the bot on server
client.run('Nzc0NjQ0MDYxOTYwOTI5Mjgx.X6axgA.LGjM5oaTN_F-NSlUAge-BykAFsU')


# https://imgur.com/a/9GCM9gQ valrant
# https://imgur.com/nlazGQ8 csgo
