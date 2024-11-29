let responses = {};
let socket;

function sockconnect() {
    socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {
        console.log("Connected to the server.");
    };

    socket.onmessage = (event) => {
        responses.push(event.data)
    };

    socket.onclose = () => {
        console.log("Connection closed.");
    };

    socket.onerror = (error) => {
        console.error("Error: Something went wrong.", error);
    };
}

function sendMessage(command) {
    const message = JSON.stringify({ command });  // Wrap command in JSON
    socket.send(message);
    console.log(`You say: ${message}`);
}