import aiohttp
import asyncio
import json
import os

# Applies prepended print statement.
from finetune_worker.stream.tasks import run_task_by_name
from finetune_worker.stream.utils import *
from finetune_worker.stream.ws import open_websocket_connection, start_conversation_thread, shutdown_conversation_thread

HOST = os.environ.get("FINETUNE_HOST", "api.finetune.build")
WORKER_ID = os.environ.get("FINETUNE_WORKER_ID")
WORKER_TOKEN = os.environ.get("FINETUNE_WORKER_TOKEN")

async def respond_to_ping():
    url = f"https://{HOST}/v1/worker/{WORKER_ID}/pong/"
    headers = {
        "Authorization": f"Worker {WORKER_TOKEN}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(
                url, ssl=False, json={"worker_id": WORKER_ID}
            ) as resp:
                if resp.status != 200:
                    print(f"Failed to respond to ping. Status: {resp.status}")
        except Exception as e:
            print(f"Ping response error: {e}")


async def listen_for_events():
    url = f"https://{HOST}/v1/worker/{WORKER_ID}/sse/"
    headers = {"Authorization": f"Worker {WORKER_TOKEN}"}

    timeout = aiohttp.ClientTimeout(sock_read=None)  # Disable read timeout
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(url, ssl=False) as response:
            print(f"Connected as {WORKER_ID}, status: {response.status}")

            if response.status != 200:
                error_details = await response.text()
                print(f"Error details: {error_details}")
                response.raise_for_status()

            async for line in response.content:
                decoded = line.decode("utf-8").strip()
                if decoded.startswith("data:"):
                    message = decoded[5:].strip()
                    try:
                        data = json.loads(message)
                        if data.get("type") == "ping":
                            print(f"Ping received. Sending pong...")
                            await respond_to_ping()

                        elif data.get("type") == "tool":
                            tool_name = data.get("tool_name")
                            run_task_by_name(tool_name)
                            print(f"Tool request received. Sending confirmation...")

                        elif data.get("type") == "websocket_open":
                            print("Opening WebSocket connection...")
                            await open_websocket_connection()

                        elif data.get("type") == "open_conversation_websocket":
                            content = data["data"]["content"]
                            conversation_id = data["data"]["conversation_id"]
                            print("Opening WebSocket connection for conversation in a thread...")
                            start_conversation_thread(conversation_id, content)

                        # Not sure if necessary to be sent with SSE as this can
                        # be done inside websocket.
                        # Will keep around just in case.
                        elif data.get("type") == "close_conversation_websocket":
                            conversation_id = data["data"]["conversation_id"]
                            print("Closing WebSocket connection for conversation in a thread...")
                            shutdown_conversation_thread(conversation_id)

                        else:
                            print(f"Received message: {data}")
                    except json.JSONDecodeError:
                        print(f"Received non-JSON message: {message}")
                elif decoded.startswith(":"):
                    print(f"Heartbeat")


async def start_worker():
    retry_delay = 1  # Start with 1 second
    max_delay = 60  # Cap the backoff

    while True:
        try:
            await listen_for_events()
            print(f"Disconnected from event stream. Retrying in {retry_delay}s...")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

        await asyncio.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, max_delay)  # Exponential backoff


if __name__ == "__main__":
    asyncio.run(start_worker())
