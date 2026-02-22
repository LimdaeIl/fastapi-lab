from abc import ABC, abstractmethod
from app.domain.members.entities.member import Member


class MemberRepository(ABC):

    @abstractmethod
    def save(self, member: Member) -> Member:
        """저장 후 DB에서 생성된 id가 반영된 Member를 반환"""
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Member | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, member_id: int) -> Member | None:
        raise NotImplementedError

    @abstractmethod
    def bump_token_version(self, member_id: int) -> None:
        """token_version을 +1 해서 기존 토큰들을 전부 무효화"""
        raise NotImplementedError