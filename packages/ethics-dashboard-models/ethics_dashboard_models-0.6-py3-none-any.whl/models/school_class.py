from .db import db, ma

from .professor import Professor

class Class(db.Model):
    __tablename__ = "classes"
    
    id = db.Column("class_id", db.Integer, primary_key=True)
    class_name = db.Column("class_name", db.String)
    prof_id = db.Column("prof_id", db.Integer, db.ForeignKey('professors.prof_id'))
    class_code = db.Column("class_code", db.String, unique=True)
    
    # Relationships
    # enrollments = db.relationship("Enrollment", backref="class", lazy='dynamic')
    # case_studies = db.relationship("CaseStudy", backref="class", lazy='dynamic')
    
    # caseStudies = db.relationship("CaseStudy", backref='class_id', lazy=True)
    # enrollements = db.relationship("Enrollment", backref='class_id', lazy=True)

    def __init__(self, class_name, prof_id, class_code):
        self.class_name = class_name
        self.prof_id = prof_id
        self.class_code = class_code

    # def json(self):
    #     return {'id': self.id, 'class_name': self.class_name}
    
    def __repr__(self):
        return f"Class(ID: {self.id}, Name: {self.class_name}, Prof ID: {self.prof_id}, Class Code: {self.class_code})"
    
    def get_id(self):
        return self.id
    
    @classmethod
    def get_class_id_by_class_name(cls, class_name):
        return db.session.query(cls).filter(cls.class_name == class_name).first().id
    
    @classmethod
    def post_class(cls, class_name, prof_id, class_code):
        course = cls(class_name, prof_id, class_code)
        db.session.add(course)
        db.session.commit()

    @classmethod
    def get_class_name_by_class_id(cls, class_id):
        return db.session.query(cls).filter(cls.id == class_id).first().class_name
    
    @classmethod
    def get_prof_name_by_class_id(cls, class_id):
        return db.session.query(cls, Professor).join(Professor, cls.prof_id == Professor.id).filter(cls.id == class_id).first().Professor.name

    @classmethod 
    def get_class_id_by_class_name(cls, class_name):
        class1 = db.session.query(cls).filter(cls.class_name == class_name).first()
        print(f"In school_class model: {class1}",flush=True)
        return class1.id 
    
    @classmethod
    def get_class_by_class_code(cls, class_code):
        return db.session.query(cls).filter(cls.class_code == class_code).first()

class ClassSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Class
        session = db.session
        load_instance = True