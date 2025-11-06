import streamlit as st
from streamlit_option_menu import option_menu
import os, datetime
import pandas as pd
from helpers.mini_ai_smart import MiniLegalAI
from helpers.settings_manager import SettingsManager
from helpers.ui_components import message_bubble, section_header, info_card
from recommender import smart_recommender

# ==============================
# ⚙️ إعداد الصفحة العامة
# ==============================
st.set_page_config(page_title="منصة قانون العمل الأردني الذكية", page_icon="⚖️", layout="wide")

# تحميل ملف التنسيق العام
with open("assets/styles.css", "r", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ==============================
# 📊 ربط قاعدة بيانات Google Sheets
# ==============================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aCnqHzxWh8RlIgCleHByoCPHMzI1i5fCjrpizcTxGVc/export?format=csv"

@st.cache_data(ttl=600)
def load_google_sheets(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات من Google Sheets: {e}")
        return pd.DataFrame()

data = load_google_sheets(SHEET_URL)
if not data.empty:
    st.sidebar.success("✅ تم الاتصال بقاعدة بيانات Google Sheets بنجاح")
else:
    st.sidebar.warning("⚠️ لم يتم تحميل البيانات، تأكد من صلاحيات الرابط.")

# ==============================
# 🤖 إعداد المساعد الذكي
# ==============================
workbook_path = os.getenv("WORKBOOK_PATH", "AlyWork_Law_Pro_v2025_v24_ColabStreamlitReady.xlsx")
ai = MiniLegalAI(workbook_path)
settings = SettingsManager()

# ==============================
# 🧠 المساعد القانوني
# ==============================
def show_ai_assistant():
    section_header("🤖 المساعد القانوني الذكي", "🤖")
    st.markdown("💬 اكتب سؤالك حول قانون العمل الأردني:")
    query = st.text_input("✍️ سؤالك هنا:")
    if query:
        answer = ai.search_law(query)
        message_bubble("User", query, is_user=True)
        message_bubble("AI", answer, is_user=False)

# ==============================
# 🏠 الصفحة الرئيسية
# ==============================
def show_home():
    st.title("⚖️ منصة قانون العمل الأردني الذكية")
    st.markdown("""
    <div style='font-size:18px;'>
    منصة ذكية لتبسيط وفهم <b>قانون العمل الأردني لعام 1996</b> وتعديلاته حتى <b>2024</b>.
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ المنصة لأغراض التوعية القانونية فقط ولا تُغني عن الاستشارة القانونية.")
    st.markdown("---")

    if not data.empty:
        st.subheader("📂 نظرة سريعة على البيانات (من Google Sheets)")
        st.dataframe(data.head(10))
    else:
        st.warning("⚠️ لا توجد بيانات متاحة حاليًا من Google Sheets.")

# ==============================
# 👷 العمال
# ==============================
def workers_section():
    section_header("👷 العمال", "👷")
    info_card("حقوق العامل", "الأجر، الإجازات، مكافأة نهاية الخدمة، بيئة عمل آمنة.")
    info_card("واجبات العامل", "الالتزام بالقوانين الداخلية واحترام النظام.")
    st.selectbox("اختر حاسبة:", ["مكافأة نهاية الخدمة", "الإجازات", "العمل الإضافي"])
    show_ai_assistant()
    smart_recommender("العمال", n=4)

# ==============================
# 🏢 أصحاب العمل
# ==============================
def employers_section():
    section_header("🏢 أصحاب العمل", "🏢")
    info_card("حقوق صاحب العمل", "إدارة المنشأة ضمن القانون وتنظيم العقود.")
    info_card("الالتزامات", "دفع الأجور، تطبيق أنظمة السلامة، توثيق العقود.")
    st.selectbox("اختر أداة:", ["تكاليف الموظف", "التزامات الضمان", "الفصل القانوني"])
    show_ai_assistant()
    smart_recommender("اصحاب العمل", n=4)

# ==============================
# 🕵️ مفتشو العمل
# ==============================
def inspectors_section():
    section_header("🕵️ مفتشو العمل", "🕵️")
    info_card("المهام", "مراقبة تطبيق أحكام القانون وضمان العدالة في بيئة العمل.")
    st.selectbox("نوع التفتيش:", ["دوري", "بناء على شكوى", "طارئ"])
    show_ai_assistant()
    smart_recommender("مفتشو العمل", n=3)

# ==============================
# 📖 الباحثون والمتدربون
# ==============================
def researchers_section():
    section_header("📖 الباحثون والمتدربون", "📖")
    st.selectbox("اختر نوع التحليل:", ["تحليل التعديلات", "اختبار قانوني", "استعراض السوابق"])
    show_ai_assistant()
    smart_recommender("الباحثون والمتدربون", n=3)

# ==============================
# ⚙️ الإعدادات
# ==============================
def settings_page():
    section_header("⚙️ الإعدادات", "⚙️")
    theme = st.radio("اختر النمط:", ["فاتح", "غامق"])
    lang = st.selectbox("اختر اللغة:", ["العربية", "English"])
    settings.set("theme", theme)
    settings.set("language", lang)
    st.success("✅ تم حفظ الإعدادات.")

# ==============================
# 🧭 القائمة الجانبية والتنقل
# ==============================
with st.sidebar:
    choice = option_menu(
        "القائمة الرئيسية",
        ["🏠 الصفحة الرئيسية", "👷 العمال", "🏢 أصحاب العمل", "🕵️ مفتشو العمل", "📖 الباحثون والمتدربون", "⚙️ الإعدادات"],
        icons=["house", "person", "building", "shield", "book", "gear"],
        default_index=0
    )

if choice == "🏠 الصفحة الرئيسية":
    show_home()
elif choice == "👷 العمال":
    workers_section()
elif choice == "🏢 أصحاب العمل":
    employers_section()
elif choice == "🕵️ مفتشو العمل":
    inspectors_section()
elif choice == "📖 الباحثون والمتدربون":
    researchers_section()
elif choice == "⚙️ الإعدادات":
    settings_page()

# ==============================
# ⏰ تذييل الصفحة
# ==============================
st.markdown(f"<hr><center><small>© {datetime.datetime.now().year} AlyWork Law Pro — جميع الحقوق محفوظة.</small></center>", unsafe_allow_html=True)