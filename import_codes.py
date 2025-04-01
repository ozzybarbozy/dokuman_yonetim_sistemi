import os
import pandas as pd
from app import app
from extensions import db
from models import Originator, DocumentType, Discipline, BuildingCode

# .xlsx dosya yolları
files = {
    'originator': 'originator.xlsx',
    'document_type': 'document_type.xlsx',
    'discipline': 'discipline.xlsx',
    'building_code': 'building_code.xlsx'
}

def import_data():
    with app.app_context():
        for key, filepath in files.items():
            if not os.path.exists(filepath):
                print(f"Dosya bulunamadı: {filepath}")
                continue

            df = pd.read_excel(filepath)

            for _, row in df.iterrows():
                code = str(row.get("code", "")).strip()
                description = str(row.get("description", "")).strip()

                if not code:
                    continue

                model = {
                    'originator': Originator,
                    'document_type': DocumentType,
                    'discipline': Discipline,
                    'building_code': BuildingCode
                }.get(key)

                if not model:
                    continue

                existing = model.query.filter_by(code=code).first()
                if existing:
                    print(f"{key.upper()} zaten var: {code}")
                    continue

                new_item = model(code=code, description=description)
                db.session.add(new_item)
                print(f"{key.upper()} eklendi: {code}")

        db.session.commit()
        print("✔️ Kodlar başarıyla içe aktarıldı.")

if __name__ == "__main__":
    import_data()
