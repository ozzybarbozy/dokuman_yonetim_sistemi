from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class DocumentUploadForm(FlaskForm):
    file = FileField('Document File', validators=[FileRequired()])
    originator = SelectField('Originator', validators=[DataRequired()], choices=[
        ('', 'Select Originator'),
        ('KLN', 'KLN'),
        ('SPP', 'SPP'),
        ('SUB', 'SUB')
    ])
    document_type = SelectField('Document Type', validators=[DataRequired()], choices=[
        ('', 'Select Type'),
        ('ITP', 'ITP'),
        ('DRW', 'DRW'),
        ('SPC', 'SPC'),
        ('CAL', 'CAL')
    ])
    discipline = SelectField('Discipline', validators=[DataRequired()], choices=[
        ('', 'Select Discipline'),
        ('CV', 'CV'),
        ('EL', 'EL'),
        ('ME', 'ME'),
        ('PL', 'PL')
    ])
    building_code = SelectField('Building Code', validators=[DataRequired()], choices=[
        ('', 'Select Building'),
        ('ES01', 'ES01'),
        ('ES02', 'ES02'),
        ('ES03', 'ES03')
    ])
    description = TextAreaField('Description')
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('', 'Select Category'),
        ('IFR', 'IFR'),
        ('OFR', 'OFR'),
        ('MFR', 'MFR')
    ])
    project_code = StringField('Project Code', validators=[DataRequired()]) 