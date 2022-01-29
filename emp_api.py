from flask import Flask, request
from pymongo import MongoClient
from bson import json_util
import os
import json

os.system("cls")

app = Flask(__name__)

connection = MongoClient(host="localhost", port=27017)
database_name = "Employee_DB"
collection_name = "Employee"
db_coll = connection[database_name][collection_name]


@app.route("/lbc/employee/list", methods=["GET"])
def get_employee():
    emps = db_coll.find()
    employee = []
    for row in emps:
        employee.append(row)

    employee = json.dumps(employee, default=json_util.default)
    return employee

@app.route("/lbc/employee/detail", methods=["GET"])
def get_employee_detail():
    empId = request.args['empId']
    id = request.args['id']
    print(empId)
    employee = db_coll.find_one({"id":id,"empId":empId})
    print(employee)
    employee = json.dumps(employee,default=json_util.default)
    return employee

@app.route("/lbc/employee/create", methods=["POST"])
def create_employee():
    args = request.get_json()
    print(args)
    db_coll.insert_one(args)
    return {"status": "INSERTED"}

@app.route("/lbc/employee/create_many", methods=["POST"])
def create_many_employee():
    args = request.get_json()
    print(args)
    db_coll.insert_many(args)
    return {"status": "INSERTED"}

@app.route("/lbc/employee/update", methods=["PUT"])
def update_employee():
    args = request.get_json()
    query = {'empId':args['empId']}
    newvalues = { "$set": { 'fullName': args['fullName'], 'emailId':args['emailId'],'phone': args['phone'],'status':args['status']} }
    print(args)
    db_coll.update_one(query,newvalues)
    return {"status": "UPDATED"}

@app.route("/lbc/employee/delete", methods=["DELETE"])
def delete_employee():
    args = request.get_json()
    query = {'empId':args['empId']}
    print(args)
    db_coll.delete(query)
    return {"status": "DELETED"}

@app.route("/lbc/employee/delete_many", methods=["DELETE"])
def delete_many_employee():
    args = request.get_json()
    query = {'empId':args['empId']}
    print(args)
    db_coll.delete_many(query)
    return {"status": "DELETED"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
