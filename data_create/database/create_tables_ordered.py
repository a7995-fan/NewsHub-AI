from sqlalchemy.ext.asyncio import create_async_engine
from models.users import Base as UserBase
from models.news import Base as NewsBase
from models.favourite import Base as FavouriteBase
from models.history import Base as HistoryBase

# 数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True
)

# 按依赖顺序创建所有表
async def create_tables():
    async with async_engine.begin() as conn:
        # 先创建用户表（没有外键依赖）
        await conn.run_sync(UserBase.metadata.create_all)
        print("用户表创建完成")
        
        # 再创建新闻表（没有外键依赖）
        await conn.run_sync(NewsBase.metadata.create_all)
        print("新闻表创建完成")
        
        # 再创建收藏表（依赖用户表和新闻表）
        await conn.run_sync(FavouriteBase.metadata.create_all)
        print("收藏表创建完成")
        
        # 最后创建浏览记录表（依赖用户表和新闻表）
        await conn.run_sync(HistoryBase.metadata.create_all)
        print("浏览记录表创建完成")
    
    await async_engine.dispose()

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
    print("数据库表创建完成")
