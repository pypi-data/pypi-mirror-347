from .db import db, ma
from .. import Enrollment, Assignment, Submission, Grade, Answer, Feedback

class Student(db.Model):
    __tablename__ = "students"
    
    id = db.Column("student_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    email = db.Column("email", db.String)
    password = db.Column("password", db.String)
    guest = db.Column("guest", db.Boolean, default=False)
    consented = db.Column("consented", db.Boolean, default=False)
    deleted = db.Column("deleted", db.Boolean, default=False)
    
    # Relationship
    # assignments = db.relationship("Assignment", backref="student", lazy=True)
    # enrollments = db.relationship("Enrollment", backref="student", lazy=True)
    
    def __init__(self, name, email, password, guest=False, consented=False):
        self.name = name
        self.email = email
        self.password = password
        self.guest = guest
        self.consented = consented

    def json(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'guest': self.guest, 'consented': self.consented}
    
    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.email}, {self.guest}, {self.consented})"
    
    def set_password(self, hashed_password):
        self.password = hashed_password
        db.session.commit()

    def get_password(self):
        return self.password
    
    def did_consent(self):
        return self.consented
    
    def set_consent(self, consented):
        self.consented = consented
        db.session.commit()

    def is_deleted(self):
        return self.deleted
    
    def set_deleted(self, deleted):
        self.deleted = deleted
        db.session.commit()

    def get_id(self):
        return  self.id
    
    def set_email(self, email):
        self.email = email
        db.session.commit()

    def set_name(self, name):
        self.name = name
        db.session.commit()

    # @classmethod
    # def hard_delete_student(cls, student_id):
    #     student_id = int(student_id)

      

    #     # Manually delete dependent records first
    #     print("hard delete 1", flush=True)
    #     db.session.query(Enrollment).filter(Enrollment.student_id == student_id).delete(synchronize_session=False)
    #     db.session.commit()
    #     print("hard delete 2", flush=True)
    #     db.session.query(Assignment).filter(Assignment.student_id == student_id).delete(synchronize_session=False)
    #     db.session.commit()
    #     print("hard delete 3", flush=True)

    #     db.session.query(cls).filter(cls.id == student_id).delete(synchronize_session=False)
    #     db.session.commit()

    @classmethod
    def hard_delete_student(cls, student_id):
        student_id = int(student_id)

        try:
            print("Getting assignments", flush=True)
            assignment_ids = [a.id for a in db.session.query(Assignment.id).filter(Assignment.student_id == student_id).all()]
            
            if assignment_ids:
                print("Deleting submissions", flush=True)
                db.session.query(Submission).filter(Submission.assignment_id.in_(assignment_ids)).delete(synchronize_session=False)

                print("Deleting feedback", flush=True)
                db.session.query(Feedback).filter(Feedback.assignment_id.in_(assignment_ids)).delete(synchronize_session=False)

                print("Deleting grades", flush=True)
                db.session.query(Grade).filter(Grade.assignment_id.in_(assignment_ids)).delete(synchronize_session=False)

                print("Deleting answers", flush=True)
                db.session.query(Answer).filter(Answer.assignment_id.in_(assignment_ids)).delete(synchronize_session=False)

            print("Deleting enrollments", flush=True)
            db.session.query(Enrollment).filter(Enrollment.student_id == student_id).delete(synchronize_session=False)

            print("Deleting assignments", flush=True)
            db.session.query(Assignment).filter(Assignment.student_id == student_id).delete(synchronize_session=False)

            print("Deleting student", flush=True)
            db.session.query(cls).filter(cls.id == student_id).delete(synchronize_session=False)

            db.session.commit()
            print("Student hard deleted successfully", flush=True)

        except Exception as e:
            db.session.rollback()
            print("Error during hard delete:", e, flush=True)


    @classmethod
    def soft_delete_student(cls, student_id):
        print("soft delete 1", flush=True)

        student = db.session.query(cls).filter(cls.id == student_id).first()
        if student:
            student.set_deleted(True)
            student.set_email(None)
            student.set_name(None)
        db.session.commit()
    
    @classmethod
    def get_students(cls):
        return cls.query.all()
    
    @classmethod
    def get_student_by_email(cls, email):
        return cls.query.filter(cls.email==email).first()
    
    @classmethod 
    def get_student_id_by_email(cls, email):
        return db.session.query(cls).filter(cls.email == email).first().id
    
    @classmethod
    def get_student_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def post_student(cls, name, email, password, guest):
        student = cls(name, email, password, guest)
        db.session.add(student)
        db.session.commit()

    @classmethod
    def post_student_email(cls, email):
        student = cls(None, email, None, None)
        db.session.add(student)
        db.session.commit()

    @classmethod
    def update_student(cls, name, email, password, guest, consented):
        student = db.session.query(cls).filter(cls.email == email).first()
        student.name = name
        student.password = password 
        student.guest = guest 
        student.consented = consented
        db.session.commit()

    @classmethod 
    def delete_student_by_id(cls, id):
        db.session.query(cls).filter(cls.id == id).delete()
        db.session.commit()

    @classmethod 
    def delete_student_by_email(cls, email):
        db.session.query(cls).filter(cls.email == email).delete()
        db.session.commit()

    @classmethod
    def get_all_guests(cls):
        return db.session.query(cls).filter(cls.guest == True).all()
    
    @classmethod
    def delete_all_guests(cls):
        db.session.query(cls).filter(cls.guest == True).delete()
        db.session.commit()

    @classmethod
    def get_all_guest_ids(cls):
        guests = db.session.query(cls).filter(cls.guest == True).all()
        ids = [guest.id for guest in guests]
        return ids 
    
    
class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        session = db.session
        load_instance = True