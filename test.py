import urllib.request
globalVar = 0
array = []

def main():
    array.append(1)
    array.append(2)
    
    print(urllib.request.urlopen("http://www.google.com").read())

    if len(array) > 0:
        for i in array:
            print(i)
    else: 
        print("Or not")

if __name__ == "__main__":
    main()