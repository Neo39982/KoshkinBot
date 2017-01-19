import config
import  utils
import socket
import re
import time
import _thread as thread
from time import sleep
from collections import Counter
import game
def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    end_time = 0
    vote_dict={}
    vote_dict_all={}
    i = 0
    TIME_VOTE= 60
    #utils.mess(s, "Я твой любимый модер <3")
    def clear_vote():
        end_time = 0
        vote_dict = {}
        vote_dict_all = {}
        i = 0
    thread.start_new_thread(utils.fillOpList, ())
    thread.start_new_thread(game.game_start, ())
    while True:

        if (config.status == True):
            st =""
            for p in config.newSet:
                st+=p+','
            st=st[0:-1]
            utils.mess(s,"/me палит: {}".format(st))

            utils.clearNew()

        if(time.time()>end_time and end_time != 0):
            utils.mess(s, "Голосование оконченно!")
            c = Counter(vote_dict.values())
            sleep(1)
            st=""
            for v in c.keys():
                utils.mess(s," За {0} проголосовало - {1} человек.".format(v,str(c[v])))
                sleep(1)
            utils.mess(s, st)
            vote_dict = {}
            vote_dict_all = {}
            i=0
            end_time=0
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print(response)

           # if(not utils.isOp(username)):
                #utils.mess(s, "Привет, {}!".format(username))
                #utils.addOp(username)
            vote_list = message.strip().split('|')
            if (vote_list[0] == "!begin_vote" and len(vote_list)>3 and username=="nord_mann"):
                sleep(1)
                utils.mess(s,"Голосование: "+vote_list[1]+" Варианты:")
                sleep(1)
                for v in vote_list[2:len(vote_list)]:
                    i += 1
                    #st+=v+"[{}],    ".format(i)
                    vote_dict_all[str(i)]=v
                    utils.mess(s,v+"[{}]".format(i))
                    sleep(1)
                #st = st[0:-1]
                utils.mess(s, "Время на голосование "+str(TIME_VOTE)+" сек. Голосовать командой !vote")
                end_time = time.time()+TIME_VOTE
            if message.strip() == "!time":
                utils.mess(s, "it's currently: " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
            if message.strip() == "!messages" and utils.isOp(username):
                utils.mess(s, "Do something awesome!")
                sleep(1)
                utils.mess(s, "Go to youtube.com/koshkin__dom and click the subscribe button there!")
            vote_list = message.strip().split(' ')


            if (end_time!=0 and vote_list[0] == "!vote" and end_time!=0 and vote_list[1] in vote_dict_all.keys()):
                vote_dict[username]= vote_dict_all[vote_list[1]]
                utils.mess(s, username+" голосует - "+vote_dict_all[vote_list[1]])
        sleep(1)
if __name__ == "__main__":
    main()
