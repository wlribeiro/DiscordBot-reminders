import os
import discord
import dotenv
import sqlite3


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG = os.getenv("DEBUG")

client = discord.Client()

DB_NAME = "questions"
connection =  sqlite3.connect(f"{DB_NAME}.db")
cursor = connection.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {DB_NAME}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question VARCHAR,
    creator VARCHAR,
    date VARCHAR
)
""")

def parse_message(message):
    command_list = ["-list","-add","-help", "-edit"]
    
    count_commands = 0
    for key in command_list:
        if key in message: 
            command_ = key
            count_commands += 1
    
    if count_commands > 1 or count_commands == 0:
        return see_help()
    else:
        try:
            message = message.split(command_)
            if(command_ == "-add"):
                message = validate_data(message[1])
            elif(command_ == "-list"):
                message = list_all_questions()
            elif(command_ == "-edit"):
                message = validate_data(message)
            else:
                message = see_help()
        except Exception as error :
            print(error)
            if DEBUG : message = f"DEBUG: {error}"
            else: message = "Oops, o programador estava com muita preguiça de validar essa exeção, qualquer duvida é só olhar `$ask -help`"

        return message

def check_if_date_is_valid(date):
    return True

def validate_data(message, id=None):
    message = message.strip(" ")
    q = message.index("-q")
    if q == 0: # if -q is in init of string
        message = message.split("-q")[1] 
        message = message.split("-d")
        question = message[0].strip(" ")
        date = message[1]

    if check_if_date_is_valid(date):
        cursor.execute(f"""
        INSERT INTO {DB_NAME} (question, date) VALUES (?, ?)
        """, (question, date))
        connection.commit()
        return f"Sua quetion:\"{question}\" foi salva com suceso para o dia: {date}"
    else:
        return "Não foi possivel salvar sua question porque a data é invalida"

def add_question():
    question = ""
    date = ""

def list_all_questions():
    message = ""
    cursor.execute(f'SELECT * FROM {DB_NAME}')
    for line in cursor.fetchall():
        message += f"id: {line[0]}, question: {line[1]}, date: {line[3]} \n"
    
    return message

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
