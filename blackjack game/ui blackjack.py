import tkinter as tk
from tkinter import messagebox
import random

suits = ['♠', '♣', '♥', '♦']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
values = {**{str(i): i for i in range(2, 11)}, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

hands = {
    "dealer": [],
    "player1": [],
    "player2": [],
    "player3": []
}
split_hands = {
    "player1": [],
    "player2": [],
    "player3": []
}
balances = {
    "player1": 1000,
    "player2": 1000,
    "player3": 1000
}
bets = {
    "player1": 0,
    "player2": 0,
    "player3": 0
}
split_bets = {
    "player1": 0,
    "player2": 0,
    "player3": 0
}
player_order = ["player1", "player2", "player3", "dealer"]
current_player_index = 0
current_player = player_order[current_player_index]
dealer_hidden = True
is_split = False

def calculate_score(hand):
    score = 0
    aces = 0
    
    for card in hand:
        value = card[:-1]
        score += values[value]
        if value == 'A':
            aces += 1
    
    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score

def is_soft_hand(hand):
    return 'A' in [card[:-1] for card in hand] and calculate_score(hand) <= 21

def ai_recommendation(player_hand, dealer_upcard):
    player_score = calculate_score(player_hand)
    is_soft = is_soft_hand(player_hand)
    dealer_upcard_value = values[dealer_upcard[:-1]]
    
    if is_soft:
        if player_score >= 19:
            return "Stand"
        elif player_score == 18:
            if dealer_upcard_value in [9, 10, 11]:
                return "Hit"
            else:
                return "Stand"
        else:
            return "Hit"
    else:
        if player_score >= 17:
            return "Stand"
        elif player_score >= 13:
            if dealer_upcard_value <= 6:
                return "Stand"
            else:
                return "Hit"
        elif player_score == 12:
            if dealer_upcard_value in [4, 5, 6]:
                return "Stand"
            else:
                return "Hit"
        else:
            return "Hit"

def update_ui():
    if dealer_hidden:
        dealer_display = ["🂠"] + hands["dealer"][1:]
    else:
        dealer_display = hands["dealer"]

    dealer_cards.config(text=" ".join(dealer_display))
    player1_cards.config(text=" ".join(hands["player1"]))
    player2_cards.config(text=" ".join(hands["player2"]))
    player3_cards.config(text=" ".join(hands["player3"]))
    
    if dealer_hidden:
        dealer_score.config(text="??")
    else:
        dealer_score.config(text=calculate_score(hands["dealer"]))
    
    player1_score.config(text=calculate_score(hands["player1"]))
    player2_score.config(text=calculate_score(hands["player2"]))
    player3_score.config(text=calculate_score(hands["player3"]))
    
    player1_balance.config(text=f"Balance: ${balances['player1']}")
    player2_balance.config(text=f"Balance: ${balances['player2']}")
    player3_balance.config(text=f"Balance: ${balances['player3']}")
    player1_bet.config(text=f"Bet: ${bets['player1']}")
    player2_bet.config(text=f"Bet: ${bets['player2']}")
    player3_bet.config(text=f"Bet: ${bets['player3']}")
    
    if balances["player1"] == 0:
        player1_bet_entry.config(state=tk.DISABLED)
    if balances["player2"] == 0:
        player2_bet_entry.config(state=tk.DISABLED)
    if balances["player3"] == 0:
        player3_bet_entry.config(state=tk.DISABLED)
    
    status_label.config(text=f"{current_player}'s Turn")

def place_bets():
    try:
        for player in ["player1", "player2", "player3"]:
            if balances[player] > 0:
                bet = 0
                if player == "player1":
                    bet = int(player1_bet_entry.get())
                elif player == "player2":
                    bet = int(player2_bet_entry.get())
                elif player == "player3":
                    bet = int(player3_bet_entry.get())
                
                if bet > balances[player]:
                    messagebox.showerror("Error", f"{player} cannot bet more than their balance!")
                    return
                if bet < 0:
                    messagebox.showerror("Error", "Bet cannot be negative!")
                    return
        
        if balances["player1"] > 0:
            bets["player1"] = int(player1_bet_entry.get())
            balances["player1"] -= bets["player1"]
        else:
            bets["player1"] = 0
        if balances["player2"] > 0:
            bets["player2"] = int(player2_bet_entry.get())
            balances["player2"] -= bets["player2"]
        else:
            bets["player2"] = 0
        if balances["player3"] > 0:
            bets["player3"] = int(player3_bet_entry.get())
            balances["player3"] -= bets["player3"]
        else:
            bets["player3"] = 0
        
        player1_bet_entry.config(state=tk.DISABLED)
        player2_bet_entry.config(state=tk.DISABLED)
        player3_bet_entry.config(state=tk.DISABLED)
        place_bets_button.config(state=tk.DISABLED)
        
        start_game()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid bet amounts!")

def start_game():
    global current_player_index, current_player, deck, hands, dealer_hidden
    deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
    random.shuffle(deck)
    hands = { "dealer": [], "player1": [], "player2": [], "player3": [] }
    split_hands = { "player1": [], "player2": [], "player3": [] }
    split_bets = { "player1": 0, "player2": 0, "player3": 0 }
    current_player_index = 0
    current_player = player_order[current_player_index]
    dealer_hidden = True
    
    for _ in range(2):
        if bets["player1"] > 0:
            hands["player1"].append(deck.pop())
        if bets["player2"] > 0:
            hands["player2"].append(deck.pop())
        if bets["player3"] > 0:
            hands["player3"].append(deck.pop())
        hands["dealer"].append(deck.pop())
    
    update_ui()
    status_label.config(text="Player 1's Turn")

def hit():
    global current_player
    if current_player in hands:
        hands[current_player].append(deck.pop())
        update_ui()
        
        if calculate_score(hands[current_player]) > 21:
            status_label.config(text=f"{current_player} BUSTED!")
            next_turn()

def stand():
    next_turn()

def double_down():
    global current_player
    if current_player in bets:
        if balances[current_player] >= bets[current_player]:
            bets[current_player] *= 2
            balances[current_player] -= bets[current_player] // 2
            hands[current_player].append(deck.pop())
            update_ui()
            next_turn()
        else:
            messagebox.showerror("Error", "Not enough balance to double down!")

def split():
    global current_player, is_split
    if current_player in hands:
        if len(hands[current_player]) == 2 and hands[current_player][0][:-1] == hands[current_player][1][:-1]:
            if balances[current_player] >= bets[current_player]:
                split_hands[current_player] = [hands[current_player].pop()]
                split_bets[current_player] = bets[current_player]
                balances[current_player] -= bets[current_player]
                is_split = True
                update_ui()
            else:
                messagebox.showerror("Error", "Not enough balance to split!")
        else:
            messagebox.showerror("Error", "You can only split with two cards of the same rank!")

def exit_game():
    root.destroy()

def reset_game():
    global current_player_index, current_player, deck, hands, dealer_hidden, bets, split_bets, split_hands
    if dealer_hidden:
        for player in ["player1", "player2", "player3"]:
            balances[player] += bets[player]
    else:
        pass
    
    for player in ["player1", "player2", "player3"]:
        bets[player] = 0
        split_bets[player] = 0
        split_hands[player] = []
    
    deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
    random.shuffle(deck)
    hands = { "dealer": [], "player1": [], "player2": [], "player3": [] }
    current_player_index = 0
    current_player = player_order[current_player_index]
    dealer_hidden = True
    
    player1_bet_entry.config(state=tk.NORMAL)
    player2_bet_entry.config(state=tk.NORMAL)
    player3_bet_entry.config(state=tk.NORMAL)
    place_bets_button.config(state=tk.NORMAL)
    
    player1_bet_entry.delete(0, tk.END)
    player2_bet_entry.delete(0, tk.END)
    player3_bet_entry.delete(0, tk.END)
    
    if balances["player1"] == 0:
        player1_bet_entry.config(state=tk.DISABLED)
    if balances["player2"] == 0:
        player2_bet_entry.config(state=tk.DISABLED)
    if balances["player3"] == 0:
        player3_bet_entry.config(state=tk.DISABLED)
    
    update_ui()
    status_label.config(text="Place Bets to Start")

def next_turn():
    global current_player_index, current_player, dealer_hidden, is_split
    current_player_index += 1
    
    if current_player_index < len(player_order):
        current_player = player_order[current_player_index]
        
        if current_player == "dealer":
            dealer_hidden = False
            update_ui()
            status_label.config(text="Dealer's Turn")
            root.after(1000, dealer_turn)
        else:
            if bets[current_player] > 0:
                status_label.config(text=f"{current_player}'s Turn")
            else:
                next_turn()
    else:
        check_winner()

def dealer_turn():
    while calculate_score(hands["dealer"]) < 17:
        hands["dealer"].append(deck.pop())
        update_ui()
    check_winner()

def check_winner():
    dealer_score_value = calculate_score(hands["dealer"])
    result = []

    for player in ["player1", "player2", "player3"]:
        if bets[player] > 0:
            player_score = calculate_score(hands[player])
            if player_score > 21:
                result.append(f"{player} BUSTED (Loses ${bets[player]})")
            elif dealer_score_value > 21 or player_score > dealer_score_value:
                result.append(f"{player} WINS (Wins ${bets[player] * 2})")
                balances[player] += bets[player] * 2
            elif player_score < dealer_score_value:
                result.append(f"{player} LOSES (Loses ${bets[player]})")
            else:
                result.append(f"{player} PUSHES (Keeps ${bets[player]})")
                balances[player] += bets[player]

    final_result_label.config(text=", ".join(result))
    update_ui()

def ai_assist():
    if current_player in ["player1", "player2", "player3"]:
        player_hand = hands[current_player]
        dealer_upcard = hands["dealer"][0]
        recommendation = ai_recommendation(player_hand, dealer_upcard)
        messagebox.showinfo("AI Recommendation", f"AI recommends: {recommendation}")

root = tk.Tk()
root.title("Advanced Blackjack Game")
root.geometry("900x700")
root.config(bg="green")

tk.Label(root, text="Dealer's Hand:", font=("Arial", 16), bg="green", fg="white").grid(row=0, column=0, columnspan=3, pady=10)
dealer_cards = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="white")
dealer_cards.grid(row=1, column=0, columnspan=3)
dealer_score = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="yellow")
dealer_score.grid(row=2, column=0, columnspan=3)

