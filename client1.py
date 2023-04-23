import socket
import random

# define the IP address and port number of the server
host = 'localhost'
port = 8000

# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server's IP address and port number
client_socket.connect((host, port))
print('Connected to the server')

# define the list of cards available to the client
client_deck = [(suit, value) for suit in ['hearts', 'diamonds', 'clubs']
               for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]

# play 13 rounds of the game
for i in range(13):
    # receive the advertised card from the server
    message = client_socket.recv(1024).decode()
    print('The server advertised card:', message)

    # choose a card randomly from the client's deck
    client_card = random.choice(client_deck)
    print('Playing card:', client_card)

    # send the chosen card to the server
    client_socket.send(str(client_card).encode())

    # remove the chosen card from the client's deck
    client_deck.remove(client_card)

# receive the final result from the server
message = client_socket.recv(1024).decode()
print(message)

# close the socket
client_socket.close()
