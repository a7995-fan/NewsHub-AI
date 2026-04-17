import redis.asyncio as redis
import json
from typing import Any, Optional, List, Dict


# Redis 连接配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

NEWS_LIST_PREFIX = "news_list"

# 创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis 服务器的主机地址
    port=REDIS_PORT,  # Redis 端口号
    db=REDIS_DB,      # Redis 数据库编号，0~15
    decode_responses=True  # 是否将字节数据解码为字符串
)


# 设置 和 读取（字符串 和 列表或字典） "[{}]"
# 读取：字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)  # 反序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None


# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存
            value = json.dumps(value, ensure_ascii=False)  # 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False


# 写入缓存-新闻列表 key = news_list:分类id:页码:每页数量 + 列表数据 + 过期时间
async def set_cache_news_list(
    category_id: Optional[int], 
    page: int, 
    size: int, 
    news_list: List[Dict[str, Any]], 
    expire: int = 600
):
    # 调用 封装的 Redis 的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


# 读取缓存-新闻列表
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{size}"
    return await get_json_cache(key)
