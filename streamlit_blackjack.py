import streamlit as st
import random

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []
    st.session_state.moneylist = []
    st.session_state.current_player = None
    st.session_state.page = 'welcome'
    st.session_state.game_state = None

# Set page config
st.set_page_config(page_title="Blackjack Game", page_icon="🎰", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .big-font {
        font-size:40px !important;
        font-weight: bold;
    }
    .medium-font {
        font-size:25px !important;
    }
    .card-display {
        font-size:30px !important;
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main_menu():
    st.markdown('<p class="big-font">🎰 Blackjack Game</p>', unsafe_allow_html=True)
    
    if st.session_state.current_player:
        st.success(f"Welcome, {st.session_state.current_player}!")
        player_idx = st.session_state.players.index(st.session_state.current_player)
        st.info(f"💰 Your Balance: ${st.session_state.moneylist[player_idx]}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎮 Play Game", use_container_width=True):
            st.session_state.page = 'play'
            st.rerun()
        
        if st.button("📜 View Rules", use_container_width=True):
            st.session_state.page = 'rules'
            st.rerun()
    
    with col2:
        if st.button("💵 View Balance", use_container_width=True):
            st.session_state.page = 'balance'
            st.rerun()
        
        if st.button("👤 Change Player", use_container_width=True):
            st.session_state.page = 'change_player'
            st.rerun()
    
    with col3:
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page = 'leaderboard'
            st.rerun()
        
        if st.button("🗑️ Delete Player", use_container_width=True):
            st.session_state.page = 'delete'
            st.rerun()

def welcome_page():
    st.markdown('<p class="big-font">🎰 Welcome to Blackjack!</p>', unsafe_allow_html=True)
    st.markdown("### Enter your name to start playing")
    
    name = st.text_input("Player Name:", key="welcome_name")
    
    if st.button("Start Playing", type="primary"):
        if name:
            st.session_state.players.append(name)
            st.session_state.moneylist.append(100)
            st.session_state.current_player = name
            st.session_state.page = 'menu'
            st.success(f"Welcome {name}! You've received $100 as a starting bonus!")
            st.rerun()
        else:
            st.error("Please enter your name!")

def play_game():
    st.markdown('<p class="medium-font">🎮 Playing Blackjack</p>', unsafe_allow_html=True)
    
    player_idx = st.session_state.players.index(st.session_state.current_player)
    money = st.session_state.moneylist[player_idx]
    
    if money <= 0:
        st.error("You have no money left to play!")
        if st.button("Return to Main Menu"):
            st.session_state.page = 'menu'
            st.rerun()
        return
    
    st.info(f"💰 Current Balance: ${money}")
    
    # Initialize game state if not exists
    if st.session_state.game_state is None:
        st.session_state.game_state = {
            'stage': 'betting',
            'bet': 0,
            'dealer_cards': [],
            'player_cards': [],
            'player_score': 0,
            'dealer_score': 0,
            'result': None,
            'ace_count': 0
        }
    
    game = st.session_state.game_state
    
    # Betting stage
    if game['stage'] == 'betting':
        bet = st.number_input(f"Enter your bet (Max: ${money}):", min_value=1, max_value=money, value=10, step=10)
        
        if st.button("Place Bet", type="primary"):
            game['bet'] = bet
            game['dealer_cards'] = random.choices(range(1, 11), k=2)
            game['player_cards'] = random.choices(range(1, 11), k=2)
            game['ace_count'] = game['player_cards'].count(1)
            game['player_score'] = sum(game['player_cards'])
            game['stage'] = 'playing'
            
            # Deduct bet
            st.session_state.moneylist[player_idx] -= bet
            st.rerun()
    
    # Playing stage
    elif game['stage'] == 'playing':
        st.markdown(f"**Your Bet:** ${game['bet']}")
        
        # Display dealer's cards (one hidden)
        st.markdown("### Dealer's Cards:")
        st.markdown(f'<div class="card-display">🂠 (Hidden) | {game["dealer_cards"][1]}</div>', unsafe_allow_html=True)
        
        # Display player's cards
        st.markdown("### Your Cards:")
        cards_display = " | ".join([str(card) for card in game['player_cards']])
        st.markdown(f'<div class="card-display">{cards_display}</div>', unsafe_allow_html=True)
        
        # Calculate and display score
        player_score = game['player_score']
        if game['ace_count'] > 0 and player_score + 10 <= 21:
            player_score_ace11 = player_score + 10
            st.markdown(f"**Your Score:** {player_score_ace11} (with Ace as 11) or {player_score} (with Ace as 1)")
        else:
            st.markdown(f"**Your Score:** {player_score}")
        
        # Check for instant blackjack
        if game['ace_count'] > 0 and player_score + 10 == 21 and len(game['player_cards']) == 2:
            st.balloons()
            st.success("🎉 Blackjack! You win!")
            winnings = game['bet'] * 2.5
            st.session_state.moneylist[player_idx] += winnings
            st.info(f"💰 You won ${winnings}! New balance: ${st.session_state.moneylist[player_idx]}")
            game['stage'] = 'finished'
            game['result'] = 'blackjack'
        
        # Player actions
        if game['stage'] == 'playing':
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👊 Hit", use_container_width=True):
                    new_card = random.choice(range(1, 11))
                    game['player_cards'].append(new_card)
                    game['player_score'] += new_card
                    if new_card == 1:
                        game['ace_count'] += 1
                    
                    # Handle ace logic
                    if game['player_score'] > 21 and game['ace_count'] > 0:
                        game['player_score'] -= 10
                        game['ace_count'] -= 1
                    
                    # Check for bust
                    if game['player_score'] > 21:
                        st.error("💥 Busted! You lose!")
                        st.info(f"💰 New balance: ${st.session_state.moneylist[player_idx]}")
                        game['stage'] = 'finished'
                        game['result'] = 'bust'
                    
                    st.rerun()
            
            with col2:
                if st.button("✋ Stand", use_container_width=True):
                    # Finalize player score with ace
                    if game['ace_count'] > 0 and game['player_score'] + 10 <= 21:
                        game['player_score'] += 10
                    
                    # Dealer's turn
                    game['dealer_score'] = sum(game['dealer_cards'])
                    
                    while game['dealer_score'] < 17:
                        new_card = random.choice(range(1, 11))
                        game['dealer_cards'].append(new_card)
                        game['dealer_score'] += new_card
                    
                    game['stage'] = 'dealer_turn'
                    st.rerun()
    
    # Dealer's turn
    elif game['stage'] == 'dealer_turn':
        st.markdown(f"**Your Bet:** ${game['bet']}")
        
        # Display all cards
        st.markdown("### Dealer's Cards:")
        dealer_cards_display = " | ".join([str(card) for card in game['dealer_cards']])
        st.markdown(f'<div class="card-display">{dealer_cards_display}</div>', unsafe_allow_html=True)
        st.markdown(f"**Dealer's Score:** {game['dealer_score']}")
        
        st.markdown("### Your Cards:")
        player_cards_display = " | ".join([str(card) for card in game['player_cards']])
        st.markdown(f'<div class="card-display">{player_cards_display}</div>', unsafe_allow_html=True)
        st.markdown(f"**Your Score:** {game['player_score']}")
        
        st.markdown("---")
        
        # Determine winner
        if game['dealer_score'] > 21:
            st.success("🎉 Dealer busted! You win!")
            winnings = game['bet'] * 2
            st.session_state.moneylist[player_idx] += winnings
            st.info(f"💰 You won ${winnings}! New balance: ${st.session_state.moneylist[player_idx]}")
        elif game['dealer_score'] > game['player_score']:
            st.error("😞 Dealer wins! You lose.")
            st.info(f"💰 New balance: ${st.session_state.moneylist[player_idx]}")
        elif game['dealer_score'] < game['player_score']:
            st.success("🎉 You win!")
            winnings = game['bet'] * 2
            st.session_state.moneylist[player_idx] += winnings
            st.info(f"💰 You won ${winnings}! New balance: ${st.session_state.moneylist[player_idx]}")
        else:
            st.warning("🤝 It's a tie! You get your bet back.")
            st.session_state.moneylist[player_idx] += game['bet']
            st.info(f"💰 New balance: ${st.session_state.moneylist[player_idx]}")
        
        game['stage'] = 'finished'
    
    # Game finished
    if game['stage'] == 'finished':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Play Again", use_container_width=True):
                st.session_state.game_state = None
                st.rerun()
        with col2:
            if st.button("🏠 Main Menu", use_container_width=True):
                st.session_state.game_state = None
                st.session_state.page = 'menu'
                st.rerun()

def view_rules():
    st.markdown('<p class="medium-font">📜 Blackjack Rules</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### How to Play:
    
    1. **Goal:** Get as close to 21 as possible without going over.
    
    2. **Card Values:**
       - Number cards (2-10) are worth their face value
       - Face cards are worth 10
       - Aces can be worth 1 or 11
    
    3. **Actions:**
       - **Hit:** Take another card
       - **Stand:** Keep your current hand
    
    4. **Winning:**
       - If you go over 21, you "bust" and lose
       - If you get exactly 21 with your first two cards, it's a Blackjack! (2.5x payout)
       - The player with the highest score without busting wins
       - The dealer must hit until reaching at least 17
    
    5. **Payouts:**
       - Blackjack: 2.5x your bet
       - Regular win: 2x your bet
       - Tie: Get your bet back
    
    Good luck! 🍀
    """)
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

def view_balance():
    st.markdown('<p class="medium-font">💵 Your Balance</p>', unsafe_allow_html=True)
    
    player_idx = st.session_state.players.index(st.session_state.current_player)
    money = st.session_state.moneylist[player_idx]
    
    st.metric("Current Balance", f"${money}")
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

def change_player():
    st.markdown('<p class="medium-font">👤 Change Player</p>', unsafe_allow_html=True)
    
    name = st.text_input("Enter player name:")
    
    if st.button("Switch/Create Player", type="primary"):
        if name:
            if name in st.session_state.players:
                st.session_state.current_player = name
                player_idx = st.session_state.players.index(name)
                st.success(f"Welcome back {name}! Balance: ${st.session_state.moneylist[player_idx]}")
            else:
                st.session_state.players.append(name)
                st.session_state.moneylist.append(100)
                st.session_state.current_player = name
                st.success(f"Welcome {name}! You've received $100 as a starting bonus!")
            
            st.session_state.page = 'menu'
            st.rerun()
        else:
            st.error("Please enter a name!")
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

def delete_player():
    st.markdown('<p class="medium-font">🗑️ Delete Player</p>', unsafe_allow_html=True)
    
    if st.session_state.current_player:
        st.warning(f"Are you sure you want to delete player: {st.session_state.current_player}?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, Delete", type="primary", use_container_width=True):
                player_idx = st.session_state.players.index(st.session_state.current_player)
                del st.session_state.players[player_idx]
                del st.session_state.moneylist[player_idx]
                st.success(f"Player {st.session_state.current_player} deleted!")
                st.session_state.current_player = None
                st.session_state.page = 'welcome'
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.page = 'menu'
                st.rerun()
    else:
        st.info("No player currently logged in.")
        if st.button("← Back to Menu"):
            st.session_state.page = 'menu'
            st.rerun()

def view_leaderboard():
    st.markdown('<p class="medium-font">🏆 Leaderboard</p>', unsafe_allow_html=True)
    
    if not st.session_state.players:
        st.info("No players have played yet.")
    else:
        leaderboard = sorted(zip(st.session_state.players, st.session_state.moneylist), 
                           key=lambda x: x[1], reverse=True)
        
        for position, (player, money) in enumerate(leaderboard, start=1):
            medal = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else "🏅"
            st.markdown(f"### {medal} {position}. {player} - ${money}")
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

# Main app logic
if st.session_state.current_player is None and st.session_state.page != 'welcome':
    st.session_state.page = 'welcome'

# Route to appropriate page
if st.session_state.page == 'welcome':
    welcome_page()
elif st.session_state.page == 'menu':
    main_menu()
elif st.session_state.page == 'play':
    play_game()
elif st.session_state.page == 'rules':
    view_rules()
elif st.session_state.page == 'balance':
    view_balance()
elif st.session_state.page == 'change_player':
    change_player()
elif st.session_state.page == 'delete':
    delete_player()
elif st.session_state.page == 'leaderboard':
    view_leaderboard()
