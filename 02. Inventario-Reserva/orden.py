import zmq
import json
from Inventario.objeto import Objeto, Requerimiento


context = zmq.Context()

req = []
req.append(Requerimiento("Prod001", 10).__dict__)
req.append(Requerimiento("Prod002", 11).__dict__)
req.append(Requerimiento("Prod003", 12).__dict__)
req.append(Requerimiento("Prod004", 13).__dict__)
req.append(Requerimiento("Prod005", 14).__dict__)
req.append(Requerimiento("Prod006", 15).__dict__)
req.append(Requerimiento("Prod007", 16).__dict__)
req.append(Requerimiento("Prod008", 17).__dict__)
req.append(Requerimiento("Prod009", 18).__dict__)
req.append(Requerimiento("Prod010", 19).__dict__)

reqStr = json.dumps(req)
#jsonObj = json.loads(jsonStr)

print("*** MÓDULO DE PROCESAMIENTO DE ÓRDENES ***\n")

#  Socket to talk to server
print("Connecting to Inventario server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:1050") # 35.184.155.202

#socket.send_json(jsonObj)
socket.send_string(reqStr)

message = socket.recv()
print(message)
print(json.dumps(json.loads(message), indent=4))