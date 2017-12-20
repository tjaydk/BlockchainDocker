from flask import Flask
from requests_futures.sessions import FuturesSession
import docker
import urllib.request
import os
import socket

# Configuration
socket.setdefaulttimeout(1)

# Global variables
app = Flask(__name__)
client = docker.from_env()
onlineUsers = []
ip = ""

# Get the IP of the Docker Virtual Machine
def dockerIp():
    host_file_obj = open("host.txt", "r")
    host_ip = host_file_obj.readline()
    host_file_obj.close()
    return host_ip
    

# Ask network for userlist
# Range will be defined between port 4000 - 4010
def retrieveList():
    clientsArray = []
    clientsString = ""
    
    port = 4000
    ip = dockerIp()
    ownPort = int(socket.gethostname())
    
    for i in range(5):
        currentPort = port+i
        # Dont ask own port
        if currentPort == ownPort:
            continue
        requestString = "http://" + ip.rstrip('\n') + ":" + str(currentPort) + "/status"
        try:
            req = urllib.request.urlopen(requestString)
        except urllib.error.URLError as e:
            print(e.reason)
            continue
        except socket.timeout as err:
            continue
            
        clientsArray.append(currentPort)
    
    # Returns the list of clients and appends self to the list if not already there
    try:
        clientsArray.index(ownPort)
    except ValueError:
        clientsArray.append(ownPort)
        return clientsArray
    
    return clientsArray

    
# Is client online
@app.route("/status")
def status():
    return "yes!!"


@app.route("/")
def hello():
    ip = dockerIp()
    onlineUsers = retrieveList()
    
    onlineHtmlString = ""
    if len(onlineUsers) > 0:
        for u in onlineUsers:
            onlineHtmlString += "<li>"+str(u)+"</li>"
    else:
        onlineHtmlString = "<li>No users online</li>"

    html = "<h3>Blockchain client info</h3>" \
           "<b>Username:</b> {username}<br/>" \
           "<b>Host ip:</b> " + ip + "<br/>" \
           "<b>Clients online:</b>" \
           "<ul>" + onlineHtmlString + "</ul>"
           
    return html.format(name=os.getenv("NAME", "world"), username=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)