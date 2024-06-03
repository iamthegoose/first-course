# repositoryflat.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services.models.flat import Flat
import logging

logging.basicConfig(level=logging.DEBUG)


class FlatRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def create_flat(self, flat: Flat) -> bool:
        try:
            self.sess.add(flat)
            self.sess.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error creating flat: {e}")
            self.sess.rollback()
            return False
        finally:
            self.sess.close()
        return True

    def get_all_flats(self, filters=None, order_by=None):
        query = self.sess.query(Flat)
        if filters:
            for key, value in filters.items():
                if key == "name":
                    query = query.filter(Flat.name.ilike(f"%{value}%"))
                elif key == "location":
                    query = query.filter(Flat.location.ilike(f"%{value}%"))
                elif key == "area_min":
                    query = query.filter(Flat.area >= value)
                elif key == "area_max":
                    query = query.filter(Flat.area <= value)
                elif key == "price_min":
                    query = query.filter(Flat.price >= value)
                elif key == "price_max":
                    query = query.filter(Flat.price <= value)
                elif key == "rooms":
                    query = query.filter(Flat.rooms == value)
        if order_by:
            query = query.order_by(order_by)
        return query.all()

    def get_flats_by_user_id(self, user_id: int):
        try:
            return self.sess.query(Flat).filter(Flat.user_id == user_id).all()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching flats: {e}")
            return []
