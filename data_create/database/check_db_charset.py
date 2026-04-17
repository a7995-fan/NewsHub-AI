import asyncio
import aiomysql

async def check_charset():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 检查数据库字符集
        await cur.execute("SELECT @@character_set_database, @@collation_database")
        result = await cur.fetchone()
        print(f"数据库字符集: {result[0]}, 排序规则: {result[1]}")
        
        # 检查表是否存在
        await cur.execute("SHOW TABLES")
        tables = await cur.fetchall()
        print(f"\n现有表: {[t[0] for t in tables]}")
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(check_charset())
