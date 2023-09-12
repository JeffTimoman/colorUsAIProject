from webdata import  db
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    source_link = db.Column(db.String(200), nullable=False)
    result_link = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
    def __repr__(self):
        return f"Result('{self.id}', '{self.source_link}', '{self.result_link}', '{self.date_created}')"
    
    @property
    def source_link_name(self):
        return self.source_link.split('\\')[-1]
    
    @property
    def result_link_name(self):
        return self.result_link.split('\\')[-1]