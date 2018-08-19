from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
	__tablename__ = "person"

	id = Column('id', Integer, primary_key=True)
	username = Column('username', String, unique=True)

engine = create_engine('sqlite:///database_metadata', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()
# ----Individual database added------
# user = User()
# user.id = 0
# user.username = "alice"
#
# session.add(user)
# session.commit()

users = session.query(User).all()
for user in users:
	print("App metadata: %s with id #%d" % (user.username, user.id,))

session.close()
