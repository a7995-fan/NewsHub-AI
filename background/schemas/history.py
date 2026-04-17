from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


# 浏览记录新闻项响应模型
class HistoryNewsItemResponse(NewsItemBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")
    view_count: int = Field(alias="viewCount")
    category_name: str = Field(alias="categoryName")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# 浏览记录列表接口响应模型
class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
