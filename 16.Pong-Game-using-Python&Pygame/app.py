import streamlit as st

# Game Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 20
PADDLE_SPEED = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Initialize Game State
if 'left_paddle' not in st.session_state:
    st.session_state.left_paddle = HEIGHT // 2 - PADDLE_HEIGHT // 2
if 'right_paddle' not in st.session_state:
    st.session_state.right_paddle = HEIGHT // 2 - PADDLE_HEIGHT // 2
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = BALL_SPEED_X
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = BALL_SPEED_Y
if 'left_score' not in st.session_state:
    st.session_state.left_score = 0
if 'right_score' not in st.session_state:
    st.session_state.right_score = 0

# Move Paddle
def move_paddle(player, direction):
    if player == "left":
        if direction == "up" and st.session_state.left_paddle > 0:
            st.session_state.left_paddle -= PADDLE_SPEED
        elif direction == "down" and st.session_state.left_paddle < HEIGHT - PADDLE_HEIGHT:
            st.session_state.left_paddle += PADDLE_SPEED
    elif player == "right":
        if direction == "up" and st.session_state.right_paddle > 0:
            st.session_state.right_paddle -= PADDLE_SPEED
        elif direction == "down" and st.session_state.right_paddle < HEIGHT - PADDLE_HEIGHT:
            st.session_state.right_paddle += PADDLE_SPEED

# Move Ball
def move_ball():
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    # Ball Collision with Walls
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= HEIGHT - BALL_SIZE:
        st.session_state.ball_dy *= -1

    # Ball Collision with Left Paddle
    if (st.session_state.ball_x <= PADDLE_WIDTH and 
        st.session_state.left_paddle <= st.session_state.ball_y <= st.session_state.left_paddle + PADDLE_HEIGHT):
        st.session_state.ball_dx *= -1

    # Ball Collision with Right Paddle
    if (st.session_state.ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and 
        st.session_state.right_paddle <= st.session_state.ball_y <= st.session_state.right_paddle + PADDLE_HEIGHT):
        st.session_state.ball_dx *= -1

    # Scoring
    if st.session_state.ball_x <= 0:
        st.session_state.right_score += 1
        reset_ball()
    if st.session_state.ball_x >= WIDTH:
        st.session_state.left_score += 1
        reset_ball()

# Reset Ball Position
def reset_ball():
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx *= -1

# Streamlit UI
st.title("🎮 Pong Game with Streamlit")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Left Player")
    st.write(f"Score: {st.session_state.left_score}")
    st.button("⬆️ Up", on_click=move_paddle, args=("left", "up"))
    st.button("⬇️ Down", on_click=move_paddle, args=("left", "down"))

with col3:
    st.subheader("Right Player")
    st.write(f"Score: {st.session_state.right_score}")
    st.button("⬆️ Up", on_click=move_paddle, args=("right", "up"))
    st.button("⬇️ Down", on_click=move_paddle, args=("right", "down"))

# Ball Movement Button
if st.button("▶ Move Ball"):
    move_ball()

# Display Ball Position
st.write(f"🏀 Ball Position: ({st.session_state.ball_x}, {st.session_state.ball_y})")

st.markdown("📌 Click 'Move Ball' to simulate movement, use buttons to move paddles.")

