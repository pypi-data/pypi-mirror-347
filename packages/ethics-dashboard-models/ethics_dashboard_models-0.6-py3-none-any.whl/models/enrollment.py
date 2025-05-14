from .db import db, ma

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    
    id = db.Column("enrollment_id", db.Integer, primary_key=True)
    class_id = db.Column("class_id", db.Integer, db.ForeignKey('classes.class_id'))
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'))

    #relationships
    # classes = db.relationship("Class", back_populates="enrollments", lazy='dynamic')
    # students = db.relationship("Student", back_populates="enrollments", lazy='dynamic')
    
    def __init__(self, class_id, student_id):
        self.class_id = class_id
        self.student_id = student_id

    # def json(self):
    #     return {'id': self.id, 'class_id': self.class_id, 'student_id': self.student_id}
    
    def __repr__(self):
        return f"Enrollment( ID: {self.id}, Class ID: {self.class_id}, Student ID: {self.student_id})"
    
    @classmethod
    def get_enrollments_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).all()
    
    @classmethod
    def enroll_student(cls, class_id, student_id):
        enrollment = cls(class_id, student_id)
        db.session.add(enrollment)
        db.session.commit()
        return enrollment
    
    

class EnrollmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Enrollment
        session = db.session
        load_instance = True