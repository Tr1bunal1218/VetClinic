from pydantic import EmailStr
from sqlalchemy import select

from src.models.user_model import UsersOrm
from src.repository.baseRep import BaseRepository
from src.shemas.user import User, UserHashedPass

class UserRepository(BaseRepository):
    model = UsersOrm
    chema = User

    async def get_user_with_hashed_pass(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model: return None
        return UserHashedPass.model_validate(model, from_attributes=True)