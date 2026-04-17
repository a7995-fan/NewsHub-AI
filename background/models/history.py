from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    浏览记录表ORM模型
    """
    __tablename__ = 'history'

    # 创建索引
    # 联合唯一约束：一个用户对同一新闻只有一条浏览记录，但会更新浏览时间
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_history_unique'),
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="浏览记录ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="浏览时间")
    view_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="浏览次数")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
