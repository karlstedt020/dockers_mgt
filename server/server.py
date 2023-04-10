from flask import Flask
from flask import request
import json

app = Flask(__name__)

#a simple flask server which receives on port 5000 data and processes it with the function process, returnes the answer by HttpResponse

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    data = json.loads(request.data)
    with open("input.json", "w") as inp:
        json.dump(data, inp)
    from asvk_KarlstedtAnton_206 import process
    ans = process()
    return ans

if __name__ == '__main__':
    app.run()