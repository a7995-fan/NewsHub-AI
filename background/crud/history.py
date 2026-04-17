from datetime import datetime
from sqlalchemy import select, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News, Category


# 添加或更新浏览记录
async def add_or_update_history(
    db: AsyncSession,
    user_id: int,
    news_id: int
):
    # 先查询是否已有浏览记录
    query = select(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(query)
    history = result.scalar_one_or_none()

    if history:
        # 已存在，更新浏览时间和浏览次数
        history.view_time = datetime.utcnow()
        history.view_count += 1
        await db.commit()
        await db.refresh(history)
    else:
        # 不存在，创建新记录
        history = History(user_id=user_id, news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
    
    return history


# 获取浏览记录列表
async def get_history_list(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 10
):
    # 总量
    count_query = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 获取浏览记录列表 - 联表查询 + 浏览时间排序 + 分页
    offset = (page - 1) * page_size

    query = (
        select(
            News,
            History.view_time.label("view_time"),
            History.id.label("history_id"),
            History.view_count.label("view_count"),
            Category.name.label("category_name")
        )
        .join(History, History.news_id == News.id)
        .join(Category, Category.id == News.category_id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query)
    # 解析结果：(新闻对象, 浏览时间, 浏览记录id, 浏览次数, 分类名称)
    history_list = result.all()

    return history_list, total


# 删除单条浏览记录
async def remove_history(
    db: AsyncSession,
    user_id: int,
    history_id: int
):
    stmt = delete(History).where(
        History.user_id == user_id,
        History.id == history_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# 清空浏览记录
async def remove_all_history(
    db: AsyncSession,
    user_id: int
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
