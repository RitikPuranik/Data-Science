import streamlit as st
import numpy as np

# -------------------------------
# Initialize Session State
# -------------------------------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

if "current" not in st.session_state:
    st.session_state.current = 1

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "winner" not in st.session_state:
    st.session_state.winner = None


# -------------------------------
# Winner Function
# -------------------------------
def check_winner(b):
    if 3 in np.sum(b, axis=1) or 3 in np.sum(b, axis=0):
        return "X"

    if -3 in np.sum(b, axis=1) or -3 in np.sum(b, axis=0):
        return "O"

    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return "X"

    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return "O"

    if not (0 in b):
        return "DRAW"

    return None


# -------------------------------
# Handle Move
# -------------------------------
def make_move(row, col):
    if st.session_state.game_over:
        return

    if st.session_state.board[row, col] != 0:
        return

    st.session_state.board[row, col] = st.session_state.current

    result = check_winner(st.session_state.board)

    if result:
        st.session_state.game_over = True
        st.session_state.winner = result
    else:
        st.session_state.current *= -1


# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮")

st.title("🎮 Tic Tac Toe")
st.write("Built with NumPy + Streamlit")

player = "X" if st.session_state.current == 1 else "O"

if not st.session_state.game_over:
    st.subheader(f"Current Player: {player}")

symbols = {
    0: "",
    1: "❌",
    -1: "⭕"
}

# Board
for i in range(3):
    cols = st.columns(3)

    for j in range(3):
        with cols[j]:
            value = symbols[st.session_state.board[i, j]]

            if st.button(
                value if value else " ",
                key=f"{i}{j}",
                use_container_width=True,
            ):
                make_move(i, j)
                st.rerun()

# Result
if st.session_state.game_over:
    if st.session_state.winner == "DRAW":
        st.success("🤝 It's a Draw!")
    else:
        st.balloons()
        st.success(f"🎉 {st.session_state.winner} Wins!")

# Restart Button
if st.button("🔄 Restart Game"):
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.game_over = False
    st.session_state.winner = None
    st.rerun()