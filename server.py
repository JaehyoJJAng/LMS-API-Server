from src.module import CRUD
from flask import Flask , request,render_template
from typing import Dict,List,Union
import json

# Set Secret file
_secret_file : str = '.secret.env'

# Set CRUD Instance
crud : CRUD = CRUD(secret_file=_secret_file)

# Connect Database
crud.connect_db()

# Create Flask Instance
app : Flask = Flask(__name__)

@app.route('/')
def root()-> str:
    return render_template('index.html')

@app.route('/classes')
def get_all_class()-> str:
    """ 모든 수업 조회 """
    read_query : str = 'SELECT * FROM class;'
    result = crud.read(read_query=read_query)
    return json.dumps(result,ensure_ascii=False)    

@app.route('/class')
def get_specific_class()-> str:
    """ 특정 분류의 수업 조회 """
    # Set request Argument
    professor_id = request.args.get('professor_id')
    code = request.args.get('code')
    class_name = request.args.get('name')
    
    # Set Query
    read_query : str = ''
    
    # request 별 read_query 설정
    if professor_id:
        read_query = f'select * from class WHERE professor_id = {professor_id}'
    elif code:
        read_query = f'select * from class WHERE code = {code}'
    elif class_name:
        read_query = f'select * from class WHERE class_name = {class_name}'
    else:
        return {"Error":{'statusCode':403,'Message':'Query does not exists'}}
    
    # Get Query Result
    result = crud.read(read_query=read_query)

    return json.dumps(result,ensure_ascii=False)

@app.route('/enrollment')
def get_enrolled()-> str:
    """ 수강중인 모든 수업 조회 """
    # Get user_id 
    user_id  = request.args.get('user_id')
    
    if user_id:        
        # Create Read Query
        read_query = f"""SELECT enrollment.em_id,class.class_name,class.code,users.name,users.user_id
        FROM enrollment
        JOIN users ON enrollment.user_id = users.user_id
        JOIN class ON enrollment.class_id = class.class_id
        WHERE users.user_id = {user_id};
        """.strip()

        # Get Datas from database
        datas = crud.read(read_query=read_query)    

        # Set result
        result = []
        
        return json.dumps(datas,ensure_ascii=False)
    else:
        return {"Error":{'statusCode':401,'Message':'유저 아이디가 정확하지 않습니다'}}

@app.route('/enrollment',methods=['POST'])
def enrolment()-> str:
    """ 수강신청 """
    data = request.get_json()
    
    # 데이터가 정상적으로 들어왔는지 체크
    if not data:
        return {'Error': {'statusCode':403,'message':'요청된 데이터가 없습니다'}}
    
    # 데이터가 유효한지 체크
    required_keys : List[str] = ['class_id','user_id']
    if all(key in data for key in required_keys) and len(required_keys) == len(data):
        try:
            # `lms.enrollment` 에 적재
            insert_query : str = f"""
            INSERT INTO enrollment (class_id,user_id) VALUES ({data['class_id']},{data['user_id']});
            """.strip()
            crud.insert(insert_query=insert_query)            
            return {"statusCode":200,"message":"Created!"}
        except:
            return {"Error": {'message':'데이터를 저장하는 도중 에러가 발생하였습니다\n자세한 사항은 어드민에게 연락바랍니다'}}
    else:
        return {'Error': {'statusCode':403,'message':'데이터가 올바르지 않습니다'}}

@app.route('/class',methods=['POST'])
def create_class()-> None:
    """ 수업 생성 """
    data = request.get_json()
    
    # 데이터가 정상적으로 들어왔는지 체크
    if not data:
        return {'Error': {'statusCode':403,'message':'요청된 데이터가 없습니다'}}
    
    # 데이터 유효한지 체크
    required_keys : List[str] = ['class_name','code','professor_id']
    if all(key in data for key in required_keys) and len(required_keys) == len(data):
        try:
            # 'lms.class' 에 적재
            insert_query : str = f"""
            INSERT INTO class (class_name,code,professor_id) VALUES (
                "{data['class_name']}",{data['code']},{data['professor_id']});""".strip()
            crud.insert(insert_query=insert_query)
            return {"statusCode":200,"message":"Created!"}
        except:
            return {"Error": {'message':'데이터를 저장하는 도중 에러가 발생하였습니다\n자세한 사항은 어드민에게 연락바랍니다'}}            
    else:
        return {"Error": {"message": "유효한 데이터가 아닙니다"}}
    
@app.route('/users',methods=["PUT"])
def update_user()-> None:
    """ 유저정보 업데이트"""
    user_id = request.args.get('user_id')
    data = request.get_json()

    # 데이터가 정상적으로 들어왔는지 체크
    if not user_id:
        return {'Error': {'statusCode':403,'message':'요청된 데이터가 없습니다'}}
    
    # 데이터 유효한지 체크
    required_keys : List[str] = ['name','email','phone','birthdate']
    if all(key in data for key in required_keys) and len(required_keys) == len(data):    
        # 데이터 수정 요청
        update_query : str = f"""
        UPDATE user SET name = {data['name']} AND
        """.strip()
        
        """ 데이터 수정 쿼리 공부한 후 수정 """
        return 'Ok'
    else:
        return {"Error": {"message": "유효한 데이터가 아닙니다"}}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)