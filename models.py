from sqlalchemy import create_engine, Column, ForeignKey, inspect, desc
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR, DATE, SMALLINT
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Consultants(Base):
    __tablename__ = 'consultants'
    id = Column(INTEGER, primary_key=True)
    consultant_name = Column(VARCHAR, key='Консультант')
    consultant_password = Column(VARCHAR)


class Patients(Base):
    __tablename__ = 'patients'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    patient_first_name = Column(VARCHAR)
    patient_sur_name = Column(VARCHAR)
    patient_age = Column(INTEGER)


class Departments(Base):
    __tablename__ = 'departments'
    id = Column(INTEGER, primary_key=True)
    department_name = Column(VARCHAR)


class Diagnoses(Base):
    __tablename__ = 'diagnoses'
    id = Column(INTEGER, primary_key=True)
    diagnose_name = Column(VARCHAR)


class Reasons(Base):
    __tablename__ = 'reasons'
    id = Column(INTEGER, primary_key=True)
    reason_name = Column(VARCHAR)


class SickLists(Base):
    __tablename__ = 'sick_lists'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    sl_date = Column(DATE)
    consultant_id = Column(ForeignKey("consultants.id"))
    number_of_sl = Column(INTEGER)
    number_of_consultation = Column(SMALLINT)
    # patient_id = Column(ForeignKey("patients.id"))
    patient_sur_name = Column(VARCHAR)
    patient_age = Column(INTEGER)
    correction = Column(SMALLINT)
    department_id = Column(ForeignKey("departments.id"))
    diagnose_id = Column(ForeignKey("diagnoses.id"))
    reason_id = Column(ForeignKey("reasons.id"))
    comment = Column(VARCHAR)


engine = create_engine('sqlite:///gkh.db', echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
