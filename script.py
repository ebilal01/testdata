from pyscript import display
from pyodide.http import pyfetch
import asyncio
import struct

async def send_rockblock_data():
    imei = "300434065264590"
    url = "https://tufts-anemometer2.onrender.com/rockblock"  # Replace with actual URL

    test_values = [
        1700000000, 5, 42.3601, -71.0589, 100, 101325, 25, 30, 28,
        10, -5, 45, 2.5, 3.2, 4.1, 0.15, 0.20, 0.10, 0.50, 0.75, 1.00
    ]

    byte_data = struct.pack('IhffHhhhhhhhhhhhhhhhh', *test_values)
    hex_data = byte_data.hex()

    params = f"?imei={imei}&data={hex_data}"

    try:
        response = await pyfetch(url + params, method="POST")
        result = await response.text()
        display(result, target="output")
    except Exception as e:
        display(f"Error: {e}", target="output")
