import asyncio
import aiomysql

async def check_error():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 显示最后的错误
        await cur.execute("SHOW ENGINE INNODB STATUS")
        result = await cur.fetchone()
        if result:
            print("InnoDB Status:")
            print(result[0][:2000])  # 只打印前2000个字符
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(check_error())
