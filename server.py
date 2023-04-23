import socket
import random


server_deck =  [(suit, value) for suit in ['spades']
        for value in [1,2,3,4,5,6,7,8,9,10,11,12,13]]


# create a dictionary to store the scores of each player
scores = {1: 0, 2: 0, 3: 0}

# create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define the IP address and port number
host = 'localhost'
port = 8000

# bind the socket to a specific IP address and port number
server_socket.bind((host, port))

# listen for incoming connections
server_socket.listen(3)
print('Server is listening for incoming connections')

# create a list of player names and scores
players = ["Client 1", "Client 2", "Client 3"]
clients = {}
player_scores = {player: 0 for player in players}

client_sockets = []
counter = 1
# accept connections from three clients
# the game only continues after the three clients have connected
print("Waiting for clients to connect!")
while len(client_sockets) < 3:
    sock, client_address = server_socket.accept()
    print('Client {} connected!'.format(counter))
    client_sockets.append(sock)
    clients[sock] = "Client "+ str(counter)
    counter +=1
  
  
# play 13 rounds of the game
for i in range(13):
    print("\nStarting round {}".format(i+1))
    # randomly choose a card from the server's deck
    server_card = random.choice(server_deck)
    print("The server advertised card: {}".format(server_card))
    # remove the chosen card from the server's deck
    server_deck.remove(server_card)
    # send each client the cards in their hand
    for j, client_socket in enumerate(client_sockets):
        client_socket.send(str(server_card).encode())

    # receive one card from each client
    cards_played = []
    for j, client_socket in enumerate(client_sockets):
        while True:
            # receive the card played by this client
            message = client_socket.recv(1024).decode()
            print(str(clients[client_socket])+" sent card {}".format(message))
            if message in cards_played:
                # if the card has already been played, ask the client to play a different card
                #client_socket.send("You have already played this card. Please play a different card.".encode())
                cards_played.append(message)
                break
            else:
                # if the card is new, add it to the list of cards played and move on to the next client
                cards_played.append(message)
                break

    # find the highest card value played in this round
    highest_value = max([int(card.split()[1].strip('() ')) for card in cards_played])
    # find the number of times this value was played
    count = [card.split()[1].strip('() ') for card in cards_played].count(str(highest_value))
    # determine the winner(s) of this round and update their scores
    if count == 1:
        winner_index = [card.split()[1].strip('() ') for card in cards_played].index(str(highest_value))
        winner = players[winner_index]
        print("\n{} wins this round!".format(winner))
        player_scores[winner] += int(server_card[1])
    else:
        #assign both players who tie same
        winners = [players[i] for i in range(count) if cards_played[i].split()[1].strip('() ') == str(highest_value)]
        print("\nWinner of the round: {} and {}".format(", ".join(winners[:-1]), winners[-1]))
        for card in cards_played:
            if card.split()[1].strip('() ') == str(highest_value):
                player_scores[players[cards_played.index(card)]] += int(server_card[1])
        

# determine the winner of the game
winner = max(player_scores, key=player_scores.get)
print("\n{} wins the game with a score of {}!".format(winner, player_scores[winner]))
