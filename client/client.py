import requests
import json

#simple client just opens the file linked from the host computer with the input and each test is sent to the server

try:
    data = []
    with open("/input.json", "r") as f:
        data = json.load(f)
        for x in data:
            responce = requests.post("http://127.0.0.1:5000/calculate", data=json.dumps(x))
            print(responce.text)
except json.JSONDecodeError:
    print("Wrong format of the input file")
except IOError:
    print("Input file wasn't created")

print("Client script finished")