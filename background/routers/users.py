from fastapi import APIRouter, Depends, HTTPException, status
from config.db_conf import get_db
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, LoginRequest, UserUpdateRequest, UserChangePasswordRequest
from utils.response import success_response
from utils.dependencies import get_current_user
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):  # 用户信息 和 db
    # 注册逻辑：验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }

    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)


@router.post("/login")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户名和密码 -> 生成 Token -> 响应结果
    result = await users.login(db, login_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    user, token = result
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)

# 查Token查用户 → 封装crud → 功能整合成一个工具函数 → 路由导入使用：依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))



# 修改用户信息：验证Token → 更新（用户输入数据 put提交 → 请求体参数 → 定义Pydantic模型类） → 响应结果
# 参数：用户输入的 + 验证Token的 + db（调用更新的方法）
@router.put("/update")
async def update_user_info(
    user_data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.update_user(db, user.username, user_data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(user))



@router.put("/password")
async def update_password(
    password_data: UserChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res_change_pwd = await users.change_password(
        db, 
        user, 
        password_data.old_password, 
        password_data.new_password
    )
    if not res_change_pwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 原代码500不合理，修正为400
            detail="修改密码失败，请检查旧密码是否正确"
        )
    return success_response(message="修改密码成功")
