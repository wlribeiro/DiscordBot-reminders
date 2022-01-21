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
        "-help": "see_help()"
        }
    
    count_commands = 0
    for key in list(command_list.keys()):
        if key in message:
            command = key
            count_commands += 1
    
    if count_commands > 1:
        return see_help()
    else:
        return locals()[command_list[command]]()


def add_question():
    question = ""
    date = ""

def list_all_questions():
    id_ = 0
    creator = ""
    editors = []
    question = ""
    date = ""
    return {"id": id_, "creator": creator, "question": question, "date": date}

def see_help():
    return """
Olá, esta é a seção de comandos, voce pode usar os comandos abaixo para realizar as tarefas

-list lista todas as questions

-add adiciona uma nova question (é obrigatorio definir um atributo da família -d)
    $ask -add <question> -d <date>
    $ask -add isso é uma questão? -d 30/01/2025

    -d adciona uma data para a questão, e a questão não irá se repetir
    -dw aciona uma data e vai repetir a questão toda semana, a partir da data escolhida
    -dm aciona uma data e vai repetir a questão todo mês, a partir da data escolhida
    -dy aciona uma data e vai repetir a questão todo ano, a partir da data escolhida

-edit edita uma question
    $ask -e <question_id>

-see exibe as informações sobre uma question
    $ask -see <question_id>

-help exibe painel de ajuda
    """

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
