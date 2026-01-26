from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.models import Base, IntIdMixin, TimeActionMixin


class Categories(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "categories"

    name = Column(String(512), nullable=False)
    description = Column(String(1024), nullable=False)


