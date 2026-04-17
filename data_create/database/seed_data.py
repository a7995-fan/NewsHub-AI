import asyncio
import aiomysql
import random
from datetime import datetime, timedelta

# 生成随机日期
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# 新闻分类数据
categories = [
    {"name": "科技", "sort_order": 1},
    {"name": "娱乐", "sort_order": 2},
    {"name": "体育", "sort_order": 3},
    {"name": "财经", "sort_order": 4},
    {"name": "教育", "sort_order": 5},
    {"name": "健康", "sort_order": 6},
    {"name": "汽车", "sort_order": 7},
    {"name": "房产", "sort_order": 8}
]

# 新闻标题和内容模板
news_templates = [
    {
        "title": "{category}领域最新突破：{tech}技术取得重大进展",
        "content": "据最新消息，{category}领域的{tech}技术取得了重大突破。专家表示，这一突破将对{category}行业产生深远影响，预计将在未来{time}年内改变{category}领域的格局。相关研究团队表示，他们将继续深入研究，争取在{tech}技术上取得更多成果。"
    },
    {
        "title": "{category}行业迎来新机遇：{company}发布新品",
        "content": "{company}近日发布了全新的{product}产品，引起了{category}行业的广泛关注。这款产品采用了最新的{tech}技术，具有{feature1}、{feature2}等特点，预计将在市场上取得不错的销售成绩。分析师表示，{company}的这一举措将为{category}行业带来新的发展机遇。"
    },
    {
        "title": "{category}市场分析：2026年发展趋势预测",
        "content": "根据最新的市场研究报告，2026年{category}市场将呈现{trend1}、{trend2}等发展趋势。报告指出，随着{factor}的不断发展，{category}市场规模预计将达到{value}亿元，年增长率将保持在{rate}%以上。业内专家建议，相关企业应抓住机遇，积极布局，以应对市场的变化。"
    }
]

# 科技词汇
tech_words = ["人工智能", "大数据", "云计算", "区块链", "5G", "物联网", "虚拟现实", "增强现实", "量子计算", "生物技术"]

# 公司名称
companies = ["科技公司A", "科技公司B", "创新科技", "未来科技", "全球科技", "数字科技", "智能科技", "绿色科技", "前沿科技", "科技先锋"]

# 产品名称
products = ["智能手机", "智能手表", "智能音箱", "智能家居系统", "智能汽车", "智能眼镜", "智能机器人", "智能健康设备", "智能教育设备", "智能办公设备"]

# 特点
features = ["高性能", "低功耗", "智能化", "便携性", "安全性", "稳定性", "易用性", "美观性", "多功能", "高性价比"]

# 发展趋势
trends = ["智能化", "数字化", "绿色化", "个性化", "全球化", "融合化", "创新化", "服务化", "平台化", "生态化"]

# 影响因素
factors = ["技术进步", "政策支持", "市场需求", "资本投入", "人才培养", "国际合作", "消费升级", "产业升级", "全球化", "数字化转型"]

# 时间词汇
time_words = ["3-5", "5-10", "10-15", "15-20"]

# 生成随机数值
def random_value():
    return random.randint(100, 10000)

# 生成随机增长率
def random_rate():
    return round(random.uniform(5, 30), 1)

# 生成新闻数据
def generate_news(category_id, category_name, count):
    news_list = []
    for i in range(count):
        template = random.choice(news_templates)
        tech = random.choice(tech_words)
        company = random.choice(companies)
        product = random.choice(products)
        feature1 = random.choice(features)
        feature2 = random.choice(features)
        trend1 = random.choice(trends)
        trend2 = random.choice(trends)
        factor = random.choice(factors)
        time = random.choice(time_words)
        value = random_value()
        rate = random_rate()
        
        title = template["title"].format(
            category=category_name,
            tech=tech,
            company=company,
            product=product
        )
        
        content = template["content"].format(
            category=category_name,
            tech=tech,
            company=company,
            product=product,
            feature1=feature1,
            feature2=feature2,
            trend1=trend1,
            trend2=trend2,
            factor=factor,
            time=time,
            value=value,
            rate=rate
        )
        
        news = {
            "title": title,
            "description": content[:100] + "...",
            "content": content,
            "image": f"https://picsum.photos/800/400?random={i}",
            "author": f"作者{i}",
            "category_id": category_id,
            "views": random.randint(0, 10000),
            "publish_time": random_date(datetime(2025, 1, 1), datetime(2026, 3, 29))
        }
        news_list.append(news)
    return news_list

