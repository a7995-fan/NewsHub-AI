import asyncio
import aiomysql

async def drop_all_tables():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 禁用外键检查
        await cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 获取所有表
        await cur.execute("SHOW TABLES")
        tables = await cur.fetchall()
        
        # 删除所有表
        for table in tables:
            table_name = table[0]
            try:
                await cur.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"删除表 {table_name}")
            except Exception as e:
                print(f"删除表 {table_name} 失败: {e}")
        
        # 启用外键检查
        await cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        await conn.commit()
        
        print("\n所有表已删除")
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(drop_all_tables())
