import streamlit as st


# 페이지 기본 설정
st.set_page_config(
    page_icon="🐥",
    page_title="스트림릿 배포하기",
    layout="wide",
)

st.subheader("인바디 사진을 첨부하세요")
file = st.file_uploader('이미지를 올려주세요.', type=['jpg', 'png'])

st.subheader("[결과]")