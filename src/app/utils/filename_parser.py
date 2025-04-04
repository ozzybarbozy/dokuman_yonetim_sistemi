import re
from ..models.settings import Originator, DocumentType, Discipline, BuildingCode

def parse_and_validate_filename(base_name):
    pattern = r'^([A-Z]{3})-SPP2-([A-Z]{3})-([A-Z]{2})-([A-Z0-9]+)-(\d{3})_R(\d{2})$'
    match = re.match(pattern, base_name)
    
    if not match:
        return None

    originator_code, doc_type_code, discipline_code, building_code, seq, rev = match.groups()

    # Kodlar veritabanında var mı kontrolü
    if not all([
        Originator.query.filter_by(code=originator_code).first(),
        DocumentType.query.filter_by(code=doc_type_code).first(),
        Discipline.query.filter_by(code=discipline_code).first(),
        BuildingCode.query.filter_by(code=building_code).first()
    ]):
        return None

    return {
        'originator': originator_code,
        'document_type': doc_type_code,
        'discipline': discipline_code,
        'building_code': building_code,
        'sequence': seq,
        'revision': int(rev)
    }
