from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import UserToken, User

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码加密
def get_hash_password(password: str):
    return pwd_context.hash(password)

# 密码验证
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 验证 Token
async def verify_token(db: AsyncSession, token: str):
    # 查询 token 是否存在且未过期
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()
    
    if not user_token:
        return None
    
    # 检查 token 是否过期
    if datetime.now() > user_token.expires_at:
        return None
    
    # 获取用户信息
    user_stmt = select(User).where(User.id == user_token.user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    return user