from datetime import datetime
from .db import db, ma

class FormDescription(db.Model):
    __tablename__ = 'form_descriptions'

    form_description_id = db.Column("form_description_id", db.Integer, primary_key=True, nullable=False)
    case_study_id = db.Column("case_study_id", db.Integer, db.ForeignKey('case_studies.case_study_id'))
    form_id = db.Column("form_id", db.Integer, db.ForeignKey('forms.form_id'))
    description = db.Column("description", db.String)

    def __init__(self, case_study_id, form_id, description):
        self.case_study_id = case_study_id
        self.form_id = form_id
        self.description = description

    def json(self):
        return {
            'form_description_id': self.form_description_id,
            'case_study_id': self.case_study_id,
            'form_id': self.form_id,
            'description': self.description
        }

    def __repr__(self):
        return f"<FormDescription(form_description_id={self.form_description_id}, case_study_id={self.case_study_id}, form_id={self.form_id}, description={self.description})>"
    
    def to_dict(self):
        return {
            'description': self.description
        }
    

    @classmethod
    def post_form_description(cls, case_study_id, form_id, description):
        form_description = cls(case_study_id, form_id, description)
        db.session.add(form_description)
        db.session.commit()

    @classmethod
    def get_form_description_by_case_study_id_and_form_id(cls, case_study_id, form_id):
        return cls.query.filter(cls.case_study_id == case_study_id, cls.form_id == form_id).first()

    @classmethod
    def get_form_description_by_id(cls, form_description_id):
        return cls.query.filter(cls.form_description_id == form_description_id).first()

    @classmethod
    def get_form_descriptions_by_case_study_id(cls, case_study_id):
        return cls.query.filter(cls.case_study_id == case_study_id).all()

    @classmethod
    def get_form_descriptions_by_form_id(cls, form_id):
        return cls.query.filter(cls.form_id == form_id).all()

    @classmethod
    def delete_form_description_by_id(cls, form_description_id):
        cls.query.filter(cls.form_description_id == form_description_id).delete()
        db.session.commit()

    @classmethod
    def delete_form_descriptions_by_case_study_id(cls, case_study_id):
        cls.query.filter(cls.case_study_id == case_study_id).delete()
        db.session.commit()

    @classmethod
    def delete_form_descriptions_by_form_id(cls, form_id):
        cls.query.filter(cls.form_id == form_id).delete()
        db.session.commit()

    @classmethod
    def update_description_by_id(cls, form_description_id, description):
        form_description = cls.query.filter(cls.form_description_id == form_description_id).first()
        if form_description:
            form_description.description = description
            db.session.commit()

class FormDescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FormDescription
        session = db.session
        load_instance = True