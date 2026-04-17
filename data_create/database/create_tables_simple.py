import asyncio
import aiomysql

async def create_tables():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 创建用户表（没有外键）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
                username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
                nickname VARCHAR(50) COMMENT '昵称',
                avatar VARCHAR(255) DEFAULT 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg' COMMENT '头像URL',
                gender ENUM('male', 'female', 'unknown') DEFAULT 'unknown' COMMENT '性别',
                bio VARCHAR(500) DEFAULT '这个人很懒，什么都没留下' COMMENT '个人简介',
                phone VARCHAR(20) UNIQUE COMMENT '手机号',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("用户表创建完成")
        
        # 创建用户令牌表（有外键依赖用户表）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS user_token (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '令牌ID',
                user_id INT NOT NULL COMMENT '用户ID',
                token VARCHAR(255) NOT NULL UNIQUE COMMENT '令牌',
                expires_at DATETIME NOT NULL COMMENT '过期时间',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("用户令牌表创建完成")
        
        # 创建新闻分类表（没有外键）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS news_category (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
                name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
                sort_order INT DEFAULT 0 COMMENT '排序',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("新闻分类表创建完成")
        
        # 创建新闻表（有外键依赖新闻分类表）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '新闻ID',
                title VARCHAR(255) NOT NULL COMMENT '新闻标题',
                description VARCHAR(500) COMMENT '新闻简介',
                content TEXT NOT NULL COMMENT '新闻内容',
                image VARCHAR(255) COMMENT '封面图片URL',
                author VARCHAR(50) COMMENT '作者',
                category_id INT NOT NULL COMMENT '分类ID',
                views INT DEFAULT 0 COMMENT '浏览量',
                publish_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                FOREIGN KEY (category_id) REFERENCES news_category(id) ON DELETE CASCADE,
                INDEX idx_category (category_id),
                INDEX idx_publish_time (publish_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("新闻表创建完成")
        
        # 创建收藏表（有外键依赖用户表和新闻表）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS favorite (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '收藏ID',
                user_id INT NOT NULL COMMENT '用户ID',
                news_id INT NOT NULL COMMENT '新闻ID',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE,
                UNIQUE KEY user_news_unique (user_id, news_id),
                INDEX idx_user (user_id),
                INDEX idx_news (news_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("收藏表创建完成")
        
        # 创建浏览记录表（有外键依赖用户表和新闻表）
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '浏览记录ID',
                user_id INT NOT NULL COMMENT '用户ID',
                news_id INT NOT NULL COMMENT '新闻ID',
                view_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '浏览时间',
                view_count INT DEFAULT 1 COMMENT '浏览次数',
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE,
                UNIQUE KEY user_news_history_unique (user_id, news_id),
                INDEX idx_user (user_id),
                INDEX idx_news (news_id),
                INDEX idx_view_time (view_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("浏览记录表创建完成")
        
        await conn.commit()
    
    conn.close()
    print("\n所有表创建完成")

if __name__ == "__main__":
    asyncio.run(create_tables())
