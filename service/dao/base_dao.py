from service.dao.models import engine
from sqlalchemy.orm import Session


class BaseDao:

    def __init__(self):
        self.session = Session(bind=engine)
