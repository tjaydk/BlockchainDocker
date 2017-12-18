import urllib.request
globalVar = 0
array = []

def main():
    clientsString = ""
    clientsArray = []
    port = 4000
    ip = "192.168.99.100"
    for i in range(10):
        requestString = "http://" + ip + ":" + str(port+i) + "/list"
        
        print("Trying to fetch list on: " + requestString)
        try:
            clientsString = urllib.request.urlopen(requestString).read()
            print(clientsString)
            string = str(clientsString)
            array = string[2:-1].split(",")
            for e in array:
                print(e)
            if len(array) > len(clientsArray):
                print("Updating array")
                clientsArray = array
        except urllib.error.URLError as e:
            print(e.reason)

if __name__ == "__main__":
    main()