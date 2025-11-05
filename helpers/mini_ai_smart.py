import pandas as pd, json, os

class MiniLegalAI:
    def __init__(self, workbook_path, memory_file="logs/ai_memory.json"):
        self.workbook_path = workbook_path
        self.memory_file = memory_file
        self.memory = []
        self.df = None
        self.load_data()
        self.load_memory()

    def load_data(self):
        try:
            self.df = pd.read_excel(self.workbook_path)
        except Exception as e:
            print("⚠️ خطأ في تحميل قاعدة البيانات:", e)
            self.df = pd.DataFrame(columns=["المادة", "الوصف", "الملخص"])

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.memory = json.load(f)

    def save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def remember(self, query, answer):
        self.memory.append({"سؤال": query, "إجابة": answer})
        if len(self.memory) > 25:
            self.memory.pop(0)
        self.save_memory()

    def search_law(self, query):
        if self.df is None or self.df.empty:
            return "⚠️ لا توجد بيانات قانونية حالياً."
        query = query.strip().lower()
        results = self.df[self.df.apply(lambda x: query in str(x).lower(), axis=1)]
        if results.empty:
            answer = "❌ لم يتم العثور على نتيجة مطابقة."
        else:
            top = results.iloc[0]
            answer = f"🔹 المادة {top['المادة']} — {top['الملخص']}"
        self.remember(query, answer)
        return answer