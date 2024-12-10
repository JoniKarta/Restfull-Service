from typing import Literal

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int = Field(default=1, gt=0)
    size: int = Field(default=10, gt=0)
    order_by: Literal["country", "name", "created_at"] = "name"
    desc: bool = False

    def offset(self):
        return (self.page - 1) * self.size