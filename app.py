from flask import Flask
import urllib.request
import os
import socket

# Global variables
app = Flask(__name__)
onlineUsers = []

# Get the IP of the Docker Virtual Machine
def dockerIp():
    host_file_obj = open("host.txt", "r")
    host_ip = host_file_obj.readline()
    host_file_obj.close()
    return host_ip

# Ask network for userlist
# Range will be defined between port 4000 - 4010
def retrieveList():
    clientsString = ""
    clientsArray = []
    port = 4000
    ip = dockerIp()
    for i in range(10):
        clientsString = urllib.request.urlopen(ip + ":" + (port+i)).read()
        array = clients.split(",")
        if len(array) > len(clientsArray):
            clientsArray = array
    
    clientsArray.append(socket.gethostname)
    return clientsArray
    
# Retrieve clients clienlist
@app.route("/list")
def list():
    return onlineUsers
    
# Introduce client to list of clients
@app.route("/list/<username>")
def online(username):
    onlineUsers.append(username)
    
    return "<p>Welcome " + username + "</p>"


@app.route("/")
def hello():
    ip = dockerIp()
    #onlineUsers = retrieveList()
    
    onlineHtmlString = ""
    if len(onlineUsers) > 0:
        for u in onlineUsers:
            onlineHtmlString += "<li>"+u+"</li>"
    else:
        onlineHtmlString = "<li>No users online</li>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Username:</b> {username}<br/>" \
           "<b>Host ip:</b> " + ip + "<br/>" \
           "<b>Clients online:</b>" \
           "<ul>" + onlineHtmlString + "/<ul>" \
           
    return html.format(name=os.getenv("NAME", "world"), username=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)