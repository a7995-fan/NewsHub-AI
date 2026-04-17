import asyncio
import aiomysql

async def check_database_data():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 检查所有表
        await cur.execute("SHOW TABLES")
        tables = await cur.fetchall()
        print(f"数据库中的表: {[table[0] for table in tables]}")
        print()
        
        # 检查每个表的数据量
        for table in tables:
            table_name = table[0]
            await cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = await cur.fetchone()
            print(f"表 {table_name}: {count[0]} 条记录")
            
            # 如果有数据，显示前几条
            if count[0] > 0:
                await cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
                records = await cur.fetchall()
                print(f"前3条记录: {records}")
            print()
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(check_database_data())
