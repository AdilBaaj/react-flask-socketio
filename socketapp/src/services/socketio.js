import io from 'socket.io-client';

let socket;

export const getSocket = () => socket;

export const initiateSocketConnection = () => {
	console.log(`Connecting socket...`);
	socket = io.connect("http://localhost:5000", {
		reconnection: true,
		query: {token : 'secret2'},
	});
}

export const disconnectSocket = () => {
  console.log('Disconnecting socket...');
  if(socket) socket.disconnect();
}

export const stopSending = () => {
	socket.emit("message", {'data':'Stop Sending', 'status':'Off'})
}

export const startSending = () => {
	socket.emit("message", {'data':'Start Sending', 'status':'On'})
}
