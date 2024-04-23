from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.db import db


class Todo(db.Model):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(String(100), nullable=False)
    check = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Todo:[id:{self.id}, title:{self.title}, content:{self.content}, check:{self.check}, user:{self.user}]>"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "check": self.check,
            "user": self.user_id,
        }
