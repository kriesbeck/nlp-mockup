import spacy
import translators as ts
from langdetect import detect
from langcodes import Language
import streamlit as st
import spacy_streamlit


DEFAULT_TEXT = """新华社北京8月3日电 8月3日，中共中央台办发言人受权就依法惩治“台独”顽固分子发表谈话。全文如下：

“台独”分裂是祖国统一的最大障碍，是民族复兴的严重隐患。极少数“台独”顽固分子大肆进行“台独”分裂活动，甘当外部反华势力马前卒，处心积虑制造“两个中国”、“一中一台”、“台湾独立”，其“台独”分裂言行公然挑衅国家主权和领土完整，公然挑衅国家法律尊严，严重危害台海和平稳定，严重损害两岸同胞共同利益和中华民族根本利益，必须依法予以严惩。

国家追究“台独”顽固分子刑事责任具有明确的法律依据。宪法明确规定，台湾是中华人民共和国的神圣领土的一部分。反分裂国家法、国家安全法明确规定，中国的主权和领土完整不容分割，维护国家主权、统一和领土完整是包括台湾同胞在内的全中国人民的共同义务，任何个人和组织不履行法定义务或者从事危害国家安全活动的，依法追究法律责任。刑法明确规定，组织、策划、实施分裂国家、破坏国家统一的，以分裂国家罪定罪处罚；煽动分裂国家、破坏国家统一的，以煽动分裂国家罪定罪处罚；与外国机构、组织、个人相勾结实施上述罪行的，依法从重处罚。

法网恢恢，疏而不漏。凡是以身试法的“台独”顽固分子，我们将采取刑事惩处措施，依法严惩不贷，依法终身追责。任何人、任何势力都不要低估我们捍卫国家主权和领土完整的坚强决心、坚定意志、强大能力。"""


st.title("Text Triage Toolkit")
st.write("\n\n")

input_text = st.text_area("Text to analyze:", DEFAULT_TEXT, height=400)
input_language = detect(input_text)[:2]
input_language_display = Language.make(language=input_language).display_name()
text_en = ts.google(input_text, from_language=input_language, to_language='en')

with st.sidebar:
    st.image("assets/magnifying_glass_icon.png", width=200)
    st.write("Select models:")
    #TODO: Make checkboxes work
    st.checkbox("Translate", value=True)
    st.checkbox("Summarize", value=False)
    st.checkbox("Entities", value=True)
    st.checkbox("Sentiment", value=False)
    st.checkbox("Terminology Extraction", value=False)

col1, col2 = st.columns(2)

#TODO: Summarize
summarize_input = """ """

#TODO: Summarize
summarize_en = """ """

entity_labels = ["PERSON", "DATE", "GPE", "NORP", "FAC", "ORG", "LOC", "PRODUCT", "EVENT", "MONEY"]

with col1:
    # st.write(summarize_input)

    try:
        doc_input = spacy_streamlit.process_text(f"{input_language}_core_web_sm", input_text)
    except:
        try:
            doc_input = spacy_streamlit.process_text(f"{input_language}_core_news_sm", input_text)
        except:
            doc_input = None
            pass
       
    if doc_input:
        spacy_streamlit.visualize_ner(
            doc_input,
            labels=entity_labels,
            show_table=False,
            title=f"{input_language_display} Entities",
            key="input_ner"
        )
    else:
        st.write("No language model available.")

with col2:
    # st.write(summarize_en)
    
    nlp_en = "en_core_web_sm"
    doc_en = spacy_streamlit.process_text(nlp_en, text_en)
    spacy_streamlit.visualize_ner(
        doc_en,
        labels=entity_labels,
        show_table=False,
        title="English entities",
        key="english_ner"
    )

