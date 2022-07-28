import telebot

admins = [640632571, 156707897]
users = []

reg_err = "Mi di spiace non sei un membro della gilda ghe ghe ghe\n Prova ad usere /register"
not_adm = "Mi dispiace ma accetto ordini solo da Bridge, Thalar e Aiden, Ghe Ghe"
group_id = -793240876

xpnextlvl = [0, 0, 0, 0, 0, 7500, 15000, 17800, 20000, 24500]



token = open("token.txt", "r").readline()
bot = telebot.TeleBot(token, False)

class user:
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
    if(isAdmin(message.from_user.id)):
        bot.reply_to(message, "Tu sei un master, non hai px")
        return
    user = get_user(message.from_user.id)
    if(user == None):
        bot.reply_to(message, reg_err)
        return
    bot.reply_to(message, "Adesso hai {0} px, ghe ghe".format(user.xp))


@bot.message_handler(commands=["giveall"])
def giveall(message):
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


bot.message_handler(commands={"saytogroup"})
def say(message):
    if isAdmin(message.from_user.id):
        try:
            to_say = extract_arg(message.text)
            bot.send_message(group_id, to_say)
        except Exception:
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)


bot.message_handler(commands={"levelup"})
def levelup(message):
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


bot.message_handler(commands={"give", "givepx", "givexp"})
def give(message):
    if(isAdmin(message.from_user.id)):
        try:
            numXp = int(extract_arg(message.text).split[1])
            name = extract_arg(message.text).split[0]
            for user in users:
                if user.name == name:
                    user.addXp(numXp)
                    write_users()
                    return
            bot.reply_to(message, "Non so di chi parli, ghe")
        except Exception:
            bot.reply_to(message, "Comando errato, ghe")
    else:
        bot.reply_to(message, not_adm)

bot.message_handler(commands={"register"})
def register(message):
    id = message.from_user.id
    if (get_user(id) != None):
        bot.reply_to(message, "Idiota, ti conosco! Non sono ancora un goblin scemo!")
    try:
        name = extract_arg(message.text).split[0]
        lvl = int(extract_arg(message.text).split[1])
        users.append(User(name, id, level))
        write_users()
        bot.reply_to(message, "Perfetto, ora mi ricorderò di te, ghe ghe ghe")
    except Exception:
            bot.reply_to(message, "Comando errato, ghe")

@bot.message_handler(commands=["delete"])
def deluser(message):
    u = get_user(message.from_user.id)
    if u != None:
        try:
            response = extract_arg(message.text)
            if response == "YES":
                users.remove(u)
                write_users()
                bot.reply_to(message, "Operazione completata... Chi cazzo sei?")
            else:
                bot.reply_to(message, user_error)
                print(response)
        except:
            bot.reply_to(message, "ATTENZIONE, stai elminando il tuo profilo e i tuoi px\n se sei sicuro ripeti il comando con l'aggiunta di YES in questo modo.\n /deluser YES")            
    else:
        bot.reply_to(message, "Mi dispiace, non ho la minima idea di chi tu sia, ghe ghe!")




#caricamento utenti
try:
    f = open("users","rb")
    users = pickle.load(f)
    f.close()
except:
    users = []

while True:
    bot.delete_webhook()
    bot.polling(none_stop=True)
    print("bot reboot")