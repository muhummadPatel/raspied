from channels import include


# Map which channels are handled by which consumers
channel_routing = [
    # Include routing from the students app for the specific websocket path
    include('students.routing.websocket_routing', path=r'^/robot_terminal/stream'),

    # Include routing from the students app for all the terminal actions
    include('students.routing.robot_terminal_routing'),
]
