from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News, Category
from models.users import User
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# 千问API配置
QIANWEN_API_KEY = os.getenv("QIANWEN_API_KEY", "sk-f3c325f1f5d84e5b8ecce7af876e7fce")
QIANWEN_API_BASE = os.getenv("QIANWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")

# 初始化千问模型
llm = ChatOpenAI(
    model="qwen-plus",
    openai_api_key=QIANWEN_API_KEY,
    openai_api_base=QIANWEN_API_BASE,
    temperature=0.7
)

# 定义新闻助手提示模板
NEWS_ASSISTANT_TEMPLATE = """你是一个专业的新闻助手，基于以下数据库信息回答用户的问题。

数据库中的新闻分类：
{categories}

数据库中的新闻信息（最新20条）：
{news}

用户问题：{question}

请基于以上数据库信息，为用户提供准确、有用的回答。如果问题涉及到具体的新闻内容，请引用相关新闻的标题和内容。如果问题涉及到新闻分类，请提供相关分类的介绍。

回答要求：
1. 基于数据库信息回答，不要编造
2. 回答要准确、简洁、有用
3. 如果数据库中没有相关信息，请诚实地告知
4. 回答要友好、专业
5. 可以适当引用数据库中的新闻标题和内容
"""

# 创建提示模板
prompt = ChatPromptTemplate.from_template(NEWS_ASSISTANT_TEMPLATE)

# 获取数据库中的新闻分类
async def get_categories(db: AsyncSession):
    query = select(Category).order_by(Category.sort_order)
    result = await db.execute(query)
    return result.scalars().all()

# 获取数据库中的新闻信息
async def get_news_for_ai(db: AsyncSession, limit: int = 20):
    query = select(News, Category).join(Category, News.category_id == Category.id).order_by(News.publish_time.desc()).limit(limit)
    result = await db.execute(query)
    return result.all()

# 获取特定分类的新闻
async def get_news_by_category(db: AsyncSession, category_id: int, limit: int = 10):
    query = select(News, Category).join(Category, News.category_id == Category.id).where(News.category_id == category_id).order_by(News.publish_time.desc()).limit(limit)
    result = await db.execute(query)
    return result.all()

# 搜索新闻
async def search_news(db: AsyncSession, keyword: str, limit: int = 10):
    query = select(News, Category).join(Category, News.category_id == Category.id).where(
        News.title.contains(keyword) | News.content.contains(keyword)
    ).order_by(News.publish_time.desc()).limit(limit)
    result = await db.execute(query)
    return result.all()

# 格式化数据库信息用于AI处理
def format_database_info(categories, news_list):
    # 格式化分类信息
    categories_text = "\n".join([f"- {cat.name}" for cat in categories])
    
    # 格式化新闻信息
    news_text = "\n".join([
        f"标题: {news[0].title}\n分类: {news[1].name}\n作者: {news[0].author}\n发布时间: {news[0].publish_time}\n浏览量: {news[0].views}"
        for news in news_list
    ])
    
    return categories_text, news_text

# AI问答处理
async def ai_chat(db: AsyncSession, question: str, conversation_id: str = None):
    try:
        # 获取数据库信息
        categories = await get_categories(db)
        news_list = await get_news_for_ai(db, limit=20)
        
        # 格式化数据库信息
        categories_text, news_text = format_database_info(categories, news_list)
        
        # 构建消息
        messages = [
            SystemMessage(content="你是一个专业的新闻助手，基于数据库信息回答用户问题。"),
            HumanMessage(content=f"数据库中的新闻分类：\n{categories_text}\n\n数据库中的新闻信息（最新20条）：\n{news_text}\n\n用户问题：{question}")
        ]
        
        # 调用LLM
        response = await llm.ainvoke(messages)
        
        return response.content, conversation_id or "default"
        
    except Exception as e:
        print(f"AI问答错误: {e}")
        return "抱歉，AI助手暂时无法回答您的问题，请稍后再试。", conversation_id or "default"

# 基于搜索的AI问答
async def ai_chat_with_search(db: AsyncSession, question: str, conversation_id: str = None):
    try:
        # 先搜索相关新闻
        news_list = await search_news(db, question, limit=5)
        
        if news_list:
            # 格式化搜索结果
            news_text = "\n".join([
                f"标题: {news[0].title}\n分类: {news[1].name}\n内容: {news[0].content[:200]}..."
                for news in news_list
            ])
            
            # 构建消息
            messages = [
                SystemMessage(content="你是一个专业的新闻助手，基于搜索结果回答用户问题。"),
                HumanMessage(content=f"搜索结果：\n{news_text}\n\n用户问题：{question}")
            ]
            
            # 调用LLM
            response = await llm.ainvoke(messages)
            
            return response.content, conversation_id or "search"
        else:
            # 没有搜索结果，使用通用问答
            return await ai_chat(db, question, conversation_id)
            
    except Exception as e:
        print(f"基于搜索的AI问答错误: {e}")
        return "抱歉，AI助手暂时无法回答您的问题，请稍后再试。", conversation_id or "search"
