import telebot
import pickle

admins = [640632571, 156707897, 854784936]
users = []

reg_err = "Mi di spiace non sei un membro della gilda ghe ghe ghe\n Prova ad usere /register"
not_adm = "Mi dispiace ma accetto ordini solo da Bridge, Thalar e Aiden, Ghe Ghe"
group_id = -793240876

xpnextlvl = [0, 0, 0, 0, 0, 7500, 15000, 17800, 20000, 24500]

telebot.apihelper.SESSION_TIME_TO_LIVE = 60 * 5
token = open("token.txt", "r").readline()
bot = telebot.TeleBot(token, False)

class User:
    def __init__(self, nome, id, level):
        self.nome = nome
        self.id = id
        self.level = level
        self.xp = 0
    
    def can_level(self):
        if(self.xp >= xpnextlvl[self.level]):
            return True

    def addXp(self, n):
        if(n < 0):
            return
        self.xp += n
        return self.can_level()

    def levelup(self):
        if(self.can_level()):
            self.xp -= xpnextlvl[self.level]
            self.level += 1
    
    def __str__(self) -> str:
        s = "{0} {1} {2}".format(self.nome, self.xp, self.level)
        return s
    
def write_users():
    f = open("users","wb")
    pickle.dump(users, f)
    f.close()

def extract_arg(arg):
    command_length = len(arg.split()[0])
    if len(arg) == command_length:
        raise Exception()
    return arg[command_length+1:]

def get_user(user_id):
    for u in users:
        if(u.id == user_id):
            return u
    return None

def isAdmin(user_id):
    for id in admins:
        if user_id == id:
            return True
    return False

@bot.message_handler(commands=["xp","px"])
def myxp(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        bot.reply_to(message, "Tu sei un master, non hai px")
        return
    user = get_user(message.from_user.id)
    if(user == None):
        bot.reply_to(message, reg_err)
        return
    if(user.can_level()):
        bot.reply_to(message, "Adesso hai {0} px e puoi livellare, ghe ghe".format(user.xp))
    else:
        bot.reply_to(message, "Adesso hai {0} px, ghe ghe".format(user.xp))
    


@bot.message_handler(commands=["giveall"])
def giveall(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        try:
            numXp = int(extract_arg(message.text))
            for u in users:
                if u.addXp(numXp):
                    bot.reply_to(message, u.nome+ " ha livellato, ora è migliore ma non quanto un Goblin!")
            write_users()    
        except Exception:
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)


@bot.message_handler(commands=["saytogroup"])
def say(message):
    print(message.text)
    if isAdmin(message.from_user.id):
        try:
            to_say = extract_arg(message.text)
            bot.send_message(group_id, to_say)
        except Exception:
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)


@bot.message_handler(commands=["levelup"])
def levelup(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        bot.reply_to(message, "Tu sei un master, non hai px")
        return
    user = get_user(message.from_user.id)
    if(user == None):
        bot.reply_to(message, reg_err)
        return
    if(not user.can_level()):
        bot.reply_to(message, "Hai provasto a fregarmi! Tu non puoi livellare!")
        return
    user.levelup()
    write_users()

@bot.message_handler(commands=["users"])
def printusers(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        text = ""
        for u in users:
            text += str(u) + "\n"
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, not_adm)


@bot.message_handler(commands=["give", "givepx", "givexp"])
def give(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        try:
            numXp = int(extract_arg(message.text).split()[1])
            name = extract_arg(message.text).split()[0]
            for user in users:
                if user.nome == name:
                    user.addXp(numXp)
                    write_users()
                    if(user.can_level()):
                        bot.reply_to(message, "Fatto, ghe... Ah ma può livellare!")
                    else:
                        bot.reply_to(message, "Fatto, ghe")
                    return
            bot.reply_to(message, "Non so di chi parli, ghe")
        except Exception as e:
            print(e)
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)

@bot.message_handler(commands=["register"])
def register(message):
    print(message.text)
    id = message.from_user.id
    if (get_user(id) != None):
        bot.reply_to(message, "Idiota, ti conosco! Non sono ancora un goblin scemo!")
    try:
        name = extract_arg(message.text).split()[0]
        lvl = int(extract_arg(message.text).split()[1]) 
        users.append(User(name, id, lvl))
        write_users()
        bot.reply_to(message, "Perfetto, ora mi ricorderò di te, ghe ghe ghe")
    except Exception as e:
            print(e)
            bot.reply_to(message, "Devi anche dirmi come ti mi e il tuo attuale livello, ghe (es: /register Giacco 3)")

@bot.message_handler(commands=["delete"])
def deluser(message):
    print(message.text)
    u = get_user(message.from_user.id)
    if u != None:
        try:
            response = extract_arg(message.text)
            if response == "YES":
                users.remove(u)
                write_users()
                bot.reply_to(message, "Operazione completata... Chi cazzo sei?")
        except:
            bot.reply_to(message, "ATTENZIONE, stai elminando il tuo profilo e i tuoi px\n se sei sicuro ripeti il comando con l'aggiunta di YES in questo modo.\n /delete YES")            
    else:
        bot.reply_to(message, "Mi dispiace, non ho la minima idea di chi tu sia, ghe ghe!")


@bot.message_handler(commands=["pxu"])
def pxu(message):
    print(message.text)
    if(isAdmin(message.from_user.id)):
        try:
            name = extract_arg(message.text)
            for user in users:
                if user.nome == name:
                    bot.reply_to(message, str(user))
                    return
            bot.reply_to(message, "Mi dispiace, non ho la minima idea di chi tu sia, ghe ghe!")
        except Exception as e:
            print(e)
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)

#caricamento utenti
try:
    f = open("users","rb")
    users = pickle.load(f)
    f.close()
except:
    users = []

while True:
    try:
        bot.delete_webhook()
        bot.send_message(group_id, "Sono di nuovo Up bastardi!")
        bot.polling(none_stop=True)
        print("bot reboot")
    except Exception as e:
        bot.send_message(640632571, "Sono crashato con errore:\n" + str(e))
        print(e)