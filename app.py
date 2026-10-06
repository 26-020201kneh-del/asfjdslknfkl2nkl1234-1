import streamlit as st

# -------------------------
# 기본 설정
# -------------------------
BOARD_SIZE = 15

st.set_page_config(
    page_title="오목 게임",
    page_icon="⚫",
    layout="centered"
)

st.title("⚫ 오목 게임 ⚪")
st.write("흑돌부터 시작합니다. 먼저 5개의 돌을 연속으로 놓으면 승리합니다.")

# -------------------------
# 게임 상태 초기화
# -------------------------
if "board" not in st.session_state:
    st.session_state.board = [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

if "turn" not in st.session_state:
    st.session_state.turn = 1  # 1 = 흑, 2 = 백

if "winner" not in st.session_state:
    st.session_state.winner = 0


# -------------------------
# 승리 확인
# -------------------------
def check_winner(board, row, col, player):
    directions = [
        (1, 0),   # 세로
        (0, 1),   # 가로
        (1, 1),   # 대각선 \
        (1, -1),  # 대각선 /
    ]

    for dr, dc in directions:
        count = 1

        # 한 방향
        r, c = row + dr, col + dc
        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r += dr
            c += dc

        # 반대 방향
        r, c = row - dr, col - dc
        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False


# -------------------------
# 돌 놓기
# -------------------------
def place_stone(row, col):
    if st.session_state.winner != 0:
        return

    board = st.session_state.board

    # 이미 돌이 있으면 무시
    if board[row][col] != 0:
        return

    player = st.session_state.turn

    board[row][col] = player

    # 승리 확인
    if check_winner(board, row, col, player):
        st.session_state.winner = player
    else:
        # 턴 변경
        st.session_state.turn = 3 - player


# -------------------------
# 게임판 표시
# -------------------------
st.markdown("### 게임판")

for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE, gap="small")

    for col in range(BOARD_SIZE):
        value = st.session_state.board[row][col]

        if value == 1:
            text = "⚫"
        elif value == 2:
            text = "⚪"
        else:
            text = "＋"

        cols[col].button(
            text,
            key=f"cell_{row}_{col}",
            on_click=place_stone,
            args=(row, col),
            use_container_width=True
        )


# -------------------------
# 게임 상태 표시
# -------------------------
if st.session_state.winner == 1:
    st.success("🎉 흑돌 승리!")
elif st.session_state.winner == 2:
    st.success("🎉 백돌 승리!")
else:
    if st.session_state.turn == 1:
        st.info("현재 차례: ⚫ 흑돌")
    else:
        st.info("현재 차례: ⚪ 백돌")


# -------------------------
# 다시 시작
# -------------------------
if st.button("🔄 게임 다시 시작", use_container_width=True):
    st.session_state.board = [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]
    st.session_state.turn = 1
    st.session_state.winner = 0
    st.rerun()
