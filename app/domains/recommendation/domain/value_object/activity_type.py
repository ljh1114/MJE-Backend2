from enum import Enum


class ActivityType(Enum):
    CORE_ACTIVITY = "CORE_ACTIVITY"
    SUB_ACTIVITY = "SUB_ACTIVITY"


class ActivityKind(Enum):
    # CORE_ACTIVITY — 기본 추천에 우선 사용
    EXHIBITION = ("EXHIBITION", ActivityType.CORE_ACTIVITY)
    WALK = ("WALK", ActivityType.CORE_ACTIVITY)
    SHOPPING = ("SHOPPING", ActivityType.CORE_ACTIVITY)
    POPUP = ("POPUP", ActivityType.CORE_ACTIVITY)
    WORKSHOP = ("WORKSHOP", ActivityType.CORE_ACTIVITY)
    INDOOR_PLAY = ("INDOOR_PLAY", ActivityType.CORE_ACTIVITY)

    # SUB_ACTIVITY — 시간대/코스 흐름에 따라 보조 사용
    MOVIE = ("MOVIE", ActivityType.SUB_ACTIVITY)
    KARAOKE = ("KARAOKE", ActivityType.SUB_ACTIVITY)
    BAR = ("BAR", ActivityType.SUB_ACTIVITY)
    NIGHT_VIEW = ("NIGHT_VIEW", ActivityType.SUB_ACTIVITY)
    SPORTS = ("SPORTS", ActivityType.SUB_ACTIVITY)
    LATE_NIGHT = ("LATE_NIGHT", ActivityType.SUB_ACTIVITY)

    def __new__(cls, value: str, activity_type: ActivityType) -> "ActivityKind":
        obj = object.__new__(cls)
        obj._value_ = value
        obj._activity_type = activity_type
        return obj

    @property
    def activity_type(self) -> ActivityType:
        return self._activity_type

    @property
    def is_core(self) -> bool:
        return self._activity_type == ActivityType.CORE_ACTIVITY

    @classmethod
    def core_activities(cls) -> list["ActivityKind"]:
        return [a for a in cls if a.activity_type == ActivityType.CORE_ACTIVITY]

    @classmethod
    def sub_activities(cls) -> list["ActivityKind"]:
        return [a for a in cls if a.activity_type == ActivityType.SUB_ACTIVITY]
