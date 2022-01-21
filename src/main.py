import os
import discord
import dotenv


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

def parse_message(message):
    command_list = {
        "-list": "list_all_questions",
        "-add": "add_question",
        "-help": "see_help",
        "-edit": ""
        }
    
    count_commands = 0
    for key in command_list:
        if key in message: 
            command_ = key
            count_commands += 1
    
    if count_commands > 1 or count_commands == 0:
        return see_help()
    else:
        message = message.split(command_)
        if(command_ == "-add"):
            validate_data(message)
        elif(command_ == "-list"):
            pass
        elif(command_ == "-edit"):
            validate_data(message)
        else:
            return see_help()

def check_if_date_is_valid(date):
    return date

def validate_data(message, id=None):
    message = message[1].split("-d")

    question = message[0]
    check_if_date_is_valid(message[1])

def add_question():
    question = ""
    date = ""

def list_all_questions():
    id_ = 0
    creator = ""
    question = ""
    date = ""
    return {"id": id_, "creator": creator, "question": question, "date": date}

def see_help():
    text = open(os.path.realpath("src/texts/help.txt"), "r").readlines()
    return "".join(text)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:4] == "$ask":
        response = parse_message(message.content)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

# don't delete this line bellow, it is responsible to do bot work 
client.run(TOKEN)
