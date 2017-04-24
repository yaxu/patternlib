from websocket import create_connection

import re

def sendrecv(msg):
    ws = create_connection("ws://localhost:9162")
    welcome = ws.recv()
    print "Received '%s'" % welcome
    if re.match(r'^/welcome', welcome):
        print("sending message:" + msg)
        ws.send(msg)
        result = ws.recv()
        print("received: " + result)
    else:
        raise Exception("unexpected welcome")
    m = re.match(r'^/(\w+) (\w+) (.*)', result)

    if m:
        return(m.group(1), m.group(2), m.group(3))
    else:
        raise Exception("could not understand response")

