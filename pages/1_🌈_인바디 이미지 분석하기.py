import streamlit as st
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re


st.markdown("""
<style>
body {
    background-color: #f4f4f4;
}
.big-font {
    font-size:50px !important;
    color: #5a9;
    text-align: center;
    padding-top: 50px;
}
.file-uploader {
    display: flex;
    justify-content: center;
    padding: 50px;
}
.result-header {
    color: #5a9;
    font-size: 30px;
}
.result-text {
    font-size: 20px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="big-font">
    인바디 사진 분석기
</div>
""", unsafe_allow_html=True)

st.markdown("""
이 애플리케이션은 인바디 사진을 분석하여 체중, 골격근량, 체지방량을 알려줍니다.  
사진을 업로드하면 결과를 확인할 수 있습니다.
""")

uploaded_file = st.file_uploader("인바디 사진을 업로드하세요", type=["jpg", "png"], key="1")

if uploaded_file is not None:
    # 이미지를 OpenCV 이미지로 변환
    img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

    # 이미지를 가로로 3등분하기
    height, width, _ = img.shape
    part_height = height // 3
    img_parts = [img[part_height * i:part_height * (i + 1), :] for i in range(3)]

    # 각 부분에서 소수점 첫째자리까지 표기된 숫자 찾기
    weights, muscles, fats = [], [], []
    for i, img_part in enumerate(img_parts):
        data = pytesseract.image_to_data(img_part, lang='eng', output_type=Output.DICT)
        numbers = [(float(num), data['height'][j]) for j, num in
                   enumerate(re.findall('\d+\.\d', ' '.join(data['text']))) if num]
        if numbers:
            num, _ = max(numbers, key=lambda x: x[1])  # 폰트 크기가 가장 큰 숫자 선택
            if i == 0:
                weights.append(num)
            elif i == 1:
                muscles.append(num)
            else:
                fats.append(num)

    # 각 부분에서 폰트 크기가 가장 큰 숫자를 변수에 저장
    weight = max(weights) if weights else None
    muscle = max(muscles) if muscles else None
    fat = max(fats) if fats else None

    # 결과 출력
    st.markdown("<h2 class='result-header'>결과</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='result-text'>체중: {weight}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='result-text'>골격근량: {muscle}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='result-text'>체지방량: {fat}</p>", unsafe_allow_html=True)

    # 방향성 제공
    if weight and muscle and fat:
        muscle_ratio = muscle / weight * 100
        fat_ratio = fat / weight * 100

        if muscle_ratio > 50:
            st.success("근육량이 많아서 훌륭합니다. 현재의 운동량을 유지하시는 것이 좋겠습니다.")
        else:
            st.warning("근육량이 더 필요합니다. 규칙적인 운동을 통해 근육량을 늘려보세요.")

    # 이미지 출력
    st.markdown("<h2 class='result-header'>분석한 이미지 부분</h2>", unsafe_allow_html=True)
    for i, img_part in enumerate(img_parts):
        st.image(img_part, channels="BGR", use_column_width=True)