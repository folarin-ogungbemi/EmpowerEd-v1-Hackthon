import React, {useState}  from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


export default function App() {
  const [welcomeMessage, setWelcomeMessage] = useState('');
  const [messageHistory, setMessageHistory] = useState<any>([]);
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");

  const { readyState, sendJsonMessage } = useWebSocket('wss://8000-okserm-empowered-qrw26zw6fk2.ws-eu87.gitpod.io', {
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
        case 'chat_message_echo':
          setMessageHistory((prev:any) => prev.concat(data));
          break;
        default:
          console.error('Unknown message type!');
          break;
      }
    }
  });

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  function handleChangeMessage(e: any) {
    setMessage(e.target.value)
  }

  function handleChangeName(e: any) {
    setName(e.target.value)
  }

  const handleSubmit = () => {
    sendJsonMessage({
      type: "chat_message",
      message,
      name
    })
    setName("")
    setMessage("")
  }

  return (
    <div>
      <span>The WebSocket is currently {connectionStatus}</span>
      <p>{welcomeMessage}</p>
     
      <Form.Control 
        style={{ width: '200px' }}
        name="name" 
        placeholder='Name'
        onChange={handleChangeName}
        value={name}
        className="ms-5 me-5 mb-2"
        />

      <Form.Control 
        style={{ width: '400px' }}
        name="message" 
        placeholder='Message'
        onChange={handleChangeMessage}
        value={message}
        className="ms-5 me-5 mb-2"/>
      <Button variant="success" className="ms-5 mb-2" onClick={handleSubmit}>Submit</Button>
      <hr />
      <ul>
        {messageHistory.map((message: any, idx: number) => (
          <div className="" key={idx}>
            {message.name}: {message.message}
          </div>
        ))}
      </ul>

    </div>
  )
};