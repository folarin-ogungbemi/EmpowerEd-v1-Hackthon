import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
// @ts-ignore
import { ConversationModel } from "../models/Conversation.ts";
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';


export default function Conversations() {
  const [conversations, setActiveConversations] = useState<ConversationModel[]>([]);
  const [isError, setIsError] = useState("");
  const id = JSON.parse(document.getElementById('id')!.textContent!);

  useEffect(() => {
    async function fetchConversations() {
      try {
        const res = await fetch('/api/conversations/');
        if (res.status === 200) {
          setActiveConversations(await res.json());
          setIsError('');
        } else {
          throw new Error('Unexpected response from the server.');
        }
      } catch (error) {
        setIsError('Server error, please try again later.');
      }
    }
    fetchConversations();
  });

  function createConversationName(user_id: string) {
    const sorted = [id, user_id].sort();
    return `conv${sorted[0]}_${sorted[1]}`;
  }

  function formatMessageTimestamp(timestamp?: string) {
    if (!timestamp) return;
    const date = new Date(timestamp);
    return date.toLocaleTimeString().slice(0, 5);
  }

  return (
    <div>
      <Card>
      <Card.Header
      style={{
        fontSize: "21px",
        background: "#499ef5",
        color: "#f8fbfe"
    }}
      className="px-4">
          Your Chats
      </Card.Header>
      <ListGroup variant="flush">
      {conversations.map((c) => (
          <ListGroup.Item action
          className="py-0"
          key={createConversationName(c.other_user.pk)}>
        <Link 
          to={`/chat/${createConversationName(c.other_user.pk)}`}
          
        >
          <div className="px-3">
            <div
            className="d-flex"
            style={{
              flexDirection: 'row',
              justifyContent: 'space-between'
            }}
            >
            <Card.Title>{c.other_user.first_name} {c.other_user.last_name}</Card.Title>
            <p className="text-muted align-self-end mb-0">{formatMessageTimestamp(c.last_message?.timestamp)}</p>
            </div>
            <p className="text-muted">{c.last_message?.text}</p>
            </div>
        </Link>
      </ListGroup.Item>
      ))}
       </ListGroup>
      </Card>
    </div>
  );
}