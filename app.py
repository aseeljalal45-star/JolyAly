import streamlit as st
from streamlit_option_menu import option_menu
import os, datetime
import pandas as pd
from helpers.mini_ai_smart import MiniLegalAI
from helpers.settings_manager import SettingsManager
from helpers.ui_components import message_bubble, section_header, info_card
from recommender import smart_recommender
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.express as px

# ==============================
# ⚙️ إعداد الصفحة العامة
# ==============================
st.set_page_config(
    page_title="منصة قانون العمل الأردني الذكية",
    page_icon="⚖️",
    layout="wide"
)

# ==============================
# 🌈 Theme ديناميكي
# ==============================
def load_css(theme="فاتح"):
    css_file = "assets/styles_light.css" if theme=="فاتح" else "assets/styles_dark.css"
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# 📊 تحميل بيانات Google Sheets
# ==============================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aCnqHzxWh8RlIgCleHByoCPHMzI1i5fCjrpizcTxGVc/export?format=csv"

@st.cache_data(ttl=600)
def load_google_sheets(url):
    try:
        with st.spinner("⏳ جاري تحميل البيانات..."):
            df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return pd.DataFrame()

data = load_google_sheets(SHEET_URL)

# ==============================
# 🤖 إعداد المساعد الذكي
# ==============================
workbook_path = os.getenv("WORKBOOK_PATH", "AlyWork_Law_Pro_v2025_v24_ColabStreamlitReady.xlsx")
ai = MiniLegalAI(workbook_path)
settings = SettingsManager()

# ==============================
# 🧠 المساعد القانوني الذكي
# ==============================
def show_ai_assistant():
    section_header("🤖 المساعد القانوني الذكي", "🤖")
    query = st.text_input("💬 اكتب سؤالك هنا:")
    if query:
        answer, reference, example = ai.advanced_search(query)
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({"user": query, "ai": answer})
        for chat in st.session_state.chat_history[-5:]:
            message_bubble("User", chat['user'], is_user=True)
            message_bubble("AI", chat['ai'], is_user=False)
        st.markdown(f"**📜 نص القانون:** {reference}")
        st.markdown(f"**💡 مثال تطبيقي:** {example}")

# ==============================
# 📈 عرض البيانات بشكل تفاعلي
# ==============================
def show_data_table(df):
    if df.empty:
        st.warning("⚠️ لا توجد بيانات للعرض.")
        return
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=True, filter=True)
    grid_options = gb.build()
    AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, height=400)

# ==============================
# 📊 Charts و Metrics
# ==============================
def show_statistics(df):
    st.markdown("### 📊 إحصائيات سريعة")
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد المواد القانونية", len(df))
    col2.metric("عدد التعديلات", df['المادة'].nunique() if 'المادة' in df.columns else 0)
    col3.metric("عدد الأقسام القانونية", df['القسم'].nunique() if 'القسم' in df.columns else 0)

    if 'القسم' in df.columns:
        section_counts = df['القسم'].value_counts()
        fig = px.pie(values=section_counts.values, names=section_counts.index,
                     title="نسبة المواد حسب القسم", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

# ==============================
# 🏠 الصفحة الرئيسية – Grid Cards UI
# ==============================
def show_home():
    st.title("⚖️ منصة قانون العمل الأردني الذكية")
    st.markdown("""
    منصة ذكية لتبسيط وفهم <b>قانون العمل الأردني لعام 1996</b>
    وتعديلاته حتى <b>2024</b>.
    """, unsafe_allow_html=True)
    st.info("⚠️ المنصة لأغراض التوعية القانونية فقط ولا تُغني عن الاستشارة القانونية.")
    st.markdown("---")

    # Grid Cards للأقسام
    sections = [
        {"title":"👷 العمال","desc":"حقوق وواجبات العامل","icon":"person","func":workers_section},
        {"title":"🏢 أصحاب العمل","desc":"حقوق وواجبات صاحب العمل","icon":"building","func":employers_section},
        {"title":"🕵️ مفتشو العمل","desc":"مهام التفتيش القانونية","icon":"shield","func":inspectors_section},
        {"title":"📖 الباحثون والمتدربون","desc":"تحليل، اختبارات واستعراض السوابق","icon":"book","func":researchers_section},
        {"title":"⚙️ الإعدادات","desc":"تخصيص المنصة","icon":"gear","func":settings_page}
    ]

    cols = st.columns(3)
    for i, section in enumerate(sections):
        with cols[i % 3]:
            if st.button(f"{section['icon']} {section['title']}", key=section['title']):
                section['func']()

    show_data_table(data.head(10))
    show_statistics(data)

# ==============================
# 👷 العمال
# ==============================
def workers_section():
    section_header("👷 العمال", "👷")
    info_card("حقوق العامل", "الأجر، الإجازات، مكافأة نهاية الخدمة، بيئة عمل آمنة.")
    info_card("واجبات العامل", "الالتزام بالقوانين الداخلية واحترام النظام.")
    tabs = st.tabs(["مكافأة نهاية الخدمة", "الإجازات", "العمل الإضافي"])
    for tab in tabs:
        with tab:
            st.markdown(f"🛠️ أداة: {tab.title}")
    show_ai_assistant()
    smart_recommender("العمال", n=6)  # ✅ عرض البطاقات المتحركة الآن

# ==============================
# 🏢 أصحاب العمل
# ==============================
def employers_section():
    section_header("🏢 أصحاب العمل", "🏢")
    info_card("حقوق صاحب العمل", "إدارة المنشأة ضمن القانون وتنظيم العقود.")
    info_card("الالتزامات", "دفع الأجور، تطبيق أنظمة السلامة، توثيق العقود.")
    tabs = st.tabs(["تكاليف الموظف", "التزامات الضمان", "الفصل القانوني"])
    for tab in tabs:
        with tab:
            st.markdown(f"🛠️ أداة: {tab.title}")
    show_ai_assistant()
    smart_recommender("اصحاب العمل", n=6)

# ==============================
# 🕵️ مفتشو العمل
# ==============================
def inspectors_section():
    section_header("🕵️ مفتشو العمل", "🕵️")
    info_card("المهام", "مراقبة تطبيق أحكام القانون وضمان العدالة في بيئة العمل.")
    tabs = st.tabs(["دوري", "بناء على شكوى", "طارئ"])
    for tab in tabs:
        with tab:
            st.markdown(f"🛠️ نوع التفتيش: {tab.title}")
    show_ai_assistant()
    smart_recommender("مفتشو العمل", n=6)

# ==============================
# 📖 الباحثون والمتدربون
# ==============================
def researchers_section():
    section_header("📖 الباحثون والمتدربون", "📖")
    tabs = st.tabs(["تحليل التعديلات", "اختبار قانوني", "استعراض السوابق"])
    for tab in tabs:
        with tab:
            st.markdown(f"🛠️ نوع التحليل: {tab.title}")
    show_ai_assistant()
    smart_recommender("الباحثون والمتدربون", n=6)

# ==============================
# ⚙️ الإعدادات
# ==============================
def settings_page():
    section_header("⚙️ الإعدادات", "⚙️")
    theme = st.radio("اختر النمط:", ["فاتح", "غامق"])
    lang = st.selectbox("اختر اللغة:", ["العربية", "English"])
    settings.set("theme", theme)
    settings.set("language", lang)
    load_css(theme)
    st.success("✅ تم حفظ الإعدادات.")

# ==============================
# 🧭 القائمة الجانبية
# ==============================
with st.sidebar:
    choice = option_menu(