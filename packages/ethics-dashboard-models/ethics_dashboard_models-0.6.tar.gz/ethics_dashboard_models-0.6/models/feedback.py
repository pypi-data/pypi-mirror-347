from .db import db, ma
from ..ethics_dashboard_models import Answer
from ..ethics_dashboard_models.form import Form

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    
    id = db.Column("feedback_id", db.Integer, primary_key=True)
    assignment_id = db.Column("assignment_id", db.Integer, db.ForeignKey('assignments.assignment_id', ondelete='CASCADE'))

    #Either answer_id is populated, or form_id and section_key are populated, or just form_id is populated
    answer_id = db.Column("answer_id", db.Integer, db.ForeignKey('answers.answer_id')) #for feedback associated with a single answer (only answer id populated)
    form_id = db.Column("form_id", db.Integer, db.ForeignKey('forms.form_id')) #for feedback associated with a whole form (only form id populated)
    section_key = db.Column("section_key", db.String) #for feedback associated with a section of a form (form id and section key populated)

    content = db.Column("content", db.String)
    last_modified = db.Column("last_modified", db.Date)

    #relationships
    # assignments = db.relationship("Assignment", back_populates='feedbacks')
    
    def __init__(self, assignment_id, content, last_modified):
        self.assignment_id = assignment_id
        self.content = content
        self.last_modified = last_modified

    def json(self):
        return {'id': self.id, 'assignment_id': self.assignment_id, 'content': self.content}
    
    def __repr__(self):
        return f"Feedback({self.id}, {self.assignment_id})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'form_id': self.form_id,
            'content': self.content,
            'created': self.created.isoformat(),
            'last_modified': self.last_modified.isoformat()
        }
    
    @classmethod
    def get_feedback_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def get_feedbacks_by_assignment_id(cls, assignment_id):
        return cls.query.filter(cls.assignment_id == assignment_id).all()
    
    @classmethod
    def get_feedbacks_by_assignment_id_and_form_id(cls, assignment_id, form_id):
        #Get the answers where the assignment_id and form_id match
        results = db.session.query(Answer.key, cls.content).join(cls, cls.answer_id == Answer.id).filter(
            cls.assignment_id == assignment_id, Answer.form_id == form_id).all()
    
        
        #Add to results the feedbacks that are associated with the section_key and form_id
        #If the section_key is null, use the form_name instead
        results += db.session.query(
            db.case([(cls.section_key.isnot(None), cls.section_key)], else_=Form.name).label('key'),
            cls.content
        ).join(Form, cls.form_id == Form.id).filter(
            cls.assignment_id == assignment_id, cls.form_id == form_id
        ).all()
        
      

        # Debugging: Log the results
        print(f"Query results for assignment_id={assignment_id} and form_id={form_id}: {results}")
        
        # Convert the Row objects to a list of dictionaries
        feedback_list = [{'key': row[0], 'content': row[1]} for row in results]
        return feedback_list
       
    
    @classmethod
    def delete_feedback_by_id(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_feedback_by_answer_id(cls, answer_id):
        return cls.query.filter(cls.answer_id == answer_id).first()
    
class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        session = db.session
        load_instance = True

