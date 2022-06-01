# chessOnline
Chess online game made with Python. Client-Server communication is realized with sockets (IPv4-TCP, flag+data format messages). "Offline" game made with pygame, chess logic is checked and server on server side, so no client manipulation (bad move etc.) is possible.

# Example
![game 1](game1.PNG?raw=true "Example")
![game 2](game2.PNG?raw=true "Example")
![game 3](game3.PNG?raw=true "Example")
## Technologies
- PyGame - client-side game
- socket - client-server communication
- select - check if any data to receive in client-server socket
- threading - used in server process, to simultaneous service of many clients

## Getting Started
Run chess server with: 

*python game_server.py* [ip] [port]

## Requirements:
* requiremetns.txt

## Author
* **Dominik Baran** - [MasterGTFX](https://github.com/MasterGTFX)

## License
This project is free to use or modify.
