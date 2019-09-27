from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/api/v1/capture/getImages", methods=['POST'])
def getImages():
    jsonRequest = request.json

    url = jsonRequest["url"]
    responseEncodingType = jsonRequest["responseEncodingType"]
    language = jsonRequest["language"]
    isNoSub = jsonRequest["isNoSub"]
    numberToCapture = jsonRequest["numberToCapture"]
    startTimeStamp = jsonRequest["startTimeStamp"]
    endTimeStamp = jsonRequest["endTimeStamp"]

    # TODO Add core logic to capture

    return ""

if __name__ == '__main__':
    app.run()