# 生成用户数据
def generate_users(count):
    users = []
    for i in range(count):
        user = {
            "username": f"user{i+1}",
            "password": "123456",  # 实际应用中应该加密
            "nickname": f"用户{i+1}",
            "avatar": f"https://picsum.photos/100/100?random={i}",
            "gender": random.choice(["male", "female", "unknown"]),
            "bio": f"这是用户{i+1}的个人简介",
            "phone": f"1380013800{i+1}" if i < 10 else f"138001380{i+1}"
        }
        users.append(user)
    return users

async def seed_data():
    # 连接数据库
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='news_app'
    )
    
    async with conn.cursor() as cur:
        # 插入新闻分类（使用 INSERT IGNORE 避免重复）
        print("插入新闻分类...")
        category_ids = []
        for category in categories:
            await cur.execute(
                "INSERT IGNORE INTO news_category (name, sort_order) VALUES (%s, %s)",
                (category["name"], category["sort_order"])
            )
            # 获取分类ID（不管是否新插入）
            await cur.execute("SELECT id FROM news_category WHERE name = %s", (category["name"],))
            category_id = await cur.fetchone()
            if category_id:
                category_ids.append(category_id[0])
        await conn.commit()
        print(f"处理了 {len(categories)} 个新闻分类")
        
        # 插入新闻数据
        print("插入新闻数据...")
        news_ids = []
        for i, category_id in enumerate(category_ids):
            category_name = categories[i]["name"]
            news_list = generate_news(category_id, category_name, 10)  # 每个分类生成10条新闻
            for news in news_list:
                await cur.execute(
                    "INSERT INTO news (title, description, content, image, author, category_id, views, publish_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (news["title"], news["description"], news["content"], news["image"], news["author"], news["category_id"], news["views"], news["publish_time"])
                )
                news_ids.append(cur.lastrowid)
        await conn.commit()
        print(f"插入了 {len(news_ids)} 条新闻")
        
        # 插入用户数据（使用 INSERT IGNORE 避免重复）
        print("插入用户数据...")
        user_ids = []
        users = generate_users(10)  # 生成10个用户
        for user in users:
            await cur.execute(
                "INSERT IGNORE INTO user (username, password, nickname, avatar, gender, bio, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user["username"], user["password"], user["nickname"], user["avatar"], user["gender"], user["bio"], user["phone"])
            )
            # 获取用户ID（不管是否新插入）
            await cur.execute("SELECT id FROM user WHERE username = %s", (user["username"],))
            user_id = await cur.fetchone()
            if user_id:
                user_ids.append(user_id[0])
        await conn.commit()
        print(f"处理了 {len(users)} 个用户")
        
        # 插入收藏数据（使用 INSERT IGNORE 避免重复）
        print("插入收藏数据...")
        favorite_count = 0
        for user_id in user_ids:
            # 每个用户随机收藏1-5条新闻
            favorite_news = random.sample(news_ids, random.randint(1, 5))
            for news_id in favorite_news:
                await cur.execute(
                    "INSERT IGNORE INTO favorite (user_id, news_id) VALUES (%s, %s)",
                    (user_id, news_id)
                )
                favorite_count += 1
        await conn.commit()
        print(f"处理了 {favorite_count} 条收藏记录")
        
        # 插入浏览记录数据（使用 INSERT IGNORE 避免重复）
        print("插入浏览记录数据...")
        history_count = 0
        for user_id in user_ids:
            # 每个用户随机浏览5-10条新闻
            history_news = random.sample(news_ids, random.randint(5, 10))
            for news_id in history_news:
                await cur.execute(
                    "INSERT IGNORE INTO history (user_id, news_id, view_count) VALUES (%s, %s, %s)",
                    (user_id, news_id, random.randint(1, 5))
                )
                history_count += 1
        await conn.commit()
        print(f"处理了 {history_count} 条浏览记录")
    
    conn.close()
    print("\n数据填充完成！")

if __name__ == "__main__":
    asyncio.run(seed_data())
