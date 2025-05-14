from .db import db, ma

class Professor(db.Model):
    __tablename__ = "professors"
    
    id = db.Column("prof_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    email = db.Column("email", db.String)
    password = db.Column("password", db.String)
    
    # Relationship
    # case_studies = db.relationship("CaseStudy", back_populates="professor", lazy='dynamic')
    # classes = db.relationship("Class", back_populates="professor", lazy='dynamic')
    
    # classes = db.relationship("Class", backref='prof_id', lazy=True)
    # caseStudies = db.relationship("CaseStudy", backref='professor_id', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def get_password(self):
        return self.password

    # def json(self):
    #     return {'id': self.id, 'name': self.name, 'email': self.email}
    
    def __repr__(self):
        return f"Professor(ID: {self.id}, Name: {self.name}, Email: {self.email})"
    
    def get_id(self):
        return self.id
    
    @classmethod
    def get_professor_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()
    
    @classmethod
    def post_professor(cls, name, email, password):
        professor = cls(name, email, password)
        print(f"in professor model, posting {name} {email} {password}")
        db.session.add(professor)
        db.session.commit()
    
    @classmethod
    def post_professor_email(cls, email):
        professor = cls(None, email, None)
        db.session.add(professor)
        db.session.commit()

    @classmethod
    def update_professor(cls, name, email, password):
        professor = db.session.query(cls).filter(cls.email == email).first()
        professor.name = name
        professor.password = password  
        db.session.commit()

    @classmethod
    def update_password_by_id(cls, id, password):
        student = db.session.query(cls).filter(cls.id == id).first()
        student.password = password
        db.session.commit()

    @classmethod
    def get_professor_id_by_professor_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).first().id
    
    @classmethod
    def get_professor_by_id(cls, id):
        return db.session.query(cls).filter(cls.id == id).first()

class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Professor
        session = db.session
        load_instance = True