from .db import db, ma

class TA(db.Model):
    __tablename__ = "tas"
    
    id = db.Column("ta_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    email = db.Column("email", db.String)
    password = db.Column("password", db.String)
    
    # Relationship
    # case_studies = db.relationship("CaseStudy", back_populates="ta", lazy='dynamic')
    
    # caseStudies = db.relationship("CaseStudy", backref='ta_id', lazy=True)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    # def json(self):
    #     return {'id': self.id, 'name': self.name, 'email': self.email}
    
    def __repr__(self):
        return f"TA({self.id}, {self.name}, {self.email})"
    
    def get_password(self):
        return self.password
    
    @classmethod
    def get_ta_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()
    
    @classmethod 
    def post_ta_email(cls, email):
        ta = cls(None, email, None)
        db.session.add(ta)
        db.session.commit()
        
    @classmethod
    def post_ta(cls, name, email, password):
        ta = cls(name, email, password)
        db.session.add(ta)
        db.session.commit()

    @classmethod 
    def update_ta(cls, name, email, password):
        ta = db.session.query(cls).filter(cls.email == email).first()
        ta.name = name
        ta.password = password
        db.session.commit()
    
class TASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TA
        session = db.session
        load_instance = True