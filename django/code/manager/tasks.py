from celery.decorators import task
from datetime import datetime
from manager import models as ManagerModels
import asyncio
import websockets
import json
import os, time
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def generate_schedule_datetime(schedule_date, schedule_time):
    # Assuming schedule_date and schedule_time are in the format "YYYY-MM-DD" and "HH:MM" respectively
    date_format = "%Y-%m-%d %H:%M"
    schedule_datetime_str = f"{schedule_date} {schedule_time}"
    schedule_datetime = datetime.strptime(schedule_datetime_str, date_format)
    return schedule_datetime

async def send_json_data(host, port, username, msg_data):
    uri = f"ws://{host}:{port}"

    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to Node.js socket server at {uri}")

            data_to_send = {"type": "connect user", "username": username}
            json_data = json.dumps(data_to_send)
            await websocket.send(json_data)

            while True:
                response = await websocket.recv()
                # print("Server response:", response)
                json_response = json.loads(response)

                if json_response.get("type") == "account connected":
                    data_to_send = {"type": "send message", "data": msg_data, "username": username}
                    json_data = json.dumps(data_to_send)
                    await websocket.send(json_data)
                    break
                else:
                    time.sleep(3)

                    

    except websockets.exceptions.ConnectionClosedError:
        print("Connection to server closed.")
    except Exception as e:
        print(f"An error occurred while connecting: {e}")

@task
def send_scheduled_message():
    logger.info("We are here")
    try:
        due_tasks = ManagerModels.Task.objects.filter(schedule_date__lte = datetime.now(), sent=False)
        logger.info(due_tasks)
        for task in due_tasks:
            asyncio.get_event_loop().run_until_complete(send_json_data(os.environ.get("NODE_SOCKET_HOST"), 3030, task.user.username, task.data))
            task.sent = True
            task.save()
            # task.delete()
    except Exception as err:
        print(err)