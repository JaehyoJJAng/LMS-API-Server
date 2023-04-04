---
title:  "[CS] 데브옵스 프로젝트 #4 - 최종 구현"
excerpt: "회고록"

categories:
  - "CS-Projects"
tags:
  - [회고록,최종구현]

toc: true
toc_sticky: true
published: false
---

# ERD

- `Entity Relationship Diagram`
- `course`
  - 강의 정보 저장 테이블
- `users`
  - 유저 정보 저장 테이블
- `enrollment`
  - 수강 정보 테이블
  - `course` , `student` 테이블을 참조
- [dbdiagram.io](https://dbdiagram.io/d/642b849a5758ac5f17267836)

![image](https://user-images.githubusercontent.com/91415701/229717074-a5017f7a-d5bd-4f8a-b01f-1f459bdb058b.png)

**Schema**
```json
Table users {
  user_id integer [primary key,increment]
  name varchar(10)
  email varchar(50)
  phone varchar(15)
  birthdate date
}

Table class {
  class_id integer [primary key,increment]
  class_name varchar(70)
  code integer
  professor_id integer 
}

Table enrollment {
  enrollment_id integer [primary key,increment]
  class_id integer
  user_id integer
}

Table token {
  id integer [primary key,increment]
  user_id int
  token varchar(255)
}

Ref: enrollment.class_id > class.class_id
Ref: enrollment.user_id > users.user_id
Ref: class.professor_id > users.user_id
Ref: token.user_id > users.user_id
```

# API 문서 제작

- 문서 제작
- Swagger 서비스 이용하여 API 문서 제작

|Method|Path|Request Header|Request Body|Response Status Code|Response Body|DESC|
|------|----|--------------|------------|--------------------|-------------|----|
|GET|/class|\-|\-|200 OK|list-of-class|모든 수업 조회|
|GET|/class?professor_id={professor_id}|\-|\-|200 OK|list-of-class|특정 분류의 수업 조회|
|GET|/class?code={code}|\-|\-|200 OK|list-of-class|특정 분류의 수업 조회|
|GET|/class?name={class_name}|\-|\-|200 OK|list-of-class|특정 분류의 수업 조회|
|GET|/enrollment?user_id={user_id}|\-|\-|200 OK|list-of-class|수강중인 모든 수업 조회|
|POST|/enrollment|Authorization|detail-of-class|200 OK|\-|수강 신청|
|POST|/class|Authorization|detail-of-class|200 OK|\-|새로운 수업 생성|
|PUT|/users?user_id={user_id}|Authorization|detail-of-change|200 OK|\-|개인정보 변경|
|DELETE|/enrollment?em_id={em_id}|Authorization|\-|200 OK|\-|수강신청 취소|

<br>

**`GET /class`**
```json
{
  "class": [
    {
      "class_id": 1,
      "class_name": "JavaScript",
      "code": 334324,
      "professor_id": 2
    },
    {
      "class_id": 2,
      "class_name": "CSS",
      "code": 334325,
      "professor_id": 2
    }    
  ]
}
```

**`GET /class?professor_id={professor_id}`**
```json
# /class?professor_id=2
{
  "class": [
    {
      "class_id": 1,
      "class_name": "JavaScript",
      "code": 334324,
      "professor_id": 2
    },
    {
      "class_id": 2,
      "class_name": "CSS",
      "code": 334325,
      "professor_id": 2
    }    
  ]
}
```

**`GET /class?name={course_name}`**
```json
# /class?name=JavaScript

{
  "class": [
    {
      "class_id": 1,
      "class_name": "JavaScript",
      "code": 334324,
      "professor_id": 2
    }
  ]
}
```


**`GET /class?code={code}`**
```json
# /class?code=334324

{
  "class": [
    {
      "class_id": 1,
      "class_name": "JavaScript",
      "code": 334324,
      "professor_id": 2
    }
  ]
}
```

**`GET /enrollment?user_id={user_id}`**
```json
# /enrollment?user_id=1
{
  "enrollment": [
    {
      "em_id": 1,
      "class_id": 1,
      "user_id": 1
    },
    {
      "em_id": 2,
      "class_id": 2,
      "user_id": 1
    }
  ]
}
```

**`POST /enrollment`**
```json
{
  "user_id": 1,
  "class_id":3
}
```

**`POST /class`**
```json
{ 
  "class_id": 5,
  "class_name" : "재미없는 전공 수업",
  "code": 554334,
  "professor_id": 5
}
```

**`PUT /users?user_id={user_id}`**
```json
# /users?user_id=1
{
  "name": "맛재효",
  "email": "dd@dd.com",
  "phone": "xx",
  "birthdate": "xxxx-xx-xx"
}
```

<br>

# 데이터베이스

- 모델링한 데이터베이스 구현
- `MySQL` 채택
- 도커로 데이터베이스 배포 (`MySQL`)

## 데이터베이스 배포

**docker-compose.yaml**
```yaml
version: "3"

services:
  db:
    image: mysql:5.7
    restart: always
    volumes: 
      - "mydata:/var/lib/mysql"
    ports:
      - "9988:3306"
    container_name: "lmsdb"
    env_file:
      - ".mysql.env"
volumes:
  mydata:
```

<br>

**.mysql.env**
```conf
MYSQL_ROOT_PASSWORD=lms123
MYSQL_DATABASE=lms
MYSQL_USER=lms123
MYSQL_PASSWORD=lms123
```

## 스키마 구현

**users**
```sql
CREATE TABLE IF NOT EXISTS users (
  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(10),
  email VARCHAR(50),
  phone VARCHAR(15),
  birthdate DATE
);
```

**class**
```sql
CREATE TABLE IF NOT EXISTS class (
  class_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  class_name VARCHAR(70),
  code VARCHAR(50),
  professor_id INT 
);
```

**enrollment**
```sql
CREATE TABLE IF NOT EXISTS enrollment (
  em_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  class_id INT,
  user_id INT
);
```

**token**
```sql
CREATE TABLE tokens (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
);
```

## FOIRGN KEY 지정

**enrollment.class_id > class.class_id**

- `enrollment.class_id` 컬럼에 외래키 추가
- 해당 외래키가 `class.class_id` 컬럼을 참조하도록 지정

```sql
ALTER TABLE enrollment ADD FOREIGN KEY(class_id) REFERENCES class(class_id);
```

**enrollment.user_id > users.user_id**

- `enrollment.user_id` 컬럼에 외래키 추가
- 해당 외래키가 `users.user_id` 컬럼을 참조하도록 지정

```sql
ALTER TABLE enrollment ADD FOREIGN KEY(user_id) REFERENCES users(user_id);
```

**class.professor_id > users.user_id**

- `class.professor_id` 컬럼에 외래키 추가
- 해당 외래키가 `users.user_id` 컬럼을 참조하도록 지정

```sql
ALTER TABLE class ADD FOREIGN KEY(professor_id) REFERENCES users(user_id);
```

**token.user_id > users.user_id**

- `token.user_id` 컬럼에 외래키 추가
- 해당 외래키가 `users.user_id` 컬럼을 참조하도록 지정

```sql
ALTER TABLE token ADD FOREIGN KEY(user_id) REFERENCES users(user_id);
```

## INSERT

**users 테이블**
```sql
INSERT INTO users (name,email,phone,birthdate) VALUES (
    '이재효','dlgkrtod@naver,com','010-1111-1111','1998-03-13');

INSERT INTO users (name,email,phone,birthdate) VALUES (
    '이학생','dlgkrtod@naver,com','010-2222-2222','2000-03-13');
```

**class 테이블**
```sql
INSERT INTO class (class_name,code,professor_id) VALUES ( '파이썬 정규과정',100,1);
INSERT INTO class (class_name,code,professor_id) VALUES ( '처음부터 배우는 자바스크립트',101,1);
```

**enrollment 테이블**
```sql
INSERT INTO enrollment (class_id,user_id) VALUES (1,1);
INSERT INTO enrollment (class_id,user_id) VALUES (2,2);
```

**token 테이블**
```sql
INSERT INTO token (user_id,token) VALUES (2,'qwer!@#$')
```

## 참조 예제

**강의와 교수 정보 가져오기**

```sql
SELECT enrollment.em_id,class.class_id,users.name
FROM enrollment
JOIN class ON enrollment.class_id = class.class_id 
JOIN users ON enrollment.user_id  = users.user_id;

+-------+----------+-----------+
| em_id | class_id | name      |
+-------+----------+-----------+
|     1 |        1 | 이재효    |
+-------+----------+-----------+
1 row in set (0.03 sec)
```

**사용자의 모든 수업 조회**
```sql
SELECT class.class_name,class.code,users.name
FROM enrollment
JOIN class ON enrollment.class_id = class.class_id
JOIN users ON enrollment.user_id  = users.user_id
WHERE enrollment.user_id = 2;

+-------------------------------------------+------+-----------+
| class_name                                | code | name      |
+-------------------------------------------+------+-----------+
| 처음부터 배우는 자바스크립트              | 101  | 이학생    |
+-------------------------------------------+------+-----------+
```

**특정 분류의 수업 조회 [`강사,수업명,수업코드`]**
```sql
// 강사 기준
SELECT class.class_name,class.code
FROM class
WHERE class.professor_id = 1;

+-------------------------------------------+------+
| class_name                                | code |
+-------------------------------------------+------+
| 파이썬 정규과정                           | 100  |
| 처음부터 배우는 자바스크립트              | 101  |
+-------------------------------------------+------+

// 수업명 기준
SELECT class.class_name,class.code
FROM class
WHERE class.class_name = '파이썬 정규과정';

+------------------------+------+
| class_name             | code |
+------------------------+------+
| 파이썬 정규과정        | 100  |
+------------------------+------+

// 수업코드 기준
SELECT class.class_name,class.code
FROM class
WHERE class.code = 100;

+------------------------+------+
| class_name             | code |
+------------------------+------+
| 파이썬 정규과정        | 100  |
+------------------------+------+
```

**모든 수강중인 수업 조회**
```sql
SELECT class.class_name,class.code,users.name
FROM enrollment
JOIN users ON enrollment.user_id = users.user_id
JOIN class ON enrollment.class_id = class.class_id
WHERE users.user_id = 2;

+-------------------------------------------+------+-----------+
| class_name                                | code | name      |
+-------------------------------------------+------+-----------+
| 처음부터 배우는 자바스크립트              | 101  | 이학생    |
+-------------------------------------------+------+-----------+
```

# 인증 토큰 구현

```python
from flask import Flask, request

app = Flask(__name__)

# 유저 정보 데이터베이스. 토큰과 연결된 유저 ID를 저장합니다.
user_info = {
    "aaa": 1,
    "bbb": 2
}

# 토큰 검증 데코레이터 함수
def token_required(func):
    def wrapper(*args, **kwargs):
        # request에서 토큰값 추출
        token = request.headers.get('Authorization')

        # 토큰 없으면 401 리턴 ㄱ
        if not token:
            return {"error": "Unauthorized"}, 401

        # 토큰값 유효하지 않으면 403 리턴 ㄱ
        if token not in user_info:
            return {"error": "Forbidden"}, 403

        # 토큰에 매칭되는 user 가져오기
        user_id = user_info[token]

        return func(user_id, *args, **kwargs)
    return wrapper

# 테스트용 API 엔드포인트
@app.route('/test')
@token_required
def test(user_id):
    return f"Hello, user {user_id}!"

if __name__ == '__main__':
    app.run()
```

# 최종 구현