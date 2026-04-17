import asyncio
import aiomysql

async def check_database_details():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 检查新闻分类
        print("=== 新闻分类 ===")
        await cur.execute("SELECT id, name, sort_order FROM news_category ORDER BY sort_order")
        categories = await cur.fetchall()
        for cat in categories:
            print(f"ID: {cat[0]}, 名称: {cat[1]}, 排序: {cat[2]}")
        print()
        
        # 检查每个分类下的新闻数量
        print("=== 各分类新闻数量 ===")
        for cat in categories:
            await cur.execute("SELECT COUNT(*) FROM news WHERE category_id = %s", (cat[0],))
            count = await cur.fetchone()
            print(f"{cat[1]}: {count[0]} 条新闻")
        print()
        
        # 检查用户信息
        print("=== 用户信息 ===")
        await cur.execute("SELECT id, username, nickname, phone FROM user LIMIT 5")
        users = await cur.fetchall()
        for user in users:
            print(f"ID: {user[0]}, 用户名: {user[1]}, 昵称: {user[2]}, 手机: {user[3]}")
        print()
        
        # 检查收藏记录
        print("=== 收藏记录统计 ===")
        await cur.execute("SELECT COUNT(DISTINCT user_id) FROM favorite")
        user_count = await cur.fetchone()
        await cur.execute("SELECT COUNT(*) FROM favorite")
        total_count = await cur.fetchone()
        print(f"收藏用户数: {user_count[0]}, 总收藏数: {total_count[0]}")
        print()
        
        # 检查浏览记录
        print("=== 浏览记录统计 ===")
        await cur.execute("SELECT COUNT(DISTINCT user_id) FROM history")
        user_count = await cur.fetchone()
        await cur.execute("SELECT COUNT(*) FROM history")
        total_count = await cur.fetchone()
        print(f"浏览用户数: {user_count[0]}, 总浏览数: {total_count[0]}")
        print()
        
        # 检查最新新闻
        print("=== 最新5条新闻 ===")
        await cur.execute("""
            SELECT n.id, n.title, nc.name, n.author, n.views, n.publish_time 
            FROM news n 
            JOIN news_category nc ON n.category_id = nc.id 
            ORDER BY n.publish_time DESC 
            LIMIT 5
        """)
        news_list = await cur.fetchall()
        for news in news_list:
            print(f"ID: {news[0]}, 标题: {news[1][:30]}..., 分类: {news[2]}, 作者: {news[3]}, 浏览: {news[4]}, 时间: {news[5]}")
        print()
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(check_database_details())
