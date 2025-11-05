import pandas as pd

def load_data(source_path):
    try:
        if source_path.startswith("http"):
            return pd.read_csv(source_path)
        if source_path.endswith(".xlsx"):
            return pd.read_excel(source_path)
        if source_path.endswith(".csv"):
            return pd.read_csv(source_path)
        raise ValueError("صيغة غير مدعومة.")
    except Exception as e:
        print("خطأ:", e)
        return pd.DataFrame()