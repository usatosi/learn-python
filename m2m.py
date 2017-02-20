# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from sqlalchemy_utils import *

base = declarative_base()

assoc = Table('assoc', base.metadata,
  Column('aform_id', Integer, ForeignKey('AForm.id')),
# Column('bform_id', Integer, ForeignKey('BForm.id')),
  Column('tag_id', Integer, ForeignKey('Tag.id'))
)

class Tag(base):
  __tablename__ = 'Tag'
  id = Column(Integer, primary_key = True)
  name = Column(String)
  aform = relationship('AForm', secondary = assoc, back_populates = 'atag')

class Form(AbstractConcreteBase, base):
  id = Column(Integer, primary_key = True)
  amount = Column(Integer)

class AForm(Form, base):
  __tablename__ = 'AForm'
  __mapper_args__ = {
  'polymorphic_identity':'AForm',
  'concrete':True
  }
  atag = relationship('Tag', secondary = assoc, back_populates = 'aform')

# class BForm(Form, base):
#   __tablename__ = 'BForm'
#   __mapper_args__ = {
#   'polymorphic_identity':'AForm',
#   'concrete':True
#   }

db_uri = 'sqlite:////tmp/m2m.sqlite'
drop_database(db_uri)
engine = create_engine(db_uri, echo =True)
if not database_exists(engine.url):
  create_database(engine.url)
base.metadata.create_all(bind = engine)
Session = sessionmaker(bind = engine)
session = Session()

a = AForm(amount = 100)
atag = Tag(name = 'booked')
a.atag.append(atag)
session.add(a)
session.commit()
session.query(AForm).all()
f=session.query(Form.amount, Form).first()
print(f[1].atag[0].name)
