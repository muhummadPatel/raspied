from channels import route
from .consumers import ws_connect, ws_receive, ws_disconnect
from .consumers import robot_terminal_join, robot_terminal_leave, robot_terminal_send, robot_terminal_kill


# websocket action routing
websocket_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]


# Routing for the robot terminal consumers
robot_terminal_routing = [
    route('robot.receive', robot_terminal_join, command='^join$'),
    route('robot.receive', robot_terminal_leave, command='^leave$'),
    route('robot.receive', robot_terminal_send, command='^send$'),
    route('robot.receive', robot_terminal_kill, command='^kill$'),
]
