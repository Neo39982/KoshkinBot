import config
import urllib.request
import  json
import  time
import _thread
from time import sleep

def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode())



def ban(sock, user):
    mess(sock, ".ban {}".format(user))



def timeout(sock, user, seconds = 500):
    mess(sock, ".timeout {}".format(user, seconds))



#req = request
#res = response
def fillOpList():
    while True:
            try:
                url = "http://tmi.twitch.tv/group/user/koshkin__dom/chatters"

                #req = urllib.request(url, headers={"accept": "*/*"})
                res = urllib.request.urlopen(url).read()
                res = res.decode('utf8')
                setNewNow= set ()

                config.oplist.clear()
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                        config.oplist[p] = "mod"
                        setNewNow.add(p)

                for p in data["chatters"]["global_mods"]:
                        config.oplist[p] = "global_mod"
                        setNewNow.add(p)
                for p in data["chatters"]["admins"]:
                        config.oplist[p] = "admin"
                        setNewNow.add(p)
                for p in data["chatters"]["staff"]:
                        config.oplist[p] = "staff"
                        setNewNow.add(p)
                for p in data["chatters"]["viewers"]:
                        config.oplist[p] = "viewers"
                        setNewNow.add(p)
                if (len(setNewNow-config.opSet)>0 and len(config.opSet)>1):
                    config.newSet |= setNewNow-config.opSet
                    config.status = True

                config.opSet |= setNewNow
                sleep(5)
            except:
                print("Bad")



def isOp(user):
    return user in config.oplist

def addOp(user):
    config.oplist.append(user)
def clearNew():
    config.status = False
    config.newSet = set()
