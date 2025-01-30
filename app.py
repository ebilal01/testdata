from flask import Flask, render_template, request, jsonify
import struct
import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rockblock', methods=['POST'])
def handle_rockblock():
    imei = request.args.get('imei')
    data = request.args.get('data')

    if imei != "300434065264590":
        return "FAILED,10,Invalid login credentials", 400

    if not data:
        return "FAILED,16,No data provided", 400

    try:
        byte_data = bytearray.fromhex(data)

        if len(byte_data) != 50:
            return "FAILED,17,Invalid message length", 400

        unpacked_data = struct.unpack('IhffHhhhhhhhhhhhhhhhh', byte_data)
        unpacked_data = list(unpacked_data)

        for x in range(5, 12):
            unpacked_data[x] /= 10
        for x in range(12, 15):
            unpacked_data[x] /= 1000
        for x in range(15, 21):
            unpacked_data[x] /= 100

        sent_time_utc = datetime.datetime.fromtimestamp(
            unpacked_data[0], datetime.UTC
        ).strftime('%Y-%m-%dT%H:%M:%SZ')

        message_data = {
            "received_time": datetime.datetime.utcnow().isoformat() + "Z",
            "sent_time": sent_time_utc,
            "unix_epoch": unpacked_data[0],
            "latitude": unpacked_data[2],
            "longitude": unpacked_data[3],
            "altitude": unpacked_data[4]
        }

        print("Received Data:", message_data)
        return jsonify(message_data)

    except Exception as e:
        return f"FAILED,15,Error processing message: {str(e)}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
