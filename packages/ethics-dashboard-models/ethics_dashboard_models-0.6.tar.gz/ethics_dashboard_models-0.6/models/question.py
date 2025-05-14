from .db import db, ma


class Question(db.Model):
    __tablename__ = "dynamic_questions"
    
    id = db.Column("dynamic_question_id", db.Integer, primary_key=True)
    case_study_id = db.Column("case_study_id", db.Integer, db.ForeignKey('case_studies.case_study_id'))
    form_id = db.Column("form_id", db.Integer, db.ForeignKey('forms.form_id'))
    question_text = db.Column("question_text", db.String)
  
    #relationships
    # case_studies = db.relationship("CaseStudy", back_populates='questions', lazy='dynamic')
    # answers = db.relationship("Answer", back_populates='questions', lazy='dynamic')
    # template = db.relationship("Template", back_populates='question', lazy='dynamic')

    # answers = db.relationship("Answer", backref='question_id', lazy=True)
    
    def __init__(self, case_study_id, form_id, content):
        self.case_study_id = case_study_id
        self.form_id = form_id
        self.question_text = content       

    # def json(self):
    #     return {'id': self.id, 'content': self.content}
    
    def __repr__(self):
        return f"Question({self.id}, Form id: {self.form_id}, {self.question_text})"
    
    def json(self):
        return {'id': self.id, 'case_study_id': self.case_study_id, 'form_id': self.form_id, 'question_text': self.question_text}
    

    @classmethod
    def get_total_questions_by_form_id_and_case_study_id(cls, form_id, case_study_id):
        return cls.query.filter(cls.form_id == form_id, cls.case_study_id == case_study_id).count()

    @classmethod
    def get_question_by_id(cls, idd):
        return cls.query.filter(cls.id == idd).first()
    
    @classmethod
    def get_questions_by_case_study_id(cls, case_study_id):
        return cls.query.filter(cls.case_study_id == case_study_id).all()
    
    @classmethod
    def get_questions_by_case_study_id_and_form_id(cls, case_study_id, form_id):
        return cls.query.filter(cls.case_study_id == case_study_id, cls.form_id == form_id).all()
    
    @classmethod
    def delete_question_by_id(cls, id):
        cls.query.filter(cls.id==id).delete()

    @classmethod
    def delete_question_by_case_study_id_and_question_text(cls, case_study_id, question_text):
        cls.query.filter(cls.case_study_id==case_study_id, cls.question_text==question_text).delete()

    @classmethod
    def modify_question_by_case_study_id_and_question_text(cls, case_study_id, question_text):
       question = cls.query.filter(cls.case_study_id==case_study_id, cls.question_text==question_text)
       question.question_text = question_text
       db.session.commit()

    @classmethod 
    def post_question_by_case_study_id_and_form_id(cls, case_study_id, form_id, question_text):
        question = cls(case_study_id, form_id, question_text)
        db.session.add(question)
        db.session.commit()


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        session = db.session
        load_instance = True