from fastapi import APIRouter, Depends, HTTPException, status
from config.db_conf import get_db
from crud import ai
from schemas.ai import ChatRequest, ChatResponse
from utils.response import success_response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/chat")
async def chat(chat_request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 判断是否需要搜索相关新闻
        if any(keyword in chat_request.message.lower() for keyword in ["搜索", "查找", "新闻", "相关", "推荐"]):
            # 使用基于搜索的AI问答
            response, conversation_id = await ai.ai_chat_with_search(db, chat_request.message, chat_request.conversation_id)
        else:
            # 使用通用AI问答
            response, conversation_id = await ai.ai_chat(db, chat_request.message, chat_request.conversation_id)
        
        return success_response(message="AI回复成功", data=ChatResponse(
            message=response,
            conversation_id=conversation_id
        ))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI问答失败: {str(e)}"
        )

@router.post("/chat/search")
async def chat_with_search(chat_request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 强制使用基于搜索的AI问答
        response, conversation_id = await ai.ai_chat_with_search(db, chat_request.message, chat_request.conversation_id)
        
        return success_response(message="AI回复成功", data=ChatResponse(
            message=response,
            conversation_id=conversation_id
        ))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI问答失败: {str(e)}"
        )

@router.get("/categories")
async def get_ai_categories(db: AsyncSession = Depends(get_db)):
    try:
        categories = await ai.get_categories(db)
        return success_response(message="获取分类成功", data=[{
            "id": cat.id,
            "name": cat.name,
            "sort_order": cat.sort_order
        } for cat in categories])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分类失败: {str(e)}"
        )

@router.get("/news")
async def get_ai_news(db: AsyncSession = Depends(get_db), limit: int = 20):
    try:
        news_list = await ai.get_news_for_ai(db, limit=limit)
        return success_response(message="获取新闻成功", data=[{
            "id": news[0].id,
            "title": news[0].title,
            "description": news[0].description,
            "content": news[0].content,
            "image": news[0].image,
            "author": news[0].author,
            "category_id": news[0].category_id,
            "category_name": news[1].name,
            "views": news[0].views,
            "publish_time": news[0].publish_time.isoformat()
        } for news in news_list])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取新闻失败: {str(e)}"
        )
