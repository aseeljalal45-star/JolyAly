# mini_ai_smart.py
import pandas as pd
import difflib

class MiniLegalAI:
    def __init__(self, workbook_path=None):
        self.workbook_path = workbook_path
        self.data = None
        if workbook_path:
            try:
                self.data = pd.read_excel(workbook_path, sheet_name=None)
            except Exception:
                self.data = None

    def analyze(self, query: str):
        if not query:
            return "الرجاء إدخال نص أو سؤال قانوني للتحليل."

        if self.data:
            text_bank = []
            for sheet, df in self.data.items():
                for col in df.columns:
                    for val in df[col].astype(str):
                        text_bank.append(val)
            match = difflib.get_close_matches(query, text_bank, n=1, cutoff=0.4)
            if match:
                return f"🔍 أقرب نص قانوني مطابق: {match[0]}"
            else:
                return "لم يتم العثور على مادة مشابهة — جرب صياغة أخرى."
        else:
            keywords = {
                "إجازة": "المادة 61: للعامل الحق في إجازة سنوية مدفوعة الأجر.",
                "مكافأة": "المادة 42: يستحق العامل مكافأة نهاية الخدمة بعد انتهاء عمله.",
                "أجر": "المادة 46: يجب دفع الأجر خلال مدة لا تتجاوز سبعة أيام.",
            }
            for k, v in keywords.items():
                if k in query:
                    return f"📘 استنادًا إلى الكلمة المفتاحية '{k}': {v}"
            return "لم أجد مادة مناسبة — تأكد من وضوح السؤال."
