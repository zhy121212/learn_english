"""
定义连接mysql的数据库 sqlmodel连接
"""

# 定义表模型

from sqlmodel import SQLModel, Session, Field, create_engine
from fastapi import Depends
from typing import Annotated


class English(SQLModel, table=True):
    e_id: int | None = Field(default=None, primary_key=True)
    e_word: str = Field(index=True)
    e_translation: str = Field(index=True)

    def __str__(self):
        return f'单词{self.e_word}, 对应的意思为{self.e_translation}'


# sqlmodel连接的网址

# 先创建引擎

url = 'sqlite:///db.db'
engine = create_engine(url)

# 创建表
SQLModel.metadata.create_all(engine)


# 创建会话
def create_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(create_session)]
