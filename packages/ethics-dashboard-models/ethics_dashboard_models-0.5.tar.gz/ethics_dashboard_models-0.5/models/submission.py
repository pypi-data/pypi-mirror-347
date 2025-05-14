from .db import db, ma


class Submission(db.Model):
    __tablename__ = "submissions"
    
    id = db.Column("submission_id", db.Integer, primary_key=True)
    assignment_id = db.Column("assignment_id", db.Integer, db.ForeignKey("assignments.assignment_id", ondelete='CASCADE'))
    student_id = db.Column("student_id", db.Integer, db.ForeignKey("students.student_id"))
    #student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    #lastModified = db.Column("last_modified", db.Date)
    form_id = db.Column("form_id", db.Integer, db.ForeignKey("forms.form_id"))
    submitted_time = db.Column("submitted_time", db.TIMESTAMP)
    
    
    def __init__(self, assignment_id, form_id, submitted_time, student_id):
        self.assignment_id = assignment_id
        self.form_id = form_id
        self.submitted_time = submitted_time
        self.student_id = student_id

    def __repr__(self):
        return f"ID: {self.id} // Assignment ID: {self.assignment_id} // Form ID: {self.form_id} // Submitted: {self.submitted_time} // Student ID: {self.student_id}"
    
    def json(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'form_id': self.form_id,
            'submitted_time': self.submitted_time,
            'student_id': self.student_id,
        }
    
    def get_id(self):
        return self.id
    
    @classmethod
    def get_submission_by_id(cls, id):
        return db.session.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_submissions_by_assignment_id(cls, assignment_id):
        # db.session.query(cls).filter(cls.email == email).delete()
        return db.session.query(cls).filter(cls.assignment_id == assignment_id).all()
    
    @classmethod
    def get_submissions_by_assignment_id_and_form_id(cls, assignment_id, form_id):
        return db.session.query(cls).filter(cls.assignment_id == assignment_id, cls.form_id == form_id).all()
    
    @classmethod
    def is_assignment_submitted(cls, assignment_id, number_of_forms):
        #query for number of rows in submission table with this assignment id
        count = db.session.query(cls).filter(cls.assignment_id == assignment_id).count()
        #if the number of rows is less than the number of forms, return false 
        #there is 1 form which doesn't count as a submission (action and duty form)
        print("Count of forms submitted for this assignment is " + str(count) + " and number of forms is " + str(number_of_forms), flush=True)

        #print all rows for this assignment id
        rows = db.session.query(cls).filter(cls.assignment_id == assignment_id).all()
        for row in rows:
            print("Row: " + str(row), flush=True)

        if count < number_of_forms-1:
           
            return False
        else:
            return True
    
    @classmethod
    def get_submissions_by_assignment_id_form_id_and_student_id(cls, assignment_id, form_id, student_id):
        return db.session.query(cls).filter(cls.assignment_id == assignment_id, cls.form_id == form_id, cls.student_id == student_id).all()
    
    @classmethod
    def post_submission(cls, assignment_id, form_id, submitted_time, student_id):
        new_submission = cls(assignment_id, form_id, submitted_time, student_id)
        db.session.add(new_submission)
        db.session.commit()

    @classmethod
    def delete_submission_by_id(cls, id):
        db.session.query(cls).filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_submissions_by_assignment_id(cls, assignment_id):
        db.session.query(cls).filter(cls.assignment_id == assignment_id).delete()
        db.session.commit()

    @classmethod
    def delete_submissions_by_assignment_id_and_form_id(cls, assignment_id, form_id):
        db.session.query(cls).filter(cls.assignment_id == assignment_id, cls.form_id == form_id).delete()
        db.session.commit()

    @classmethod
    def delete_submissions_by_assignment_id_form_id_and_student_id(cls, assignment_id, form_id, student_id):
        db.session.query(cls).filter(cls.assignment_id == assignment_id, cls.form_id == form_id, cls.student_id == student_id).delete()
        db.session.commit()

    @classmethod
    def delete_all_submissions_by_student_id(cls, student_id):
        db.session.query(cls).filter(cls.student_id == student_id).delete()
        db.session.commit()


class SubmissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Submission
        session = db.session
        load_instance = True