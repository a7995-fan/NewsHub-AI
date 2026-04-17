import asyncio
import aiomysql

async def fix_database():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 检查 user_token 表是否存在 updated_at 字段
        await cur.execute("SHOW COLUMNS FROM user_token LIKE 'updated_at'")
        result = await cur.fetchone()
        
        if not result:
            print("添加 updated_at 字段到 user_token 表...")
            await cur.execute("""
                ALTER TABLE user_token 
                ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """)
            await conn.commit()
            print("字段添加成功")
        else:
            print("updated_at 字段已存在")
        
        # 检查所有表的字段
        await cur.execute("DESCRIBE user_token")
        columns = await cur.fetchall()
        print("\nuser_token 表结构:")
        for col in columns:
            print(f"  {col[0]}: {col[1]}")
    
    conn.close()
    print("\n数据库修复完成")

if __name__ == "__main__":
    asyncio.run(fix_database())
