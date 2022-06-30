from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, DateTime, BigInteger, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date

from database import Base, engine
import uuid


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True,
                unique=True, default=uuid.uuid4)
    role = Column(String, default='user', nullable=False)
    email_id = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    phone_number = Column(BigInteger, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    updated_by = Column(String, nullable=False)
    assets = relationship('AssetsModel', backref='user')
    attendance = relationship('AttendanceModel', backref='user')
    teams = relationship('Teams', backref='user')


class AssetsModel(Base):
    __tablename__ = 'asset'
    laptop_id = Column(String, nullable=False, unique=True)
    phone_id = Column(String, nullable=False, unique=True)
    sim_number = Column(Integer, primary_key=True)
    benefits = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    updated_by = Column(String, nullable=False)
    email_id = Column(String, ForeignKey('user.email_id'), unique=True)


class AttendanceModel(Base):
    __tablename__ = 'attendance'
    index = Column(Integer, primary_key=True)
    current_date = Column(Date, nullable=False, default=date.today())
    in_time = Column(Time, nullable=False)
    percentage = Column(Float, default=0)
    email_id = Column(String, ForeignKey('user.email_id'))


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    project_description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    posted_by = Column(String, nullable=False)
    posted_on = Column(DateTime, default=datetime.utcnow)


class Teams(Base):
    __tablename__ = 'team'
    index = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    email_id = Column(String, ForeignKey('user.email_id'))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String, nullable=False)


# creates table in database
Base.metadata.create_all(engine)
