import React, {useState}  from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { Link, useParams } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { MessageModel } from "../models/Message";
// @ts-ignore 
import { Message } from "./Message.tsx";
import ListGroup from 'react-bootstrap/ListGroup';
import Card from 'react-bootstrap/Card';
import { UserModel } from '../models/User';


export default function Chat() {
    const [welcomeMessage, setWelcomeMessage] = useState("");
    const [messageHistory, setMessageHistory] = useState<any>([]);
    const [message, setMessage] = useState("");
    const { conversationName } = useParams();
      const [to_user, setToUser] = useState<UserModel>();
  
    const { readyState, sendJsonMessage } = useWebSocket(`wss://8000-okserm-empowered-qrw26zw6fk2.ws-eu87.gitpod.io/messages/chat/${conversationName}`, {
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
            setMessageHistory((prev: any) => prev.concat(data.message));
            break;
          default:
            console.error('Unknown message type!');
            break;
          case "last_50_messages":
            setMessageHistory(data.messages);
            setToUser(data.to_user)
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
  
    const handleSubmit = () => {
      sendJsonMessage({
        type: "chat_message",
        message,
      })
      setMessage("")
    }
  
    return (
      <div className="ms-2 me-2" >        
      <Card>
      <Card.Header
      style={{
        background: "#499ef5",
        color: "#f8fbfe"
    }}
      className="px-4">
        <Link to={"/"}>
        <i className='bx bxs-chevron-left bx-flip-vertical px-2 pb-1' style={{fontSize: "21px", color: "#f8fbfe"}} ></i>
        </Link>
          {to_user?.first_name} {to_user?.last_name}
      </Card.Header>
        <ListGroup>
          {messageHistory.map((message: MessageModel) => (
              <Message key={message.id} message={message} />
          ))}
        </ListGroup>
      </Card>
      <div className="d-flex">
        <Form.Control 
          style={{ 
            display: "inline-block"
         }}
          name="message" 
          placeholder="Message"
          onChange={handleChangeMessage}
          value={message}
          />
        <Button 
          variant="success" 
          className="mb-1"
          onClick={handleSubmit}>Send</Button>
        </div>
      </div>
    )
  };