#! /Work1/HOME/eonebi/anaconda3/envs/streamlit_env/bin/python3

# PlateView / ColonyMap
# streamlit run ./virtual_colony_reading_web_demo_v1.py

import streamlit as st
import io 
from PIL import Image, ImageDraw
from src.data_loader import load_data
#from src.plate_visualizer import generate_plate_view

st.header('Plate View')
st.divider()

st.markdown("### Upload your data")
uploaded_file = st.file_uploader("", type=['txt', 'tsv'], label_visibility="collapsed")

st.markdown("#### Select input data type.")
chosen_type = st.selectbox(
    "", 
    ('Taxonomy', 'Virulence Factor'),
    label_visibility="collapsed"
)

# 세부 옵션 처리를 위한 초기화
chosen_level = None
if chosen_type == "Taxonomy":
    st.markdown("##### Choose taxonomy level")
    chosen_level = st.radio("", ('Kindom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'), horizontal=True, label_visibility="collapsed")

st.write("")
st.markdown("### Choose Visualization Option")
st.markdown("#### Color By")
chosen_color = st.radio("", ('Each taxon', 'Gram-stain'), horizontal=True, label_visibility="collapsed")

# 세션 상태(session_state) 초기화 및 옵션 변경 감지 로직
if 'plate_image' not in st.session_state:
    st.session_state.plate_image = None
if 'plate_bytes' not in st.session_state:
    st.session_state.plate_bytes = None

# 현재 선택한 옵션들의 상태 하나의 튜플로 묶기
current_options = (uploaded_file is not None, chosen_type, chosen_color)

if "previous_options" not in st.session_state:
    st.session_state.previous_options = current_options

# 이전 옵션과 현재 옵션이 다르면? = 유저가 옵션을 변경한 경우
if st.session_state.previous_options != current_options:
    st.session_state.plate_image = None
    st.session_state.plate_bytes = None
    st.session_state.previous_options = current_options

# Visualize! 안내 문구와 버튼을 가로로 정렬 (Enter 단축키 포함)
with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.markdown("#### Ready to view tour plate?")
    click_visualize = st.button("Visualize!", type='primary', shortcut='Enter', use_container_width=True)

# 버튼 클릭 시 작동하는 내부 프로세스
if click_visualize:
    if not uploaded_file:
        st.warning("⚠️ Please upload a data file first.")
    else:
        st.success("🎨 Generating Plate Image...")

        # --------------------------------------------------
        # 💡 [구현 파트 연동]
        # --------------------------------------------------
        # df = load_data(uploaded_file)

        # if df is not None:
        #     generated_img = generate_plate_view(
        #         data = df,
        #         data_type = chosen_type,
        #         taxonomy_level = chosen_level,
        #         color_by = chosen_color
        #     )
                    
        #     # 지금은 테스트용으로 빈 임시 이미지(PNG)를 하나 생성합니다. (나중에 삭제 가능)
        #     dummy_img = Image.new('RGB', (300, 300), color = (73, 109, 137))
        #     d = ImageDraw.Draw(dummy_img)
        #     d.text((120, 190), f"{chosen_type}\n({chosen_color})", fill=(255, 255, 255))
        #     # --------------------------------------------------

        #     # 이미지 다운로드
        #     # 이미지를 파일 형태로 다운로드하기 위해 바이트 스트림(BytesIO)으로 변환
        #     img_buffer = io.BytesIO()
        #     dummy_img.save(img_buffer, format="PNG") # dummy_img는 코드 구현 완료된 후, generated_img로 변경

        #     # 생성된 데이터 세션에 보관
        #     st.session_state.plate_image = dummy_img
        #     st.session_state.plate_bytes = img_buffer.getvalue()
        

        # 지금은 테스트용으로 빈 임시 이미지(PNG)를 하나 생성합니다. (나중에 삭제 가능)
        dummy_img = Image.new('RGB', (300, 300), color = (73, 109, 137))
        d = ImageDraw.Draw(dummy_img)
        d.text((120, 190), f"{chosen_type}\n({chosen_color})", fill=(255, 255, 255))
        # --------------------------------------------------

        # 이미지 다운로드
        # 이미지를 파일 형태로 다운로드하기 위해 바이트 스트림(BytesIO)으로 변환
        img_buffer = io.BytesIO()
        dummy_img.save(img_buffer, format="PNG") # dummy_img는 코드 구현 완료된 후, generated_img로 변경

        # 생성된 데이터 세션에 보관
        st.session_state.plate_image = dummy_img
        st.session_state.plate_bytes = img_buffer.getvalue()

if st.session_state.plate_image is not None:

    st.image(st.session_state.plate_image, caption='Generated Plate Image', use_container_width=True)

    empty_space, download_space = st.columns([2, 1])
        
    # 다운로드 버튼 배치
    with download_space:
        st.download_button(
        label="Download Image (PNG)",
        data=st.session_state.plate_bytes,
        file_name=f"plate_view_{chosen_type}_{chosen_level if chosen_level else ''}_{chosen_color}.png",
        mime="image/png",
        type="secondary",
        use_container_width=True
    )