tk.Label(root, text="Player 1's Hand:", font=("Arial", 16), bg="green", fg="white").grid(row=3, column=0, pady=10)
player1_cards = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="white")
player1_cards.grid(row=4, column=0)
player1_score = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="yellow")
player1_score.grid(row=5, column=0)
player1_balance = tk.Label(root, text=f"Balance: ${balances['player1']}", font=("Arial", 14), bg="green", fg="yellow")
player1_balance.grid(row=6, column=0)
player1_bet = tk.Label(root, text=f"Bet: ${bets['player1']}", font=("Arial", 14), bg="green", fg="yellow")
player1_bet.grid(row=7, column=0)
player1_bet_entry = tk.Entry(root)
player1_bet_entry.grid(row=8, column=0)

tk.Label(root, text="Player 2's Hand:", font=("Arial", 16), bg="green", fg="white").grid(row=3, column=1, pady=10)
player2_cards = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="white")
player2_cards.grid(row=4, column=1)
player2_score = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="yellow")
player2_score.grid(row=5, column=1)
player2_balance = tk.Label(root, text=f"Balance: ${balances['player2']}", font=("Arial", 14), bg="green", fg="yellow")
player2_balance.grid(row=6, column=1)
player2_bet = tk.Label(root, text=f"Bet: ${bets['player2']}", font=("Arial", 14), bg="green", fg="yellow")
player2_bet.grid(row=7, column=1)
player2_bet_entry = tk.Entry(root)
player2_bet_entry.grid(row=8, column=1)

