import React from "react";
// @ts-ignore
import { MessageModel } from "../models/Message.ts";
import Alert from 'react-bootstrap/Alert';


export function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

export function Message({ message }: { message: MessageModel }) {
  const id = JSON.parse(document.getElementById('id')!.textContent!);

  function formatMessageTimestamp(timestamp: string) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString().slice(0, 5);
  }

  return (
      <Alert
        className={classNames(
        "mt-1 px-3 py-1 shadow",
        id === message.to_user.id ? "align-self-start" : "align-self-end"
      )}
        style={{ 
          width: 'fit-content',
          maxWidth: '400px',
          wordBreak: 'break-word'
      }}
        variant={
          id === message.to_user.id ? "warning" : "primary"
        }>
      
        <div>
          <span className="block">{message.text}&nbsp;&nbsp;</span>
          <span
            style={{
              fontSize: "0.6rem",
              lineHeight: "1rem"
            }}
          >
            {formatMessageTimestamp(message.timestamp)}
          </span>
        </div>
      </Alert>
  );
}