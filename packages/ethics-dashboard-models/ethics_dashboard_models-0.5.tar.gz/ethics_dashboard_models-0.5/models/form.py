from .db import db, ma 

class Form(db.Model):
    __tablename__ = "forms"

    id = db.Column("form_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}
    
    def __repr__(self):
        return f"Form({self.id}, {self.name})"
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def get_name(self):
        return self.name
    
    @classmethod
    def get_form_by_name(cls, name):
        print("FORM MODEL: get_form_by_name called with name " + name)
        f = cls.query.filter(cls.name == name).first()
        if f:
            print("form returned in get form by name in form model was " + f.name)
            return f
        else:
            print("No form found with name " + name)
            return None
    
    @classmethod
    def get_form_id_by_name(cls, name):
        form = cls.query.filter(cls.name == name).first()
        return form.id
    
    @classmethod
    def get_form_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod 
    def post_form(cls, name):
        form = cls(name)
        db.session.add(form)
        db.session.commit()

    @classmethod
    def delete_form_by_id(cls, id):
        db.session.query(cls).filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_form_by_name(cls, name):
        db.session.query(cls).filter(cls.name == name).delete()
        db.session.commit()

    @classmethod
    def patch_form_by_id(cls, id, name):
        form = db.session.query(cls).filter(cls.id == id)
        form.name = name
        db.session.commit()

    @classmethod
    def get_all_forms(cls):
        forms = cls.query.all()
        return forms
    
    @classmethod
    def get_count_of_forms(cls):
        count = db.session.query(cls).count()
        return count
    
class FormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Form
        session = db.session
        load_instance = True