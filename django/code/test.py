import asyncio
import websockets
import json

async def send_json_data(host, port, data):
    uri = f"ws://{host}:{port}"

    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to Node.js socket server at {uri}")

            json_data = json.dumps(data)
            await websocket.send(json_data)

            response = await websocket.recv()
            print("Server response:", response)

    except websockets.exceptions.ConnectionClosedError:
        print("Connection to server closed.")
    except Exception as e:
        print(f"An error occurred while connecting: {e}")

if __name__ == "__main__":
    node_host = "127.0.0.1"  # Change this to the Node.js server host
    node_port = 3000  # Change this to the Node.js server port

    # Example data to send as JSON
    data_to_send = {"type": "connect user", "username": "admin"}

    asyncio.get_event_loop().run_until_complete(send_json_data(node_host, node_port, data_to_send))
