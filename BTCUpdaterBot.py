import requests
import json

token = '1278823227:AAGx7SKxPazqbQ-vAMKYus4eKY06JJpvONM'
base = "http://api.telegram.org/bot{}".format(token)

countries = ["USD", "EUR", "GBP"]
countriesFull = ["USD", "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "DKK", "EUR", "GBP", "HKD", "INR", "ISK", "JPY", "KRW", "NZD", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD"]
params = ["last", "symbol"]
IDToSend = []

updateId = None
message = None
newLink = ""


def insertInIDs(id):
    if(id in IDToSend):
        pass
    else:
        IDToSend.append(id)
        reply = "Done! You'll get updated every hour!"
        sendMessage(reply, id)


def stopUpdatingMe(idToPop):
    IDToSend.remove(idToPop)

    reply = "You will no longer get updated."
    sendMessage(reply, idToPop)


def tellMeAboutBTC(senderID):
    print("NOW IN TELLMEABOUTBTC")

    currentValue = ""
    currentSymbol = ""
    currentCountry = ""

    btcRawData = requests.get('https://blockchain.info/ticker')
    btcData = btcRawData.text
    btcData = json.loads(btcData)

    reply = ""

    for ctrs in countries:
        for words in params:
            currentSymbol = btcData["{}".format(ctrs)]["symbol"]
            print(currentSymbol)

            currentValue = btcData["{}".format(ctrs)]["last"]
            print(currentValue)

            rawReply = "{}: {}{}".format(ctrs, currentValue, currentSymbol)

        reply = "{}\n{}".format(reply, rawReply)
    sendMessage(reply, senderID)


def getUpdates(offset = None):
    print("NOW IN GETUPDATES")

    url = base + "/getUpdates?timeout=60"
    if offset:
        url = url + "&offset={}".format(offset + 1)
    r = requests.get(url)
    print(r.content)
    return json.loads(r.content)

def sendMessage(message, chatId):
    print("NOW IN SENDMESSAGE")

    url = base + "/sendMessage?chat_id={}&text={}".format(chatId, message)

    if message is not None:
        requests.get(url)

    print(url)


def start():
    reply = """
HI! I'll help you keeping track of BTC Price!
/tellMeAboutBTC -> I'll send you the current BTC value!
/keepMeUpdated -> I'll keep you updated sending you
messages every hour!
/stopUpdatingMe -> You won't get updated anymore.
            """

    sendMessage(reply, fromId)
    return 0


if __name__ == "__main__":
    while True:
        updates = getUpdates(offset=updateId)
        updates = updates["result"]

        if updates:
            for item in updates:
                updateId = item["update_id"]
                # try:
                #     message = item["message"]["text"]
                # except a as Exception:
                #     message = None

                message = item["message"]["text"]

                fromId = item["message"]["from"]["id"]

                print("Message: ", message)
                print("FromID: ", fromId)

                if message == "/start":
                    start()
                elif message == "/tellMeAboutBTC":
                    tellMeAboutBTC(fromId)
                elif message == "/keepMeUpdated":
                    insertInIDs(fromId)
                elif message == "/stopUpdatingMe":
                    stopUpdatingMe(fromId)
                else:
                    reply = "Sorry, that was not a valid command. Please try again."
                    sendMessage(reply, fromId)

        currentTime = requests.get('http://worldclockapi.com/api/json/utc/now')
        time = currentTime.text
        time = json.loads(time)
        time = time["currentDateTime"]
        time = time.split('T')
        time = time[1].split('Z')
        time = time[0]
        time = time[3:5]

        if time == "00":
            for id in IDToSend:
                tellMeAboutBTC(id)