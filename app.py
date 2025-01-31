from flask import Flask, render_template, request, jsonify
import struct
import datetime
import logging

app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rockblock', methods=['POST'])
def handle_rockblock():
    try:
        imei = request.form.get('imei')
        data = request.form.get('data')

        logging.debug(f"Received request: IMEI={imei}, Data={data}")

        if imei != "300434065264590":
            logging.warning("Invalid IMEI received.")
            return jsonify({"status": "FAILED", "code": 10, "message": "Invalid IMEI"}), 400

        if not data:
            logging.warning("No data provided.")
            return jsonify({"status": "FAILED", "code": 16, "message": "No data provided"}), 400

        # Convert the data to byte format
        if all(c in '0123456789abcdefABCDEF' for c in data) and len(data) % 2 == 0:
            byte_data = bytearray.fromhex(data)
            logging.debug(f"Byte data received: {byte_data}")

            if len(byte_data) == 50:  # Expected message length
                unpacked_data = struct.unpack('IhffHhhhhhhhhhhhhhhhh', byte_data)
                logging.debug(f"Unpacked Data: {unpacked_data}")
            else:
                logging.warning(f"Unexpected message length: {len(byte_data)} bytes")
                return jsonify({"status": "FAILED", "code": 17, "message": "Invalid message length"}), 400

        logging.info("Message received successfully.")
        return jsonify({"status": "OK", "message": "Message received successfully"}), 200

    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return jsonify({"status": "FAILED", "code": 15, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


