#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from WebSocket.websocket_server.websocket_server import WebsocketServer, Client
import json
from enum import Enum
from typing import NewType, Callable, Optional, Union

from WebSocket.Thread.thread import Thread

Callback = NewType(
    "Callback",
    Callable[[Client, object], Optional[Union[object, str, None]]]
)

DEFAULT_PORT = 80
DEFAULT_HOST = "127.0.0.1"


class States(Enum):
    created = 0
    listen = 1
    stopped = 2


class ErrorTypes(Enum):
    badRequest = 0
    unknownEvent = 1


class CallbacksWebSocketServer:
    callbacks = {}
    state = States.created
    _logger = None
    server = None
    mainThread = None
    callbackThreads = set()
    lastSentMessageIsError = False
    onConnectedCallback: Callable[[Client], None] = None
    onDisconnectedCallback: Callable[[Client], None] = None

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, eventFieldName: str = "event",
                 dataFieldName: str = "data", logLevel: int = logging.INFO):
        self._logger = logging
        self._logger.getLogger().setLevel(logLevel)
        self.eventName = eventFieldName
        self.dataName = dataFieldName
        self.host = host
        self.port = port

    def start(self, thread=True):
        self.state = States.listen
        self._logger.info(f"WebSocket server listening on {self.host}:{self.port}")
        self.server = WebsocketServer(host=self.host, port=self.port)
        self.server.set_fn_message_received(self.__message_received)
        self.server.set_fn_new_client(self.__client_connected)
        self.server.set_fn_client_left(self.__client_disconnected)
        if thread:
            self.mainThread = Thread(target=self.server.run_forever)
            self.mainThread.start()
            return
        self.server.run_forever()

    def waitThread(self):
        if self.mainThread is None:
            raise AssertionError("WS server isn't running in thread mode")
        try:
            self.mainThread.join()
        except KeyboardInterrupt:
            pass
        self.stop()

    def stop(self):
        self._logger.info("Server stopping...")
        self.state = States.stopped
        self.server.server_close()

    def setCallback(self, eventName: str, callback: Callback) -> None:
        if self.state != States.created:
            self._logger.warning(f"Server now in listen or stopped state and can't set any callbacks")
            return

        if eventName in self.callbacks:
            self._logger.warning(f"Callback on event \"{eventName}\" already exists!")

        self.callbacks[eventName] = callback

    def removeCallback(self, eventName: str) -> Callback:
        if eventName not in self.callbacks:
            self._logger.warning(f"Callback on event \"{eventName}\" not exists!")

        callback = self.callbacks[eventName]
        del self.callbacks[eventName]
        return callback

    def send(self, client: Client, data: object) -> bool:
        try:
            self.server.send_message(client, data)
            self._logger.debug(f"Sent message to {client.address}. Message: \n {data}")
            self.lastSentMessageIsError = False
            return True
        except BrokenPipeError:
            self._logger.error(f"Client {client.address} disconnected while callback executing")
        return False

    def send_broadcast(self, message: object):
        self._logger.debug(f"Sent message to all clients. Message: \n {message}")
        self.server.send_message_to_all(message)

    def __sendError(self, client: Client, type: ErrorTypes, details: str = ""):
        if not isinstance(type, ErrorTypes):
            raise TypeError(f"\"{type}\" is not a valid error type")

        # Don't send error two times in a row
        if self.lastSentMessageIsError:
            return

        self.server.send_message(client, {
            self.eventName: "error",
            self.dataName: {
                "type": type.value,
                "details": details,
            }
        })
        self._logger.debug(f"Sent error to {client.address}. Type: {type.name}")
        self.lastSentMessageIsError = True

    def __message_received(self, client, server, message):
        self._logger.debug(f"Got message from {client.address}: {message}")
        try:
            jsoned = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.__sendError(client, ErrorTypes.badRequest, "Non-json body received")
            return

        event = jsoned.get(self.eventName)
        data = jsoned.get(self.dataName)

        # error - bad format
        if event is None or data is None:
            self.__sendError(client, ErrorTypes.badRequest,
                             f"Fields \"{self.eventName}\" and \"{self.dataName}\" required")
            return

        callback = self.callbacks.get(event)
        # error - unknown event
        if event not in self.callbacks:
            self.__sendError(client, ErrorTypes.unknownEvent, f"Unknown event \"{event}\"")
            return

        self._logger.debug(f'''Parsed:
 | event: {event}
 | data: {data}
''')

        # run callback in new thread
        def sendResult(result: Optional[Union[object, str, None]]):
            if result is None:
                return

            self.callbackThreads.remove(callbackThread)

            if isinstance(result, object):
                result = json.dumps(result)
            self.send(client, result)

        callbackThread = Thread(target=callback, args=(client, data), daemon=True, on_end_callback=sendResult)
        self.callbackThreads.add(callbackThread)
        callbackThread.start()

    def __client_connected(self, client, server):
        self._logger.debug(f"Client {client.address} connected")
        if self.onConnectedCallback is not None:
            pass
            # self.onConnectedCallback(client)

    def __client_disconnected(self, client, server):
        self._logger.debug(f"Client {client.address} disconnected")
        if self.onDisconnectedCallback is not None:
            pass
            # self.onDisconnectedCallback(client)
