from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column
from sqlalchemy import *
from sqlalchemy.sql import expression
from datetime import datetime

#engine = create_engine('mysql+mysqldb://root:toor@localhost/payroller')
metadata = MetaData()

class DBManager(object):

    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, pool_recycle=600)


    def get_connection(self):
        return self.engine.connect()

    def _execute_select(self, query):
        conn = self.get_connection()
        results = conn.execute(query).fetchall()
        conn.close()
        return [dict(row.items()) for row in results]

    def _execute_insert(self, query):
        conn = self.get_connection()
        result_id = conn.execute(query).inserted_primary_key
        conn.close()
        return result_id

    def _execute_update(self, query):
        conn = self.get_connection()
        result_id = conn.execute(query)
        conn.close()
        return result_id

    def _execute_delete(self, query):
        conn = self.get_connection()
        conn.execute(query)
        conn.close()
        return

    def get_tables(self):
        return metadata.tables.keys()
######################################
    def get_employees(self):
        q = select([employees_table])
        return self._execute_select(q)

    def get_employee_name(self, epe):
        q = select([employees_table.c.name]).where(employees_table.c.epe_id == epe)
        return self._execute_select(q)

    def get_punches(self):
        q = select([punches_table]).order_by(desc(punches_table.c.pch_id))
        return self._execute_select(q)

    def get_punch_types(self):
        q = select([punch_type_table])
        return self._execute_select(q)

    def insert_punch(self, epe_id, punch_type):

        punch = {
            'date': datetime.utcnow(),
            'epe_id': epe_id,
            'pte_id': punch_type
        }
        q = punches_table.insert().values(punch)
        punch_id = self._execute_insert(q)
        return punch_id

    def update_punch(self, pch_id, punch_type):
        q = punches_table.update().where(punches_table.c.pch_id == pch_id).values(pte_id=punch_type)
        punch_id = self._execute_update(q)
        return punch_id

    def delete_punch(self, pch_id):
        q = punches_table.delete(punches_table.c.pch_id == pch_id)
        delete = self._execute_delete(q)


    def insert_employee(self, name, pay_rate):
        employee = {
            'name': name,
            'pay_rate': pay_rate
        }
        q = employees_table.insert().values(employee)
        epe_id = self._execute_insert(q)
        return epe_id

    def update_employee(self, epe_id, pay_rate):
        q = employees_table.update().where(employees_table.c.epe_id == epe_id).values(pay_rate=pay_rate)
        employee = self._execute_update(q)
        return employee


    def delete_employee(self, epe_id):
        q = employees_table.delete(employees_table.c.epe_id == epe_id)
        self._execute_delete(q)

punches_table = Table('punches', metadata,
    Column('pch_id', Integer, primary_key=True),
    Column('date', DateTime, nullable = False, default=datetime.utcnow()),
    Column('epe_id', ForeignKey('employees.epe_id'), nullable=False),
    Column('pte_id', ForeignKey('punch_types.pte_id'), nullable=False)
)

punch_type_table = Table('punch_types', metadata,
    Column('pte_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(15), nullable=False)
)

employees_table = Table('employees', metadata,
    Column('epe_id', Integer, primary_key=True),
    Column('name', String(30), nullable=False),
    Column('pay_rate', Numeric(5, 2), nullable=False)
)


def create_tables(db_uri):
    engine = create_engine(db_uri)
    metadata.bind = engine
    metadata.create_all()

    add_punch_types(engine)

def drop_tables(db_uri):
    engine = create_engine(db_uri)
    metadata.bind = engine
    metadata.drop_all()


def add_punch_types(engine):
    engine.connect().execute(punch_type_table.insert().values(pte_id=1, name='Punch In'))
    engine.connect().execute(punch_type_table.insert().values(pte_id=2, name='Punch Out'))

def fresh_start():
    DB_URI = 'mysql+mysqldb://root:toor@localhost/payroller'
    drop_tables(DB_URI)
    create_tables(DB_URI)
fresh_start()
