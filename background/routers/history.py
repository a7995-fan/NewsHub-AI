from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.dependencies import get_current_user
from utils.response import success_response
from crud import history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await history.add_or_update_history(db, user.id, data.news_id)
    return success_response(message="添加浏览记录成功", data=result)


@router.get("/list")
async def get_history_list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await history.get_history_list(db, user.id, page, page_size)
    
    history_list = [{
        **news.__dict__,
        "viewTime": view_time.isoformat(),
        "historyId": history_id,
        "viewCount": view_count,
        "categoryName": category_name
    } for news, view_time, history_id, view_count, category_name in rows]
    
    has_more = total > page * page_size
    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)
    
    return success_response(message="获取浏览记录列表成功", data=data)


@router.delete("/remove")
async def remove_history(
    history_id: int = Query(default=..., alias="historyId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await history.remove_history(db, user.id, history_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="浏览记录不存在"
        )
    return success_response(message="删除浏览记录成功")


@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await history.remove_all_history(db, user.id)
    return success_response(message=f"清空了{count}条浏览记录")
