from multiprocessing import Process
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
import websockets, asyncio
from .health_check import health_check


class ServerManager:
    def __init__(self, ip, port, max_servers, init_func):
        self.ip = ip
        self.port = port
        self.max_servers = max_servers
        self.init_func = init_func  # Function ran to initialise a new server

        self.servers = list()

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get":
            return_msg = dumps({"type": "get", "content": [server for server in self.servers]})
            await websocket.send(return_msg)

        elif msg["type"] == "create":
            if len(self.servers)+1 <= self.max_servers:

                try:
                    new_server_port = self.port+1 + (len(self.servers)*2)
                    process = Process(target=self.init_func, args=(self.ip, new_server_port, msg["parameters"],))
                    process.start()
                    self.servers.append({"port": new_server_port, "parameters": msg["parameters"]})
                    return_msg = dumps({"type": "create", "status": "success", "content": "thread_started", "port": new_server_port})
                    await websocket.send(return_msg)
                    await websocket.close()

                except KeyError:
                    return_msg = dumps({"type": "create", "status": "error", "content": "no_parameters_given"})
                    await websocket.send(return_msg)
                    await websocket.close()
                    raise NoParametersGiven()

            else:
                return_msg = dumps({"type": "create", "status": "error", "content": "max_server_limit_reached"})
                await websocket.send(return_msg)
                await websocket.close()

    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port, process_request=health_check):
                await asyncio.Future()

        except OSError:
            raise PortInUseError(self.port)

    def run(self):
        asyncio.run(self._run())
