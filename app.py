from flask import Flask
from requests_futures.sessions import FuturesSession
import docker
import urllib.request
import os
import socket


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
    ip
    ownPort = int(socket.gethostname())
    
    for i in range(2):
        currentPort = port+i
        # Dont ask own port
        if currentPort == ownPort:
            continue
        requestString = "http://" + ip.rstrip('\n') + ":" + str(currentPort) + "/list"
        try:
            req = urllib.request.urlopen(requestString)
            response = req.read()
            clientsString = str(response)
            # Takes a substring to remove the b' and the ' in beginning and end of response
            array = clientsString[2:-1].split(",")
            # Swaps the user list if the one recieved from the client is bigger
            if len(array) > len(clientsArray):
                clientsArray = array
        except urllib.error.URLError as e:
            print(e.reason)
    # Returns the list of clients and appends self to the list if not already there
    '''try:
        clientsArray.index(ownPort)
    except ValueError:
        clientsArray.append(ownPort)
        return clientsArray'''
    clientsArray.append(ownPort)
    
    return clientsArray

    
# Retrieve clients clientlist
@app.route("/list")
def list():
    userlistString = "<p>"
    for u in onlineUsers:
        userlistString += str(u)+","
    userlistString = userlistString[:-1] + "</p>"
    return userlistString
    
# Introduce client to list of clients
@app.route("/list/<username>")
def online(username):
    onlineUsers.append(username)
    return "<p>Welcome " + username + "</p>"


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

    html = "<h3>Hello {name}!</h3>" \
           "<b>Username:</b> {username}<br/>" \
           "<b>Host ip:</b> " + ip + "<br/>" \
           "<b>Clients online:</b>" \
           "<ul>" + onlineHtmlString + "/<ul>"
           
    return html.format(name=os.getenv("NAME", "world"), username=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)