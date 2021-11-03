import React, {useEffect, useState} from 'react';
import {
  initiateSocketConnection,
  disconnectSocket,
  stopSending,
  startSending,
  getSocket
} from "./services/socketio";


function App() {
  const [socketStatus, setSocketStatus] = useState("On");
  const [socketData, setSocketData] = useState("");

  useEffect(() => {
    initiateSocketConnection();
    const socket = getSocket();
    socket.on(
        "responseMessage",
        (message) => {
          console.log("responseMessage ", message)
          setSocketData(message.data)
        })


    return () => {
      disconnectSocket();
    }
  }, []);

  const handleEmit = () => {
    if(socketStatus==="On"){
      stopSending();
      setSocketStatus("Off")
    } else{
      startSending();
      setSocketStatus("On")
    }
    console.log("Emit Clicked")
  }

  return (
    <React.Fragment>
        <div>Data: {socketData}</div>
        <div>Status: {socketStatus}</div>
        <button onClick={handleEmit}> Start/Stop</button>
    </React.Fragment>
  )

}

export default App;
