import time
import streamlit as st

st.set_page_config(page_title="Happy Farm Pro", page_icon="👨‍🌾", layout="wide")
st.title("👨‍🌾 Happy Farm - Vườn Cây Của Nông Dân")

# --- 1. CẤU HÌNH CÂY TRỒNG & SHOP ---
CROPS = {
    "🌾 Lúa": {"buy": 10, "sell": 25, "growth_time": 12},
    "🍅 Cà chua": {"buy": 25, "sell": 60, "growth_time": 20},
    "🍉 Dưa hấu": {"buy": 50, "sell": 140, "growth_time": 30},
}

# --- 2. KHỞI TẠO STATE ---
if "gold" not in st.session_state:
    st.session_state.gold = 100
if "seeds" not in st.session_state:
    st.session_state.seeds = {"🌾 Lúa": 3, "🍅 Cà chua": 1, "🍉 Dưa hấu": 0}
if "farmer_pos" not in st.session_state:
    st.session_state.farmer_pos = 0  # Vị trí bác nông dân đang đứng (0 - 5)

# Khởi tạo 6 ô đất trong vườn
if "plots" not in st.session_state:
    st.session_state.plots = [
        {"crop": None, "plant_time": 0, "watered": False, "water_bonus": 0}
        for _ in range(6)
    ]

# --- 3. SIDEBAR: THÔNG TIN & CỬA HÀNG ---
st.sidebar.header("💰 Ví tiền & Kho hàng")
st.sidebar.metric("Tiền vàng hiện có", f"{st.session_state.gold} G")

st.sidebar.subheader("📦 Hạt giống sở hữu")
for crop, count in st.session_state.seeds.items():
    st.sidebar.write(f"- {crop}: **{count}** hạt")

st.sidebar.subheader("🏪 Cửa hàng Hạt Giống")
selected_crop_to_buy = st.sidebar.selectbox(
    "Chọn hạt giống muốn mua:", list(CROPS.keys())
)
buy_price = CROPS[selected_crop_to_buy]["buy"]

if st.sidebar.button(f"🛒 Mua {selected_crop_to_buy} ({buy_price} G)"):
    if st.session_state.gold >= buy_price:
        st.session_state.gold -= buy_price
        st.session_state.seeds[selected_crop_to_buy] += 1
        st.sidebar.success(f"Đã mua 1 hạt {selected_crop_to_buy}!")
        st.rerun()
    else:
        st.sidebar.error("Không đủ tiền vàng!")

# --- 4. GIAO DIỆN CHÍNH NÔNG TRẠI ---
st.subheader("🏡 Vườn Cây Trồng Trọt")

selected_seed = st.selectbox(
    "Chọn hạt giống để bác nông dân gieo:", list(CROPS.keys())
)

cols = st.columns(3)
now = time.time()

for i, plot in enumerate(st.session_state.plots):
    with cols[i % 3]:
        # Hiển thị bác nông dân 👨‍🌾 nếu đang ở ô này
        farmer_here = "👨‍🌾 " if st.session_state.farmer_pos == i else ""
        water_status = "💧 (Đã tưới)" if plot["watered"] else "🏜️ (Khô)"

        st.markdown(f"### {farmer_here}Ô đất #{i+1} {water_status}")

        # Đặt bác nông dân tới ô đất này
        if st.button(f"🚶 Bác nông dân tới ô #{i+1}", key=f"move_{i}"):
            st.session_state.farmer_pos = i
            st.rerun()

        # Xử lý đất trống
        if plot["crop"] is None:
            st.info("Đất trống")
            if st.button(f"🌱 Gieo {selected_seed}", key=f"plant_{i}"):
                if st.session_state.seeds[selected_seed] > 0:
                    st.session_state.seeds[selected_seed] -= 1
                    plot["crop"] = selected_seed
                    plot["plant_time"] = time.time()
                    plot["watered"] = False
                    plot["water_bonus"] = 0
                    st.session_state.farmer_pos = i
                    st.rerun()
                else:
                    st.warning("Hết hạt giống loại này!")
        else:
            crop_name = plot["crop"]
            growth_required = CROPS[crop_name]["growth_time"]

            # Tính thời gian đã trôi qua + bonus khi tưới nước
            elapsed = (now - plot["plant_time"]) + plot["water_bonus"]

            if elapsed >= growth_required:
                st.success(f"🎉 {crop_name} đã chín!")
                sell_val = CROPS[crop_name]["sell"]

                # Thu hoạch lấy tiền luôn
                if st.button(
                    f"🌾 Thu hoạch (+{sell_val} G)", key=f"harvest_{i}"
                ):
                    st.session_state.gold += sell_val
                    plot["crop"] = None
                    plot["plant_time"] = 0
                    plot["watered"] = False
                    plot["water_bonus"] = 0
                    st.session_state.farmer_pos = i
                    st.toast(f"Bạn đã thu hoạch {crop_name} và nhận {sell_val} G!")
                    st.rerun()
            else:
                progress = min(1.0, elapsed / growth_required)
                rem_time = max(0, int(growth_required - elapsed))
                st.write(f"🌱 {crop_name} (Còn {rem_time}s)")
                st.progress(progress)

                # Nút tưới nước (Rút ngắn thời gian lớn đi 5 giây)
                if not plot["watered"]:
                    if st.button(f"💧 Tưới nước (-5s lớn nhanh)", key=f"water_{i}"):
                        plot["watered"] = True
                        plot["water_bonus"] += 5
                        st.session_state.farmer_pos = i
                        st.rerun()

if st.button("🔄 Cập nhật trạng thái cây (Refresh)"):
    st.rerun()
