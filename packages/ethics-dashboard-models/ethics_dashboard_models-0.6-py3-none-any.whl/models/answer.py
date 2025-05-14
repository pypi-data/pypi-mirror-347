from .db import db, ma


class Answer(db.Model):
    __tablename__ = "answers"
    
    id = db.Column("answer_id", db.Integer, primary_key=True)
    assignment_id = db.Column("assignment_id", db.Integer, db.ForeignKey('assignments.assignment_id', ondelete='CASCADE'))
    form_id = db.Column("form_id", db.Integer, db.ForeignKey('forms.form_id'))
    key = db.Column("key", db.String, nullable=True)
    value_string = db.Column("value_string", db.String, nullable=True)
    value_int = db.Column("value_int", db.Integer, nullable=True)
    created = db.Column("created", db.TIMESTAMP)
    last_modified = db.Column("last_modified", db.TIMESTAMP, nullable=True)

    def __init__ (self, assignment_id, form_id, key, value_string, value_int, created, last_modified):
        self.assignment_id = assignment_id
        self.form_id = form_id
        self.key = key
        self.value_string = value_string
        self.value_int = value_int
        self.created = created
        self.last_modified = last_modified

    def json(self):
        return {'id': self.id, 'assignment_id': self.assignment_id, 'form_id': self.form_id, 'key': self.key, 'value_string': self.value_string, 'value_int': self.value_int, 'created': self.created, 'last_modified': self.last_modified}
    
    def __repr__(self):
        return f"Answer ID:({self.id}, assignment ID: {self.assignment_id}, form ID: {self.form_id}, key: {self.key}, val: {self.value_string}, val: {self.value_int}, created: {self.created}, modified: {self.last_modified})"
    
    @classmethod
    def get_answer_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def get_answers_by_assignment_id(cls, assignment_id):
        return cls.query.filter(cls.assignment_id == assignment_id).all()
    
    @classmethod
    def delete_answer_by_id(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def post_answer(cls, assignment_id, form_id, key, value_string, value_int, created, last_modified):
        new_answer = cls(assignment_id, form_id, key, value_string, value_int, created, last_modified)
        db.session.add(new_answer)
        db.session.commit()

    @classmethod
    def get_answers_by_form_id(cls, form_id):
        return cls.query.filter(cls.form_id == form_id).all()
    
    @classmethod
    def get_answers_by_assignment_id_and_form_id(cls, assignment_id, form_id):
        print(f"Fetching answers for assignment_id: {assignment_id} and form_id: {form_id}")
        answers = cls.query.filter(cls.assignment_id == assignment_id, cls.form_id == form_id).all()
        print(f"Found answers: {answers}")
        return answers

    @classmethod
    def delete_answers_by_assignment_id_and_form_id(cls, assignment_id, form_id):
        print("deleting answers for assignment id and form id in answer model " + str(assignment_id) + " and form id " + str(form_id))
        answers = cls.query.filter(cls.assignment_id == assignment_id, cls.form_id == form_id).all()
        print("answers to delete in answer model are " + str(answers))
        for answer in answers:
            db.session.delete(answer)
        db.session.commit()

    @classmethod
    def delete_answers_by_assignment_id(cls, assignment_id):
        db.session.query(cls).filter(cls.assignment_id == assignment_id).delete()
        db.session.commit()

class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        session = db.session
        load_instance = True