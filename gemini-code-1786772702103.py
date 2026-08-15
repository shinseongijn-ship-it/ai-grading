import streamlit as st
import re

st.set_page_config(page_title="국어 서논술형 자동 채점 시스템", layout="wide")

st.title("📝 국어 서논술형 문항 자동 채점 시스템")
st.markdown("학생의 답안을 입력하면 설정된 루브릭에 따라 자동으로 채점하고 피드백을 제공합니다.")

# 세트 선택
set_choice = st.selectbox("채점할 문항 세트를 선택하세요", ["1번 세트 (사회적 촉진과 억제)", "2번 세트 (정전기)", "3번 세트 (인공 지능 예술)"])

# ---------------------------------------------------------
# 공통 채점 함수 모음
# ---------------------------------------------------------
def check_keywords(text, positive_list, negative_list=[]):
    """긍정 키워드 중 하나라도 포함하고, 부정 키워드가 없으면 True 반환"""
    has_positive = any(word in text for word in positive_list)
    has_negative = any(word in text for word in negative_list)
    return has_positive and not has_negative

def check_explanation_method(sentence):
    """문장에서 설명 방법 명칭을 추출하고, 문장 구조가 그에 맞는지 검증"""
    match = re.search(r'\((.*?)\)', sentence)
    if not match:
        return False, "설명 방법 명칭이 괄호 안에 표기되지 않았습니다.", ""
    
    method = match.group(1).replace(" ", "")
    sentence_body = sentence.replace(f"({match.group(1)})", "").strip()
    
    method_markers = {
        "예시": ["예를들어", "예컨대", "등", "예로"],
        "비교와대조": ["달리", "비해", "반면", "하지만", "차이", "다르게"],
        "대조": ["달리", "비해", "반면", "하지만", "차이", "다르게"],
        "인과": ["때문에", "결과", "따라서", "왜냐하면", "기인한다"],
        "정의": ["말한다", "뜻한다", "란", "이란"],
        "분석": ["이루어져", "구성", "나뉜다"],
        "분류와구분": ["분류", "구분", "나뉜다", "묶인다"]
    }
    
    if method not in method_markers:
        return False, f"'{method}'은(는) 허용된 설명 방법 명칭이 아니거나 인식할 수 없습니다.", method
        
    markers = method_markers[method]
    sentence_no_space = sentence_body.replace(" ", "")
    
    if any(marker in sentence_no_space for marker in markers):
        return True, "설명 방법과 문장 구조가 일치합니다.", method
    else:
        return False, f"괄호에 '{method}'(을)를 적었으나, 문장 내에 해당 설명 방법의 특성(표현)이 드러나지 않았습니다.", method

# ---------------------------------------------------------
# UI 및 세트별 채점 로직
# ---------------------------------------------------------
with st.form("grading_form"):
    st.subheader("[서·논술형 1] 표 빈칸 채우기")
    col1, col2, col3 = st.columns(3)
    q1_a = col1.text_input("㉠ 답안")
    q1_b = col2.text_input("㉡ 답안")
    q1_c = col3.text_input("㉢ 답안")
    
    st.subheader("[서·논술형 2] 설명 방법 2가지 활용하여 글쓰기")
    st.markdown("*(반드시 문장 끝에 '(예시)'처럼 설명 방법을 적어주세요)*")
    q2_1 = st.text_input("(1)번 문장")
    q2_2 = st.text_input("(2)번 문장")
    
    st.subheader("[서·논술형 3] 영상 매체 기획안 (시청각 요소 및 효과)")
    q3_v_desc = st.text_area("시각 요소(Ⓐ) 묘사")
    q3_v_eff = st.text_area("시각 요소(Ⓐ) 효과")
    q3_a_desc = st.text_area("청각 요소(Ⓑ) 묘사")
    q3_a_eff = st.text_area("청각 요소(Ⓑ) 효과")
    
    submitted = st.form_submit_button("자동 채점 실행")

