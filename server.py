import asyncio
import websockets
import random
import json

# 3.8.0 is the version this is working on

answers = ["hi", "blue", "men", "toilet", "clock", "school"]
questions = [
    "What did the cow say to the moon? ___",
    "I live over there, near the ___",
    "What's for dinner? ___",
    "What's in the bush over there? ___"
]
users = ["user1", "coolgay", "sigma"]
scores = {"user1": 2, "coolgay": 5, "sigma": 1}
user_answers = {"user1": "hi", "coolgay": "men", "sigma": "toilet"}
status = 0
connected_clients = set()  # Set to hold connected clients

async def make_response(info):
    res = {"response": info}
    print(res)
    return json.dumps(res)  # Convert the response to JSON format

async def register_user(user):
    print(user)
    users.append(user)
    return await make_response(1)

async def get_users():
    return await make_response(users)

async def get_answers():
    return await make_response(answers)

async def get_question():
    question = questions[random.randint(0, len(questions) - 1)]
    return await make_response(question)

async def get_questions():
    return await make_response(user_answers)

async def select_answer(user, answer):
    user_answers.update({user: answer})
    return await make_response(1)

async def start_round():
    global status
    global ruler
    ruler = users[random.randint(0, len(users) - 1)]
    status = 1
    await send_all(await make_response({"status": 1}))
    return await make_response(status)

async def end_round():
    global status
    status = 2
    await send_all(await make_response({"status": 2}))
    return await make_response(status)

async def get_status():
    return await make_response(status)

async def send_all(message):
    """Send a message to all connected clients."""
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handle_cmd(command):
    cmd = command.get("command")
    if cmd == "get_answers":
        return await get_answers()
    elif cmd == "get_question":
        return await get_question()
    elif cmd in ["start_game", "start_round"]:
        return await start_round()
    elif cmd == "end_round":
        return await end_round()
    elif cmd == "get_status":
        return await get_status()
    elif cmd == "register_user":
        return await register_user(command.get("user"))
    elif cmd == "get_users":
        return await get_users()
    elif cmd == "select_answer":
         return await select_answer(command.get("user"), command.get("answer"))
    elif cmd == "get_questions":
         return await get_questions()
    else:
        return await make_response(f"Unknown command: {cmd}")

async def decode_json_message(message):
    """Decode a JSON message and return the command or an error response."""
    try:
        data = json.loads(message)
        return data  # Return the entire data object
    except json.JSONDecodeError:
        return await make_response("Invalid JSON format")

# Define a callback function to handle incoming WebSocket messages
async def handle_websocket(websocket, path):
    # Register the client connection
    connected_clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Decode the incoming JSON message
            cmd = await decode_json_message(message)

            response = await handle_cmd(cmd)

            # Send the response back to the client
            await websocket.send(response)
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        # Unregister the client connection
        connected_clients.remove(websocket)

if __name__ == "__main__":
    # Start the WebSocket server
    start_server = websockets.serve(handle_websocket, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started on ws://localhost:8765")
    asyncio.get_event_loop().run_forever()