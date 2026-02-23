from app.domain.members.entities.member import Member
from app.domain.members.repositories.member_repository import MemberRepository
from app.common.security.password import hash_password
from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode


class SignupUseCase:
    def __init__(self, member_repo: MemberRepository):
        self.member_repo = member_repo

    def execute(self, email: str, password: str) -> Member:
        existing = self.member_repo.find_by_email(email)
        if existing:
            raise AppException(
                code=ErrorCode.EMAIL_ALREADY_EXISTS,
                message="Email already exists",
                status_code=409,
            )

        password_hash = hash_password(password)
        member = Member.create(email=email, password_hash=password_hash)
        return self.member_repo.save(member)
