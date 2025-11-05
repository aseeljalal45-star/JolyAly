import json
import os

class SettingsManager:
    def __init__(self, path="helpers/settings.json"):
        self.path = path
        self.settings = self.load_settings()

    def load_settings(self):
        """تحميل الإعدادات من ملف JSON أو إنشاء إعدادات افتراضية عند عدم وجود الملف"""
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️ خطأ في ملف الإعدادات: {e}")
                return self.default_settings()
        else:
            print("⚠️ لم يتم العثور على ملف settings.json، سيتم إنشاء إعدادات افتراضية.")
            return self.default_settings()

    def default_settings(self):
        """إرجاع إعدادات افتراضية في حال عدم وجود الملف"""
        return {
            "APP_NAME": "AlyWork Law Pro",
            "SHEET_URL": "",
            "LANG": "ar",
            "THEME": "light",
            "VERSION": "v25.0"
        }

    def save_settings(self):
        """حفظ الإعدادات إلى ملف JSON"""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

    def get(self, key, default=None):
        """الحصول على قيمة إعداد محدد"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """تعديل أو إضافة إعداد جديد"""
        self.settings[key] = value
        self.save_settings()