import React, {useState}  from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';


export default function App() {
  const [welcomeMessage, setWelcomeMessage] = useState('');
  const { readyState } = useWebSocket('wss://8000-okserm-empowered-qrw26zw6fk2.ws-eu87.gitpod.io', {
    onOpen: () => {
      console.log("Connected!")
    },
    onClose: () => {
      console.log("Disconnected!")
    },
    onMessage: (e) => {
      const data = JSON.parse(e.data)
      switch (data.type) {
        case 'welcome_message':
          setWelcomeMessage(data.message)
          break;
        default:
          console.error('Unknown message type!');
          break;
      }
    }
  });

  const { sendJsonMessage } = useWebSocket('wss://8000-okserm-empowered-qrw26zw6fk2.ws-eu87.gitpod.io')

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div>
      <span>The WebSocket is currently {connectionStatus}</span>
      <p>{welcomeMessage}</p>
      <button className='bg-gray-300 px-3 py-1' 
    onClick={() => {sendJsonMessage({
        type: "greeting",
        message: "Hi!"
      })
    }}>Say Hi</button>
    </div>
  );
};