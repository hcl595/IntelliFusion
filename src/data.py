# models.py
from sqlalchemy import create_engine,Column,Integer,String,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os

# 基础类
basedir= os.path.abspath(os.path.dirname(__file__)) + "\\data"
file_path = Path(__file__).parent / "data\models.sqlite"
Base = declarative_base()
engine = create_engine('sqlite:///'+os.path.join(basedir,'models.sqlite'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class userInfo(Base):
    # 数据库中存储的表名
    __tablename__ = "userInfo"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    account = Column(String(32), index=True, nullable=False, comment="姓名")
    password = Column(String(32), nullable=False, comment="密码")
    mail = Column(String(32), index=True, nullable=True, comment="邮箱")
    __table__args__ = (
        UniqueConstraint("id", "name"),  # 联合唯一约束
        Index("name", unique=True),       # 联合唯一索引
    )



    def __str__(self):
        return f"object : <id:{self.id} name:{self.name} key:{self.key}>"


class models(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    type = Column(String(32), nullable=False, comment="类型")
    comment = Column(String(32), nullable=False, comment="备注")
    url = Column(String(32), nullable=False, comment="地址")
    port = Column(Integer, nullable=False, comment="端口")
    LaunchUrl = Column(String(32), nullable=False, comment="启动地址")
    __table__args__ = (
        UniqueConstraint("id", "url"),  # 联合唯一约束
        Index("url", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} url:{self.url}>"


def setup():
    if not file_path.exists():
        print("database doesn't exist,creating database.")
        f = open(file_path,'w')
        Base.metadata.create_all(engine)
        user_instance = userInfo(
        account="admin",
        password="admin1234",
        )
        session.add(user_instance)
        BasisModel = models(
        type = "LLM",
        comment = "ChatGLM",
        url = "127.0.0.1",
        port = "18356",
        LaunchUrl = ".\\ChatGLM\\api.py"
        )
        session.add(BasisModel)
        session.commit() 
        print("database successfully setup!")

if __name__ == "__main__":
    setup()