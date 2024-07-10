from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import DateTime
from sqlalchemy.ext.associationproxy import association_proxy
import datetime

from config import db

# Models go here!

class Supplier():
  __tablename__ ='suppliers'
  id = db.column(db.integer, primary_key=True)
  name = db.column(db.string)
  description = db.column(db.string)
  date = db.column(DateTime, default=datetime.datetime.utcnow)

  def __ref__(self):
    return f'<Suppliers{self.id},{self.name},{self.description},{self.date}>'