import Alert from 'react-bootstrap/Alert';
import React, { createContext, ReactNode, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

const DefaultProps = {
  unreadMessageCount: 0,
  connectionStatus: "Uninstantiated",
  eachUser: [],
};

export interface NotificationProps {
  unreadMessageCount: number;
  connectionStatus: string;
  eachUser: Array<Array<number>>;
};

export const NotificationContext = createContext<NotificationProps>(DefaultProps);

export const NotificationContextProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [unreadMessageCount, setUnreadMessageCount] = useState(0);
  const [eachUser, setEachUser] = useState([] as any);
  const [isError, setIsError] = useState(false);

  const { readyState } = useWebSocket(
    `wss://team4-empowered.herokuapp.com/notifications/`,
    {
      onOpen: () => {
        console.log('Connected to Notifications!');
      },
      onClose: () => {
        console.log('Disconnected!');
        setIsError(true);
      },
      onError: () => {
        setIsError(true);
      },
      onMessage: (e) => {
        const data = JSON.parse(e.data);
        switch (data.type) {
          default:
            console.error('Unknown message type!');
            break;
          case 'unread_count':
            setUnreadMessageCount(data.unread_count);
            setEachUser(data.each);
            break;
          case 'new_message_notification':
            setUnreadMessageCount((count) => (count += 1));
            let from_user = eachUser.find(
              (x: any) => x[0] == data.message.from_user.pk
            );
            if (from_user == undefined) {
              eachUser.push([data.message.from_user.pk, 1]);
            } else {
              eachUser.find(
                (x: any) => x[0] == data.message.from_user.pk
              )[1] += 1;
            }
            break;
        }
      },
    }
  );

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated"
  }[readyState];

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <NotificationContext.Provider
      value={{ unreadMessageCount, connectionStatus, eachUser }}>
      {children}
      {isError && (
        <Alert key="danger" variant="danger">
          There's been a problem connecting, can't display message
          notifications.{' '}
          <a href="#" className="link-dark" onClick={handleRefresh}>
            Try again.
          </a>
        </Alert>
      )}
    </NotificationContext.Provider>
  );
};