import urllib.request
globalVar = 0
array = ["client1", "client2"]

def iterateArray():
    for item in array:
        print(str(item))

def main():
    clientsString = ""
    clientsArray = []
    port = 4000
    ip = "192.168.99.100"
    for i in array:
        clientsString += str(i) + ","
    clientsString = clientsString[:-2] + "hell"
    print(clientsString)

if __name__ == "__main__":
    main()