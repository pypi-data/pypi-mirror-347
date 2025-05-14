from .db import db, ma 

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column("grade_id", db.Integer, primary_key=True)
    grade = db.Column("grade", db.Integer)
    form_group = db.Column("form_group", db.String)
    assignment_id = db.Column("assignment_id", db.Integer, db.ForeignKey('assignments.assignment_id')) #Assignment has student id so dont need that in this table

    def __init__(self, grade, form_group, assignment_id):
        self.grade = grade
        self.form_group = form_group
        self.assignment_id = assignment_id

    def json(self):
        return {
            'id': self.id,
            'grade': self.grade,
            'form_group': self.form_group,
            'assignment_id': self.assignment_id
        }
    
    def __repr__(self):
        return f"Grade({self.id}, {self.grade}, {self.form_group}, {self.assignment_id})"
    
    @classmethod
    def get_grade_by_form_group_and_assignment_id(cls, form_group, assignment_id):
        print("GRADE MODEL: get grade by form group called with form group " + form_group + " and assignment id " + str(assignment_id))
        g = cls.query.filter(cls.form_group == form_group, cls.assignment_id == assignment_id).first()
        if g is not None:
            print("grade returned in get grade by form group and assignment id was " + str(g))
            return g
        else:
            print("No grade found for form group " + form_group + " and assignment id " + str(assignment_id))
            return None
        
    @classmethod
    def get_grade_by_assignment_id(cls, assignment_id):
        print("GRADE MODEL: get grades by assignment ID " + assignment_id)
        grades = cls.query.filter(cls.assignment_id == assignment_id).all()
        if grades is not None:
            print("grades returned in get grades by form group and assignment id was " + str(grades))
            return grades
        else:
            print("No grades found for assignment id " + str(assignment_id))
            return None
    
  
    
class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade
        session = db.session
        load_instance = True