tk.Label(root, text="Player 3's Hand:", font=("Arial", 16), bg="green", fg="white").grid(row=3, column=2, pady=10)
player3_cards = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="white")
player3_cards.grid(row=4, column=2)
player3_score = tk.Label(root, text="", font=("Arial", 14), bg="green", fg="yellow")
player3_score.grid(row=5, column=2)
player3_balance = tk.Label(root, text=f"Balance: ${balances['player3']}", font=("Arial", 14), bg="green", fg="yellow")
player3_balance.grid(row=6, column=2)
player3_bet = tk.Label(root, text=f"Bet: ${bets['player3']}", font=("Arial", 14), bg="green", fg="yellow")
player3_bet.grid(row=7, column=2)
player3_bet_entry = tk.Entry(root)
player3_bet_entry.grid(row=8, column=2)

place_bets_button = tk.Button(root, text="Place Bets", command=place_bets)
place_bets_button.grid(row=9, column=0, columnspan=3, pady=10)

button_frame = tk.Frame(root, bg="green")
button_frame.grid(row=10, column=0, columnspan=3, pady=20)

hit_button = tk.Button(button_frame, text="Hit", command=hit)
hit_button.pack(side=tk.LEFT, padx=10)

stand_button = tk.Button(button_frame, text="Stand", command=stand)
stand_button.pack(side=tk.LEFT, padx=10)

double_down_button = tk.Button(button_frame, text="Double Down", command=double_down)
double_down_button.pack(side=tk.LEFT, padx=10)

split_button = tk.Button(button_frame, text="Split", command=split)
split_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_game)
reset_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_game)
exit_button.pack(side=tk.LEFT, padx=10)

ai_assist_button = tk.Button(button_frame, text="AI Assist", command=ai_assist)
ai_assist_button.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="", font=("Arial", 16), bg="green", fg="white")
status_label.grid(row=11, column=0, columnspan=3, pady=10)

final_result_label = tk.Label(root, text="", font=("Arial", 16), bg="green", fg="yellow")
final_result_label.grid(row=12, column=0, columnspan=3, pady=10)

root.mainloop()