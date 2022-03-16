import { SOCKET_URL } from './constants';
import { createContext } from "react";
import socketIOClient from 'socket.io-client';

export const socket = socketIOClient(SOCKET_URL, {
    transports: ['websocket', 'polling', 'flashsocket']
});
export const SocketContext = createContext(socket);