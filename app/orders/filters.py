from fastapi_filter.contrib.sqlalchemy import Filter
from app.orders.models import Orders


class OrderFilter(Filter):
    user_id: str | None = None
    category_id: str | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Orders
        search_model_name = ("user_id", "status")
        search_field_name = "q"