from .db import db, ma

class CaseStudy(db.Model):
    __tablename__ = "case_studies"
    
    id = db.Column("case_study_id", db.Integer, primary_key=True)
    professor_id = db.Column("prof_id", db.Integer, db.ForeignKey('professors.prof_id'), nullable=True)
    ta_id = db.Column("ta_id", db.Integer, db.ForeignKey('tas.ta_id'), nullable=True)
    class_id = db.Column("class_id", db.Integer, db.ForeignKey('classes.class_id'), nullable=True)
    title = db.Column("title", db.String)
    last_modified = db.Column("last_modified", db.Date)
    
    # Relationships
    # questions = db.relationship("Question", back_populates="case_study", lazy='dynamic')
    # professor = db.relationship("Professor", back_populates="case_studies", lazy='dynamic')
    # assignments = db.relationship("Assignment", back_populates="case_study", lazy='dynamic')
    # course = db.relationship("Class", back_populates="case_studies", lazy='dynamic') 
    
    # assignments = db.relationship('Assignment', backref='case_study_id', lazy=True)
    # questions = db.relationship('Question', backref='case_study_id', lazy=True)

    def __init__(self, professor_id, class_id, title, last_modified):
        self.professor_id = professor_id
        self.class_id = class_id
        self.title = title
        self.last_modified = last_modified

    # def json(self):
    #     return {'id': self.id, 'title': self.title, 'last_modified': self.last_modified}
    
    def __repr__(self):
        return f"CaseStudy({self.id}, {self.title})"
    
    def get_id(self):
        return self.id
    
    @classmethod
    def post_case_study(cls, professor_id, class_id, title, last_modified):
        case_study = cls(professor_id, class_id, title, last_modified)
        db.session.add(case_study)
        db.session.commit()

    @classmethod 
    def get_case_study_by_title(cls, title):
        return db.session.query(cls).filter(cls.title == title).first()
    
class CaseStudySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaseStudy
        session = db.session
        load_instance = True