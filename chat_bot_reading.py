# Twitch Chat Bot - IRC - Reading Chat - 2018
# Dillon Cain (Twitch: dcain)
# Feel free to expand on it! =)
# This part will consist on reading chat
#######################################################################
# Info copied from (https://help.twitch.tv/customer/portal/articles/1302780-twitch-irc), (https://dev.twitch.tv/docs/irc/guide/)
#######################################################################
# Prerequisites:
# In order to connect to Twitch IRC, you must have the following information:
#
# - The name of channel that you want to join.
# - A Twitch account.
# - An OAuth token from API or from a site utilizing the API such as TwitchApps
# - (http://www.twitchapps.com/tmi/) - OAuth Token from link

import socket
# (socket) - Connects two nodes on a network to communicate.
# One listens on a port (6667 for us), while the other socket extends
# a hand out to achieve a connection. Server side the 'listener' socket waits
# while our 'client' side reaches out to it.
import threading
# (threading) - Used to run multiple threads (tasks and function calls) at the same time
# This comes in handy when taking input from chat

server_name = "irc.chat.twitch.tv"
# Server name to connect
port = 6667
# Port to connect
oauth_pass = "oauth:"
# Example: "oauth:asdasd234asd234ad234asds23"
bot_username = ""
# Account username that the chatbot uses to send messages.
# This can be your account or popular among many is creating a second account dedicated to being a chat bot.
channel_name = ""
# Twitch channel where you want your bot to join/run
message = ""
# Variable to hold messages passed in/out
#
#
# Socket instance
irc = socket.socket()
irc.connect((server_name, port))                        # Authentication with server
irc.send(("PASS " + oauth_pass + "\n"                   # Oauth token
          "NICK " + bot_username + "\n"                 # Bot username
          "JOIN #" + channel_name + "\n").encode())      # Specified channel being joined
print('Auth info sent')
# .encode() can be used individually but you can also group together ().
# I've seen "utf-8" passed inside of encode("") but the above works as well.

def twitch_irc():
    def join_chat():                                     # Confirms joining server and prints out server provided messages
        loading_process = True                                  # Twitch always has a fun response when joining =)
        while loading_process:
            read_buffer_join = irc.recv(1024)                # Receive data from socket
            read_buffer_join = read_buffer_join.decode()
            for line in read_buffer_join.split("\n")[0:-1]:  # One line read, printed out, and then new line started.... rinse and repeat.
                print(line)
                loading_process = loading_complete(line)
    def loading_complete(line):
        if ("End of /NAMES list" in line):                   # If this line is reached, bot has successfully joined
            print("Bot has joined " + channel_name + "'s Channel! Have fun! =)")
            return False
        else:
            return True

    def send_message(irc, message):
        message_temp = "PRIVMSG #" + channel_name + " :" + message  # (PRIVMSG #)" is used to signify messages being sent from someone
        irc.send((message_temp + "\n").encode())                    # Despite being called what they are, they are public to the chat channel

    def get_user(line):
        separate = line.split(":", 2)
        user = separate[1].split("!" , 1)[0]    # Extracts username from line by split()
        return user

    def get_message(line):
        global message
        try:
            message = (line.split(":", 2))[2]   # Extracts message by using split()
        except:
            message = ""                        # Catch
        return message

    def console(line):
        if "PRIVMSG" in line:                   # Looks for "PRIVMSG"
            return False
        else:
            return True

    join_chat()                                 # Call function join_chat()

    while True:
        try:
            read_buffer = irc.recv(1024).decode()                  # Receive data from socket
        except:
            read_buffer = ""
        for line in read_buffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and console(line):
                server_message = "PONG tmi.twitch.tv\r\n".encode() # Server sends "PING" every five minutes
                irc.send(server_message)                           # We reply with "PONG" to give a response
                print(server_message)                              # Print for feedback in console
                continue
            else:
                print(line)
                user = get_user(line)                              # Prints out line, user, and message
                message = get_message(line)
                print(user + " : " + message)


threading.Thread(target=twitch_irc).start() # A thread that starts twitch_irc

# I chose threading for efficiency plus researched the use of it and was fun to use, also allows for expansion.
# Threading tends to be used where a task involves some waiting, other code can be executed during the wait time.
# Another function for example can be threaded during that time.
# #################################################################
#
# If using multiple threads the below commented code is the process.
###################################################################
#if __name__ == '__main__':
#   thread_one = threading.Thread(target=twitch_irc).start()
#   thread_two = threading.Thread(target=).start()
#   thread_three = threading.Thread(target=).start()
