import pandas as pd
import os
from difflib import get_close_matches

class MiniLegalAI:
    """
    🔹 مساعد قانوني ذكي متقدم
    🔹 يدعم البحث شبه الذكي، اقتراح المواد القانونية، والأمثلة التطبيقية
    🔹 يعمل مع قاعدة البيانات السابقة (Excel)
    """

    def __init__(self, workbook_path="AlyWork_Law_Pro_v2025_v24_ColabStreamlitReady.xlsx"):
        self.workbook_path = workbook_path
        self.data = self.load_workbook(workbook_path)

    def load_workbook(self, path):
        """تحميل بيانات Excel كاملة."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"الملف غير موجود: {path}")
        try:
            xls = pd.ExcelFile(path)
            if "مواد_القانون" in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name="مواد_القانون")
            else:
                df = pd.read_excel(xls, sheet_name=0)
            df.fillna("", inplace=True)
            return df
        except Exception as e:
            raise ValueError(f"خطأ أثناء تحميل ملف Excel: {e}")

    def advanced_search(self, query, section=None, max_results=3):
        """
        البحث الذكي شبه الاصطناعي:
        🔹 query: نص المستخدم
        🔹 section: فلترة حسب القسم
        🔹 max_results: عدد النتائج
        """
        if self.data.empty:
            return "لا توجد بيانات", "", ""

        df = self.data.copy()
        if section and "القسم" in df.columns:
            df = df[df["القسم"].str.contains(section, case=False, na=False)]

        # البحث النصي الأساسي
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        # إذا لم توجد نتائج مباشرة، استخدم التطابق الذكي
        if results.empty and "نص_القانون" in df.columns:
            all_texts = df["نص_القانون"].tolist()
            matches = get_close_matches(query, all_texts, n=max_results, cutoff=0.4)
            results = df[df["نص_القانون"].isin(matches)]

        if results.empty:
            return "لا توجد نتائج مطابقة للبحث.", "", ""

        first_result = results.iloc[0]
        law_text = first_result.get("نص_القانون", "")
        reference = first_result.get("المادة", "")
        example = first_result.get("مثال_تطبيقي", "")

        return law_text, reference, example

    def suggest_related_materials(self, query, n=3):
        """
        🔹 اقتراح مواد قانونية مشابهة للموضوع
        """
        if self.data.empty or "نص_القانون" not in self.data.columns:
            return []

        all_texts = self.data["نص_القانون"].tolist()
        matches = get_close_matches(query, all_texts, n=n, cutoff=0.3)

        suggestions = []
        for match in matches:
            row = self.data[self.data["نص_القانون"] == match].iloc[0]
            suggestions.append({
                "المادة": row.get("المادة", ""),
                "القسم": row.get("القسم", ""),
                "نص_القانون": row.get("نص_القانون", ""),
                "مثال_تطبيقي": row.get("مثال_تطبيقي", "")
            })
        return suggestions

    def get_sections(self):
        """إرجاع جميع الأقسام القانونية المتاحة"""
        if "القسم" in self.data.columns:
            return self.data["القسم"].dropna().unique().tolist()
        return []

    def get_materials_by_section(self, section):
        """إرجاع جميع المواد داخل قسم محدد"""
        if "القسم" not in self.data.columns:
            return pd.DataFrame()
        return self.data[self.data["القسم"].str.contains(section, case=False, na=False)]

# ========== مثال للاستخدام ==========
if __name__ == "__main__":
    ai = MiniLegalAI()
    query = "إجازة سنوية"
    print("نتيجة البحث:", ai.advanced_search(query))
    print("اقتراح مواد ذات صلة:", ai.suggest_related_materials(query))
    print("الأقسام المتاحة:", ai.get_sections())