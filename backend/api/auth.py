# backend/api/auth.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

# --- Namespace and Models ---
ns = Namespace('auth', description='使用者認證相關操作')

register_model = ns.model('UserRegisterInput', {
    'username': fields.String(required=True, description='使用者名稱'),
    'email': fields.String(required=True, description='電子郵件'),
    'password': fields.String(required=True, description='密碼'),
})

login_model = ns.model('UserLoginInput', {
    'username': fields.String(required=True, description='使用者名稱'),
    'password': fields.String(required=True, description='密碼'),
})

# --- API Resources ---
@ns.route('/register')
class UserRegister(Resource):
    @ns.expect(register_model, validate=True)
    def post(self):
        """註冊一個新使用者"""
        data = ns.payload
        if User.query.filter_by(username=data['username']).first() is not None:
            return {'message': '此使用者名稱已被註冊'}, 400
        if User.query.filter_by(email=data['email']).first() is not None:
            return {'message': '此電子郵件已被註冊'}, 400
            
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': '使用者註冊成功'}, 201

@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        """使用者登入並獲取 JWT"""
        data = ns.payload
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
            
        return {'message': '使用者名稱或密碼錯誤'}, 401