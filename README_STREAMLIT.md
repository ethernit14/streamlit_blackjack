# 🎰 Blackjack - Streamlit Version

An interactive Blackjack card game built with Streamlit featuring multiple players, leaderboards, and authentic casino gameplay.

## Features

- 🎮 **Full Blackjack gameplay** with hit/stand mechanics
- 💰 **Player balance system** with starting bonus
- 🏆 **Leaderboard** to track top players
- 👥 **Multiple player support** - switch between players
- 📜 **Complete game rules** built-in
- 🎲 **Realistic card dealing** and scoring
- 💎 **2.5x payout for Blackjack!**

## How to Run

### Prerequisites
```bash
pip install streamlit
```

### Run the App
```bash
streamlit run streamlit_blackjack.py
```

## How to Play

1. **Create a player** by entering your name
2. **Place your bet** (you start with $100)
3. **Hit or Stand** to play your hand
4. Try to get closer to 21 than the dealer without going over!

## Game Rules

- **Goal:** Get as close to 21 as possible without going over
- **Card Values:** 
  - Number cards (2-10): Face value
  - Face cards (J, Q, K): 10 points
  - Aces: 1 or 11 points
- **Blackjack:** 21 with first two cards = 2.5x payout
- **Bust:** Over 21 = automatic loss
- **Dealer:** Must hit until 17 or higher

## Files Included

- `streamlit_blackjack.py` - Main Streamlit application
- `blackjack.py` - Original command-line version
- `README.md` - This file

## Original Version

The original command-line version is available in `blackjack.py`. Run it with:
```bash
python blackjack.py
```

Enjoy playing Blackjack! 🎰
