import React, {useState}  from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
// @ts-ignore
import Chat from "./components/Chat.tsx";
// @ts-ignore
import Conversations from "./components/Conversations.tsx";


export default function App() {
    return (
      <Router basename='/messages/'>
        <Routes>
          <Route path="" element={<Conversations />} />
          <Route path="chat/:conversationName" element={<Chat />} />
        </Routes>
      </Router>
    );
  };
