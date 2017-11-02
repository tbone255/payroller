from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime

db = create_engine('mysql+mysqldb://root:toor@localhost/payroller', echo=True)


Base = declarative_base()



#tables
class Punch(Base):
	__tablename__ = 'punches'

	id = Column('pch_id', Integer, primary_key=True, autoincrement=True)
	date_time = Column('date', DateTime, nullable = False, default=)
	employee_id = Column('epe_id', ForeignKey('employees.epe_id'), nullable=False)
	punch_type = Column('pte_id',Integer ForeignKey('punch_types.pte_id'), nullable=False)

class PunchType(Base):
	__tablename__ = 'punch_types'

	id = Column('pte_id', Integer, primary_key=True, autoincrement=True)
	name = Column('name', String, nullable=False)

class Employee(Base):
	__tablename__ = 'employees'

	id = Column('epe_id', Integer, primary_key=True, autoincrement=True)
	name = Column('name', String, nullable=False)
	pay = Column('pay_rate', Numeric(5, 2), nullable=False)

class Payroll(Base):
	id = Column('prl_id', Integer, primary_key=True, autoincrement=True)
	amount = Column('amount', Numeric(6, 2), nullable=False)
	start_date = Column('start', Date, nullable=False)
	end_date = Column('end', Date, nullable=False)
