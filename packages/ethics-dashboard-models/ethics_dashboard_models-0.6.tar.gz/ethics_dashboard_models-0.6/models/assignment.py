from datetime import datetime
from .db import db, ma
from .case_study import CaseStudy

class Assignment(db.Model):
    __tablename__ = "assignments"
    
    id = db.Column("assignment_id", db.Integer, primary_key=True)
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'))
    case_study_id = db.Column("case_study_id", db.Integer, db.ForeignKey('case_studies.case_study_id'))
    case_study_option_id = db.Column("case_study_option_id", db.Integer, db.ForeignKey("case_study_options.case_study_option_id"), nullable=True)
    submitted = db.Column("submitted", db.Boolean)
    graded = db.Column("graded", db.Boolean)
    last_modified = db.Column("last_modified", db.TIMESTAMP)


    # Relationships
    # answers = db.relationship("Answer", backref="assignment", lazy=True)
    # feedbacks = db.relationship("Feedback", backref="assignment", lazy=True)
    
    def __init__(self, student_id, case_study_id, case_study_option_id, submitted, graded, last_modified):
        self.student_id = student_id
        self.case_study_id = case_study_id
        self.case_study_option_id = case_study_option_id
        self.submitted = submitted
        self.graded = graded
        self.last_modified = last_modified

    def json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'case_study_id': self.case_study_id,
            'case_study_option_id': self.case_study_option_id,
            'submitted': self.submitted,
            'graded': self.graded,
            'last_modified': self.last_modified
        }
    
    
    def __repr__(self):
        return f"Assignment(ID: {self.id}, Student ID: {self.student_id}, Case study ID: {self.case_study_id})"
    
    def set_last_modified(self, last_modified):
        self.last_modified = last_modified

    def get_id(self):
        return self.id
    
    def set_submitted(self, boolean):
        self.submitted = boolean
        db.session.commit()

    @classmethod
    def post_assignment(cls, student_id, case_study_id, case_study_option_id=None):
        assignment = cls(student_id, case_study_id, case_study_option_id, False, False, datetime.now())
        db.session.add(assignment)
        db.session.commit()
    
    @classmethod
    def get_assignment_by_casestudy_and_student(cls, student_id, case_study_id):
        return cls.query.filter(cls.student_id == student_id, cls.case_study_id == case_study_id).first()
    
 
    @classmethod
    def get_assignment_by_student(cls, student_id, assignment_id):
        return cls.query.filter(cls.student_id == student_id, cls.id == assignment_id).first()
        #return db.session.query(Assignment).filter(Assignment.student_id == student_id, Assignment.id == assignment_id).all()

    @classmethod
    def get_all_assignments_by_student(cls, student_id):
        assignments = (
            db.session.query(cls, CaseStudy.title)
            .join(CaseStudy, cls.case_study_id == CaseStudy.id)
            .filter(cls.student_id == student_id)
            .order_by(cls.last_modified.desc())
            .all()
        )
        print(f'from assignment model: {assignments}',flush=True)
        return assignments
    
    @classmethod
    def get_all_assignments_by_student_and_class(cls, student_id, class_id):
        return (
            db.session.query(cls, CaseStudy.title)
            .join(CaseStudy, cls.case_study_id == CaseStudy.id)
            .filter(cls.student_id == student_id, CaseStudy.class_id == class_id)
            .order_by(cls.last_modified.desc())
            .all()
        )
        #return db.session.query(cls).filter(cls.student_id == student_id and cls.
    
    @classmethod 
    def get_all_assignment_ids_by_student_id(cls, student_id):
        assignments = db.session.query(cls).filter(cls.student_id == student_id).all()
        ids = [assignment.id for assignment in assignments]
        return ids

    @classmethod
    def get_assignment_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def delete_assignment_by_id(cls, id):
        db.session.query(cls).filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_assignments_by_student_id(cls, student_id):
        db.session.query(cls).filter(cls.student_id == student_id).delete()
        db.session.commit()

    @classmethod
    def set_last_modified_by_id(cls, assignment_id, last_modified):
        assignment = db.session.query(cls).filter(cls.id == assignment_id).first()
        assignment.last_modified = last_modified
        db.session.commit()
        

    @classmethod
    def set_case_study_option_by_id(cls, assignment_id, case_study_option):
        assignment = db.session.query(cls).filter(cls.id == assignment_id).first()
        assignment.case_study_option_id = case_study_option
        db.session.commit()

    
class AssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        session = db.session
        load_instance = True
