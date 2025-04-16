import streamlit as st
from processing.law_processor import get_law_list_from_api, get_highlighted_articles

st.set_page_config(page_title="📘 부칙 개정 도우미")
st.title("📘 부칙 개정 도우미")
st.caption("법령 본문 중 검색어를 포함하는 조문을 찾아줍니다.")

# 안전한 상태 초기화
if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False
if "law_details" not in st.session_state:
    st.session_state.law_details = {}
if "triggered_mst" not in st.session_state:
    st.session_state.triggered_mst = None

# 항상 표시되는 입력창
search_word = st.text_input("🔍 찾을 단어", placeholder="예: 지방법원")

col1, col2 = st.columns(2)
with col1:
    if st.button("📄 법률 검색"):
        st.session_state.search_triggered = True
        st.session_state.triggered_mst = None
        st.session_state.law_details = {}
with col2:
    if st.button("🔄 초기화"):
        st.session_state.search_triggered = False
        st.session_state.triggered_mst = None
        st.session_state.law_details = {}
        st.rerun()

# 법률 검색 결과 출력
if st.session_state.search_triggered and search_word:
    with st.spinner("법령 검색 중..."):
        laws = get_law_list_from_api(search_word)
        st.success(f"✅ 총 {len(laws)}개의 법령을 찾았습니다.")
        for idx, law in enumerate(laws, 1):
            mst = law["MST"]
            with st.expander(f"{idx:02d}. {law['법령명']}"):
                st.markdown(f"[🔗 원문 보기]({law['URL']})", unsafe_allow_html=True)
                if st.button(f"📘 조문 보기", key=f"view_{mst}"):
                    st.session_state.triggered_mst = mst
                    st.session_state.law_details[mst] = get_highlighted_articles(mst, search_word)

                # 조문보기 클릭된 경우에만 해당 법률의 조문 표시
                if st.session_state.triggered_mst == mst:
                    st.markdown(st.session_state.law_details[mst], unsafe_allow_html=True)
elif st.session_state.search_triggered and not search_word:
    st.warning("검색어를 입력해주세요.")
