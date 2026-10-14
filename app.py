import streamlit as st
import random

# Cấu hình trang
st.set_page_config(page_title="Nông Trại Hạnh Phúc", page_icon="🌾")

st.title("🌾 Nông Trại Hạnh Phúc 🚜")
st.write("Chào mừng bạn đến với game nông trại đơn giản!")

# Khởi tạo điểm số trong session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1

st.write(f"### 🏆 Điểm của bạn: **{st.session_state.score}**")
st.write(f"#### ⭐️ Cấp độ nông trại: **{st.session_state.level}**")

# Hàm cập nhật điểm và cấp độ
def update_game(points_change, message_success, message_error):
    st.session_state.score += points_change
    
    if points_change >= 0:
        st.success(message_success)
    else:
        st.error(message_error)

    # Cập nhật cấp độ mỗi 100 điểm
    new_level = max(1, st.session_state.score // 100 + 1)
    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.balloons()
        st.info(f"Chúc mừng! Bạn đã lên cấp {st.session_state.level}!")

# Giao diện hành động nông trại
st.write("---")
st.subheader("🛠️ Hành động hôm nay")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌱 Trồng Cây Mới"):
        points = random.randint(5, 15)
        update_game(points, f"Bạn đã trồng cây thành công! +{points} điểm.", "")

with col2:
    if st.button("💧 Tưới Nước"):
        if random.random() > 0.1: # 90% thành công
            points = random.randint(3, 8)
            update_game(points, f"Cây đã được tưới nước. +{points} điểm.", "")
        else:
            update_game(-10, "", "Hệ thống tưới nước bị hỏng! -10 điểm.")

with col3:
    if st.button("🌾 Thu Hoạch (Cần may mắn)"):
        # Điểm thu hoạch cao hơn nhưng có rủi ro
        outcome = random.random()
        if outcome > 0.5: # 50% thành công lớn
            points = random.randint(20, 50)
            update_game(points, f"Mùa màng bội thu! +{points} điểm.", "")
        elif outcome > 0.2: # 30% thu hoạch bình thường
            points = random.randint(10, 20)
            update_game(points, f"Thu hoạch bình thường. +{points} điểm.", "")
        else: # 20% mất mùa
            points_lost = random.randint(-20, -10)
            update_game(points_lost, "", f"Mất mùa do thời tiết xấu! {points_lost} điểm.")

st.write("---")
st.info("Trò chơi đơn giản này giúp bạn hiểu cách hoạt động của ứng dụng trên Streamlit!")
