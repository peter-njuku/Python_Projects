from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE="postgresql://peter:Peter@localhost:5432/quizapplication"

engine=create_engine(URL_DATABASE)

sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

base=declarative_base()
