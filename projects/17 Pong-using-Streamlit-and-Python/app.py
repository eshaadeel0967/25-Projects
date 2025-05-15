import streamlit as st
import matplotlib.pyplot as plt


# Initialize session state variables
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = 50
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = 50
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = 2
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = 2
if 'left_paddle' not in st.session_state:
    st.session_state.left_paddle = 40
if 'right_paddle' not in st.session_state:
    st.session_state.right_paddle = 40
if 'score_left' not in st.session_state:
    st.session_state.score_left = 0
if 'score_right' not in st.session_state:
    st.session_state.score_right = 0

# Game settings
canvas_width = 100
canvas_height = 100
paddle_height = 20
paddle_speed = 5

st.title("🏓 Streamlit Pong")

# Controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬆ Left Paddle"):
        st.session_state.left_paddle = max(0, st.session_state.left_paddle - paddle_speed)
with col2:
    if st.button("⬇ Left Paddle"):
        st.session_state.left_paddle = min(canvas_height - paddle_height, st.session_state.left_paddle + paddle_speed)
with col3:
    if st.button("⬆ Right Paddle"):
        st.session_state.right_paddle = max(0, st.session_state.right_paddle - paddle_speed)
with col4:
    if st.button("⬇ Right Paddle"):
        st.session_state.right_paddle = min(canvas_height - paddle_height, st.session_state.right_paddle + paddle_speed)

# Ball movement logic
def move_ball():
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    # Bounce top/bottom
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= canvas_height:
        st.session_state.ball_dy *= -1

    # Left paddle collision
    if (st.session_state.ball_x <= 5 and
        st.session_state.left_paddle <= st.session_state.ball_y <= st.session_state.left_paddle + paddle_height):
        st.session_state.ball_dx *= -1

    # Right paddle collision
    if (st.session_state.ball_x >= 95 and
        st.session_state.right_paddle <= st.session_state.ball_y <= st.session_state.right_paddle + paddle_height):
        st.session_state.ball_dx *= -1

    # Score conditions
    if st.session_state.ball_x < 0:
        st.session_state.score_right += 1
        reset_ball()
    elif st.session_state.ball_x > canvas_width:
        st.session_state.score_left += 1
        reset_ball()

# Reset ball position
def reset_ball():
    st.session_state.ball_x = 50
    st.session_state.ball_y = 50
    st.session_state.ball_dx *= -1

# Move ball
move_ball()

# Scoreboard
st.markdown(f"### 🅰️ Left: {st.session_state.score_left}  |  🅱️ Right: {st.session_state.score_right}")

# Display canvas
fig, ax = plt.subplots()
ax.set_xlim(0, canvas_width)
ax.set_ylim(0, canvas_height)

# Draw paddles
ax.add_patch(plt.Rectangle((1, st.session_state.left_paddle), 2, paddle_height, color='blue'))
ax.add_patch(plt.Rectangle((97, st.session_state.right_paddle), 2, paddle_height, color='red'))

# Draw ball
ax.plot(st.session_state.ball_x, st.session_state.ball_y, 'yo', markersize=10)

ax.axis('off')
st.pyplot(fig)

# Refresh button to move the ball manually
if st.button("🔁 Next Frame"):
    st.rerun()

st.write("🎮 Enjoy the game!")
st.write("🔹 Developed by Esha")