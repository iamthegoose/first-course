from typing import Dict, Any
from app.services.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.DEBUG)


class UserRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def create_user(self, signup: User) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error creating user: {e}")
            self.sess.rollback()
            return False
        finally:
            self.sess.close()
        return True

    def get_user_by_id(self, user_id):
        return self.sess.query(User).filter(User.id == user_id).first()

    def get_user(self):
        return self.sess.query(User).all()

    def get_user_by_email(self, email: str):
        return self.sess.query(User).filter(User.email == email).first()

    def update_user(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(User).filter(
                User.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True

    def delete_user(self, id: int) -> bool:
        try:
            self.sess.query(User).filter(User.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True
