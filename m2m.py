# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from sqlalchemy_utils import *

base = declarative_base()

assoc = Table('assoc', base.metadata,
  Column('aform_id', Integer, ForeignKey('AForm.id')),
  Column('bform_id', Integer, ForeignKey('BForm.id')),
  Column('tag_id', Integer, ForeignKey('Tag.id'))
)

class Tag(base):
  __tablename__ = 'Tag'
  id = Column(Integer, primary_key = True)
  name = Column(String)
  aform = relationship('AForm', secondary = assoc, back_populates = 'atag')
  bform = relationship('BForm', secondary = assoc, back_populates = 'btag')

class Form(AbstractConcreteBase, base):
  id = Column(Integer, primary_key = True)
  amount = Column(Integer)

  @declared_attr
  def __tablename__(cls):
    return cls.__name__
  
  @declared_attr
  def __mapper_args__(cls):
    return {
      'polymorphic_identity': cls.__name__,
      'concrete':True
  }

  
class AForm(Form, base):
  atag = relationship('Tag', secondary = assoc, back_populates = 'aform')

class BForm(Form, base):
   btag = relationship('Tag', secondary = assoc, back_populates = 'bform')

db_uri = 'sqlite:////tmp/m2m.sqlite'
engine = create_engine(db_uri, echo =True)
if database_exists(engine.url):
  drop_database(db_uri)
  create_database(engine.url)
base.metadata.create_all(bind = engine)
Session = sessionmaker(bind = engine)
session = Session()

a = AForm(amount = 100)
atag = Tag(name = 'booked')
a.atag.append(atag)
session.add(a)
b = BForm(amount = 200)
btag = Tag(name = 'canceled')
b.btag.append(btag)
session.add(b)
session.commit()
session.query(AForm).all()
forms=session.query(Form.amount, Form).all()
for f in forms:
  print(f)
#  print(f.atag[0].name)
#  print(f.btag[0].name)
