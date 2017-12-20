import urllib.request
globalVar = 0
array = ["client1", "client2"]

def main():
    iterateArray(array)
    
def iterateArray(arr):
    string = "hello"
    for item in arr:
        string += (str(item) + ",")
    print(string)

if __name__ == "__main__":
    main()