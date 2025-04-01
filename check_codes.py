from app import app
from extensions import db
from models import Originator, DocumentType, Discipline, BuildingCode

with app.app_context():
    print("\n🧾 Originator Kayıtları:")
    for item in Originator.query.all():
        print(f"{item.code} - {item.description}")

    print("\n📄 Document Type Kayıtları:")
    for item in DocumentType.query.all():
        print(f"{item.code} - {item.description}")

    print("\n📚 Discipline Kayıtları:")
    for item in Discipline.query.all():
        print(f"{item.code} - {item.description}")

    print("\n🏢 Building Code Kayıtları:")
    for item in BuildingCode.query.all():
        print(f"{item.code} - {item.description}")
