# Blackjack Card Game

import random

# Introduction

print("")
players = []
playername = input("Enter your name: ")
players.append(playername)
print("")

print("!!!Welcome to Blackjack!!!")
print("")

print(f"Hello {playername}, let's play Blackjack!")

print("*You have received $100 as a starting bonus*")
moneylist = []
money = 100
moneylist.append(money)
print("")

# Main Menu

def main_menu():
    print("Main Menu")
    print("1. Play Game")
    print("2. View Rules")
    print("3. View Balance")
    print("4. Delete Player")
    print("5. Change Player")
    print("6. Leaderboard")
    print("7. Exit")
    print("")

    choice = input("Enter your choice: ")
    print("")

    if choice == '1':
        play_game()
    elif choice == '2':
        view_rules()
    elif choice == '3':
        view_balance()
    elif choice == '4':
        delete_player()
    elif choice == '5':
        change_player()
    elif choice == '6':
        view_leaderboard()
    elif choice == '7':
        exit_game()
    else:
        print("Invalid choice, please try again.")
        print("")
        main_menu()

# Game
def play_game():
    global money
    print(f"You currently have ${money}.")
    if money <= 0:
        print("You have no money left to play. Now returning to the main menu.")
        print("")
        main_menu()
        return

    while True:
        try:
            bet = int(input("Enter your bet amount: "))
            if bet <= 0:
                print("Bet must be greater than zero.")
                continue
            if bet > money:
                print("You cannot bet more than you have.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    print("")
    money -= bet
    moneylist[players.index(playername)] = money
    print(f"You have placed a bet of {bet}$.")
    print("")
    print("Dealer:\n The game starts now!")

    dealercards = random.choices(range(1, 11), k=2)
    playercards = random.choices(range(1, 11), k=2)
    acequantity = 0
    player_score_ace11 = 0

    if 1 in playercards:
        if playercards[0] == 1 and playercards[1] == 1:
            print("Both of your cards are Aces!")
            acequantity = 2
        elif playercards[0] == 1:
            print("Your first card is an Ace!")
            acequantity = 1
        elif playercards[1] == 1:
            print("Your second card is an Ace!")
            acequantity = 1

    print("")
    print(f"Your cards are: {playercards[0]} and {playercards[1]}.")
    print("")
    player_score = sum(playercards)

    if acequantity != 0:
        player_score_ace11 = player_score + 10
        if player_score_ace11 == 21:
            print("Blackjack! You win!")
            print("")
            money += bet * 2.5 
            moneylist[players.index(playername)] = money
            print(f"You won! Your new balance is {money}$.")
            print("")
            main_menu()
            return

    while player_score <= 21:
        if acequantity == 0:
            print(f"Your current score is: {player_score}.")
        else:
            player_score_ace11 = player_score + 10
            print(f"Your total score is: {player_score_ace11} (with Ace as 11) or {player_score} (with Ace as 1).")
        
        print(f"Dealer's cards are: (First card is hidden) and {dealercards[1]}.")
        action = input("Do you want to 'hit' or 'stand'? ").lower()
        print("")

        if action == 'hit':
            new_card = random.choice(range(1, 11))
            playercards.append(new_card)
            print(f"You drew a {new_card}.")
            player_score += new_card
            if new_card == 1:
                acequantity += 1

            if player_score > 21 and acequantity > 0:
                player_score -= 10
                acequantity -= 1

            if player_score > 21:
                print("You busted! You lose.")
                print("")
                print(f"Your new balance is {money}$.")
                print("")
                break
            else:
                continue

        elif action == 'stand':
            print("You chose to stand.")
            if acequantity != 0 and player_score_ace11 <= 21:
                player_score = player_score_ace11  
            print(f"Your final score is: {player_score}.")
            print("Dealer's turn now.")
            print(f"Dealer's cards are: {dealercards[0]} and {dealercards[1]}.")
            dealer_score = sum(dealercards)
            print(f"Dealer's score is: {dealer_score}.")

            while dealer_score < 17:
                new_card = random.choice(range(1, 11))
                dealercards.append(new_card)
                dealer_score += new_card
                print(f"Dealer drew a {new_card}. Dealer's new score is: {dealer_score}.")

            if dealer_score > 21:
                print("Dealer busted! You win!")
                money += bet * 2
                moneylist[players.index(playername)] = money
                print(f"Your new balance is {money}$.")
                print("")
            elif dealer_score > player_score:
                print("Dealer wins!")
                print("You lose.")
                print(f"Your new balance is {money}$.")
                print("")
            elif dealer_score < player_score:
                print("You win!")
                money += bet * 2
                moneylist[players.index(playername)] = money
                print(f"Your new balance is {money}$.")
                print("")
            else:
                print("It's a tie!")
                print("You get your bet back.")
                money += bet
                moneylist[players.index(playername)] = money
                print(f"Your new balance is {money}$.")
                print("")
            break

        else:
            print("Invalid action. Please choose 'hit' or 'stand'.")
            print("")
            continue

    main_menu()

# View Rules

def view_rules():
    print("Blackjack Rules:")
    print("")
    print("1. The goal is to get as close to 21 without going over.")
    print("2. Face cards are worth 10, Aces can be worth 1 or 11, and all other cards are worth their face value.")
    print("3. Players can 'hit' to take another card or 'stand' to keep their current hand.")
    print("4. If you go over 21, you 'bust' and lose the game.")
    print("5. The player with the highest score without busting wins.")
    print("")
    input("Press Enter to return to the main menu.")
    print("")
    
    main_menu()

# View Balance

def view_balance():
    print(f"You currently have ${money}.")
    print("")

    input("Press Enter to return to the main menu.")
    print("")

    main_menu()

# Delete Player

def delete_player():
    global playername, money, players, moneylist
    print("Deleting player...")
    if playername in players:
        index = players.index(playername)
        del players[index]
        del moneylist[index]
        print(f"Player {playername} has been deleted.")
        print("")
        print("Please create a new player or change to an existing one.")
        print("")
        change_player()
    else:
        print(f"Player {playername} does not exist.")
    
    print("")
    main_menu()

# Change Player

def change_player():
    global playername, money
    print("Changing player...")
    playername = input("Enter player's name: ")
    if playername in players:
        print(f"Welcome back {playername}!")

        money = moneylist[players.index(playername)]  
        print(f"You have ${money} in your balance.")
        print("")
    elif playername in players and moneylist[players.index(playername)] == 0:
        print(f"Welcome back {playername}! You have no money left to play. Now returning to the main menu.")
        print("")
        main_menu()
        return
    else:
        players.append(playername)
        print("")

        money = 100 
        moneylist.append(money)
    
        print(f"Welcome {playername}! You have been given $100 as a starting bonus.")
    print("")
    
    main_menu()

# View Leaderboard

def view_leaderboard():
    print("Leaderboard:")
    print("")
    if not players:
        print("No players have played yet.")
    else:
        leaderboard = sorted(zip(players, moneylist), key=lambda x: x[1], reverse=True)
        for position, (player, money) in enumerate(leaderboard, start=1):
            print(f"{position}. {player} - ${money}")
    print("")
    
    input("Press Enter to return to the main menu.")
    print("")
    
    main_menu()


# Exit Game

def exit_game():
    print("Thank you for playing! Goodbye!")
    print("")
    exit()

main_menu()