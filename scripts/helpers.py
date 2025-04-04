# helpers.py
from datetime import datetime
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.app import create_app, db
from src.app.models.document import DocumentPolicy, DocumentSequence

app = create_app()

def get_active_policy():
    """
    En son uygulanan doküman politikasını döner.
    (En son eklenen politika aktif kabul edilir.)
    """
    return DocumentPolicy.query.order_by(DocumentPolicy.applied_at.desc()).first()

def get_next_sequence(originator: str, document_type: str, discipline: str, building_code: str) -> int:
    """
    Verilen kombinasyon için mevcut sıra numarasını döner ve
    tabloyu güncelleyerek sıra numarasını artırır.
    """
    sequence = DocumentSequence.query.filter_by(
        originator=originator,
        document_type=document_type,
        discipline=discipline,
        building_code=building_code
    ).first()

    if sequence is None:
        # Eğer kombinasyon daha önce kullanılmamışsa, yeni bir kayıt oluşturun.
        sequence = DocumentSequence(
            originator=originator,
            document_type=document_type,
            discipline=discipline,
            building_code=building_code,
            next_sequence=2  # İlk atama 1 olarak yapılacak, sonraki 2.
        )
        db.session.add(sequence)
        db.session.commit()
        return 1
    else:
        current = sequence.next_sequence
        sequence.next_sequence += 1
        db.session.commit()
        return current

def generate_document_number(originator: str, document_type: str, discipline: str, building_code: str) -> str:
    """
    Aktif politika bilgilerine ve sıra numarası kaydına göre doküman numarası üretir.
    Proje kodu sabit "SPP2" kabul edilir ve revizyon numarası "R00" ile başlar.
    Numara örneği: [Originator]-SPP2-[DocumentType]-[Discipline]-[BuildingCode]-[SequenceNumber]_R00
    """
    policy = get_active_policy()
    # Eğer politika tanımlı değilse, varsayılan değerlerle çalışalım:
    prefix = policy.prefix if policy and policy.prefix else ""
    date_format = policy.date_format if policy and policy.date_format else "%Y%m%d"
    separator = policy.separator if policy and policy.separator else "-"
    
    # Proje kodu sabit
    project_code = "SPP2"
    # Sıra numarasını alalım (3 haneli, sıfır doldurmalı)
    sequence_num = get_next_sequence(originator, document_type, discipline, building_code)
    sequence_str = f"{sequence_num:03d}"
    # Revizyon numarası başlangıçta R00
    revision = "R00"
    
    # Oluşturulan numarayı birleştirelim:
    document_number = f"{originator}-{project_code}-{document_type}-{discipline}-{building_code}-{sequence_str}_{revision}"
    return document_number
