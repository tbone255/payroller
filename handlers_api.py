import tornado.ioloop
import tornado.web
import json
from db.db_manager import DBManager
from decimal import Decimal
from exceptions import *

from sqlalchemy.exc import IntegrityError
from tornado.web import MissingArgumentError


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        if not self.application.dbm:
            self.dbm = DBManager('mysql+mysqldb://root:toor@localhost/payroller')

class HomeHandler(BaseHandler):
    def get(self):
        return self.render('./templates/home.html')
#######################################
class PunchHandler(BaseHandler):


    def get(self, modal=0, id=''):

        return self.render('./templates/punch.html', punches=self.dbm.get_punches(), name=self.dbm.get_employee_name, modal=modal, id=id)

    def post(self):
        modal = 0
        id = ''
        add_id = self.get_argument('employee', None)
        edit_id = self.get_argument('edit_id', None)
        delete_id = self.get_argument('delete_id', None)
        if add_id:
            punch_type = self.get_argument('punchtype', None)
            try:
                punch_id = self.dbm.insert_punch(add_id, punch_type)
                ret = {'punch_id': punch_id[0]}
            except Exception as e:
                print e
                modal = 1
                id = 'Employee ID'
        elif edit_id:
            punch_type = self.get_argument('punchtype', None)
            try:
                punch_id = self.dbm.update_punch(edit_id, punch_type)
            except Exception as e:
                modal = 1
                id = 'Punch ID.......'
                print e
        elif delete_id:
            try:
                self.dbm.delete_punch(delete_id)
            except Exception as e:
                modal = 1
                id = 'Punch ID'
        self.get(modal, id)

    def not_valid(self):
        self.get()


class EmployeeHandler(BaseHandler):
    def get(self, modal=0, id=0):
        #return self.render('./templates/employees/view.html', )
        emps = self.dbm.get_employees()
        self.render('./templates/employee.html', emps=emps, modal=modal, id=id)

    def post(self):
        modal = 0
        id = ''
        add_id = self.get_argument('add_id', None)
        edit_id = self.get_argument('edit_id', None)
        delete_id = self.get_argument('delete_id', None)
        if add_id:
            payrate = self.get_argument('payrate', None)
            try:
                employee_id = self.dbm.insert_employee(add_id, payrate)
            except Exception as e:
                modal = 1
                id = 'Employee ID or Payrate'
        elif edit_id:
            payrate = self.get_argument('payrate', None)
            try:
                punch_id = self.dbm.update_employee(edit_id, payrate)
            except Exception as e:
                modal = 1
                id = 'Employee ID or Punch ID'
                print e
        elif delete_id:
            try:
                self.dbm.delete_employee(delete_id)
            except Exception as e:
                modal = 1
                id = 'Employee ID'
        self.get(modal, id)




#######################################



api_v1 = '/api/v1'
handlers = [
    (api_v1 + r'/punch', PunchHandler),
    (api_v1 + r'/employee', EmployeeHandler),
]
