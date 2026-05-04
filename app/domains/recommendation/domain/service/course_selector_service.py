from typing import List, Optional, Tuple

from app.domains.recommendation.domain.service.course_ordering_service import OrderedCourseResult
from app.domains.recommendation.domain.service.course_scorer_service import CourseScorerService
from app.domains.recommendation.domain.value_object.scored_course import ScoredCourse
from app.domains.recommendation.domain.value_object.time_slot import TimeSlot
from app.domains.recommendation.domain.value_object.transport import Transport


class CourseSelectorService:
    def __init__(self) -> None:
        self._scorer = CourseScorerService()

    def select(
        self,
        ordered_results: List[OrderedCourseResult],
        time_slot: TimeSlot,
        transport: Transport,
    ) -> Tuple[Optional[ScoredCourse], List[ScoredCourse]]:
        if not ordered_results:
            return None, []

        scored = sorted(
            [self._scorer.score(r, time_slot, transport) for r in ordered_results],
            key=lambda c: c.total_score,
            reverse=True,
        )

        best = scored[0]
        best_ids = best.place_ids()

        optionals = sorted(
            [
                self._scorer.score(c.ordered_result, time_slot, transport, best_ids)
                for c in scored[1:]
            ],
            key=lambda c: c.total_score,
            reverse=True,
        )[:2]

        return best, optionals
