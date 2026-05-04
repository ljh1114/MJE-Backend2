import json
from dataclasses import asdict
from typing import Optional

from redis.asyncio import Redis

from app.domains.recommendation.repository.recommendation_session_repository_interface import (
    RecommendationSessionRepositoryInterface,
)
from app.domains.recommendation.service.dto.recommendation_session_dto import RecommendationSessionDto
from app.infrastructure.cache.redis_client import get_redis

_SESSION_TTL_SECONDS = 60 * 60 * 6


class RedisRecommendationSessionRepository(RecommendationSessionRepositoryInterface):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    async def save(self, session: RecommendationSessionDto) -> None:
        payload = json.dumps(asdict(session), ensure_ascii=False)

        for course in session.courses:
            await self._redis.setex(
                self._build_key(course.course_id),
                _SESSION_TTL_SECONDS,
                payload,
            )

    async def find_by_course_id(self, course_id: str) -> Optional[RecommendationSessionDto]:
        raw = await self._redis.get(self._build_key(course_id))
        if raw is None:
            return None

        data = json.loads(raw)
        return RecommendationSessionDto.from_dict(data)

    def _build_key(self, course_id: str) -> str:
        return f"recommendation:course:{course_id}"


async def get_recommendation_session_repository() -> RedisRecommendationSessionRepository:
    redis_client = await get_redis()
    return RedisRecommendationSessionRepository(redis_client)