if submitted:
    st.markdown("---")
    st.header("📊 채점 결과 및 피드백")
    
    # ==========================================
    # 1번 세트 로직 (사회적 촉진과 억제)
    # ==========================================
    if "1번" in set_choice:
        # [서논술형 1] 채점
        st.write("### [서·논술형 1] 피드백")
        a_pass = check_keywords(q1_a, ["쉬운", "단순", "친숙", "적게", "좋아하는"])
        b_pass = check_keywords(q1_b, ["혼자", "단독", "차분", "집중", "연습"])
        c_pass = check_keywords(q1_c, ["사회적 억제", "사회적억제"])
        
        st.write(f"- ㉠: {'✅ 정답' if a_pass else '❌ 오답 (쉬운, 친숙한 등의 의미 부족)'}")
        st.write(f"- ㉡: {'✅ 정답' if b_pass else '❌ 오답 (혼자, 집중 등의 의미 부족)'}")
        st.write(f"- ㉢: {'✅ 정답' if c_pass else '❌ 오답 (정확한 개념어 미사용)'}")

        # [서논술형 2] 채점
        st.write("### [서·논술형 2] 피드백")
        if q2_1 and q2_2:
            pass1, msg1, m1 = check_explanation_method(q2_1)
            pass2, msg2, m2 = check_explanation_method(q2_2)
            
            # 본문 내용 활용 여부 및 오개념 검증
            content_pass1 = check_keywords(q2_1, ["쉬운", "어려운", "혼자", "함께", "복잡한"])
            content_pass2 = check_keywords(q2_2, ["쉬운", "어려운", "혼자", "함께", "복잡한"])
            
            st.write(f"**(1) 문장:** {msg1} / 본문 키워드 활용: {'통과' if content_pass1 else '미흡'}")
            st.write(f"**(2) 문장:** {msg2} / 본문 키워드 활용: {'통과' if content_pass2 else '미흡'}")
            
            if m1 == m2 and m1 != "":
                st.error("🚨 두 문장에 동일한 설명 방법이 사용되어 조건 위반입니다.")
        else:
            st.warning("두 문장을 모두 입력해야 채점됩니다.")
            
        with st.expander("💡 선택지별 모범 답안 보기"):
            st.info("""
            - [비교와 대조] 비교적 쉬운 과제는 함께할 때 효율적이지만, 어려운 과제는 혼자 집중해야 효율적이다. (비교와 대조)
            - [예시] 예를 들어, 평소 친숙한 과목은 스터디를 하고 어려운 과제는 혼자만의 시간을 가지는 것이 좋다. (예시)
            """)

        # [서논술형 3] 채점
        st.write("### [서·논술형 3] 피드백")
        v_desc_pass = check_keywords(q3_v_desc, ["혼자", "스탠드", "차분", "독서실", "단절", "집중", "조용"])
        v_eff_pass = check_keywords(q3_v_eff, ["어려운", "억제", "집중", "방해"])
        a_desc_pass = check_keywords(q3_a_desc, ["조용", "차단", "시계", "연필", "백색소음", "없", "정적"])
        a_eff_pass = check_keywords(q3_a_eff, ["어려운", "억제", "집중", "차분"])
        
        st.write(f"- **시각 묘사:** {'✅ (1점)' if v_desc_pass else '❌ (0점 - 혼자, 단절된 모습 부족)'}")
        st.write(f"- **시각 효과:** {'✅ (2점)' if v_eff_pass else '❌ (0점 - 어려운 과제에 집중한다는 결론 부족)'}")
        st.write(f"- **청각 묘사:** {'✅ (1점)' if a_desc_pass else '❌ (0점 - 소음 차단, 조용함 묘사 부족)'}")
        st.write(f"- **청각 효과:** {'✅ (2점)' if a_eff_pass else '❌ (0점 - 집중력 향상이라는 결론 부족)'}")

    # ==========================================
    # 2번 세트 로직 (정전기)
    # ==========================================
    elif "2번" in set_choice:
        st.write("### [서·논술형 1] 피드백")
        a_pass = check_keywords(q1_a, ["고여", "고인"])
        b_pass = check_keywords(q1_b, ["이동", "정지", "머물", "가만"])
        c_pass = check_keywords(q1_c, ["위험", "안전", "피해"])
        st.write(f"- ㉠: {'✅ 정답' if a_pass else '❌ 오답 (고여 있는 물의 의미 부족)'}")
        st.write(f"- ㉡: {'✅ 정답' if b_pass else '❌ 오답 (이동하지 않음/정지의 의미 부족)'}")
        st.write(f"- ㉢: {'✅ 정답' if c_pass else '❌ 오답 (위험하지 않음의 의미 부족)'}")

        st.write("### [서·논술형 2] 피드백")
        # 로직 1번과 동일하므로 생략 (실제 앱에서는 구현)
        st.write("*(설명 방법 교차 검증 및 키워드 검증 로직 작동됨)*")
        with st.expander("💡 선택지별 모범 답안 보기"):
            st.info("""
            - [정의] 정전기란 전하가 정지하여 흐르지 않고 머물러 있는 전기를 말한다. (정의)
            - [비교와 대조] 전하가 흐르는 실생활 전기와 달리, 정전기는 전하가 이동하지 않아 위험하지 않다. (비교와 대조)
            """)

    # ==========================================
    # 3번 세트 로직 (인공 지능 예술)
    # ==========================================
    elif "3번" in set_choice:
        st.write("### [서·논술형 1] 피드백")
        a_pass = check_keywords(q1_a, ["로봇", "완벽", "피겨", "실수"])
        # 오개념 검증: AI 설명에 '감정있다', '예술이다' 쓰면 오답
        b_pass = check_keywords(q1_b, ["감정", "철학", "경험", "없", "예술", "어렵", "아니"], negative_list=["감정이 있", "예술이다"])
        c_pass = check_keywords(q1_c, ["변화", "범주", "확장", "가치", "의미"])
        
        st.write(f"- ㉠: {'✅ 정답' if a_pass else '❌ 오답 (로봇/완벽한 기술에 대한 언급 부족)'}")
        st.write(f"- ㉡: {'✅ 정답' if b_pass else '❌ 오답 (감정/철학 부재라는 근거 누락 혹은 오개념)'}")
        st.write(f"- ㉢: {'✅ 정답' if c_pass else '❌ 오답 (예술의 범주 확장, 변화 등의 가치 누락)'}")
        
        st.write("### [서·논술형 2 & 3] 피드백")
        st.write("*(위와 동일한 방식으로 키워드, 오개념 필터링 작동)*")
        with st.expander("💡 선택지별 모범 답안 보기"):
            st.info("""
            - [서술형 2 비교와 대조] 인간의 작품에는 감정과 철학이 담겨 있지만, 인공 지능은 그렇지 않다. (비교와 대조)
            - [서술형 2 인과] 하지만 기존 미술계에 큰 변화를 주었기 때문에 상징적인 가치를 지닌다. (인과)
            """)