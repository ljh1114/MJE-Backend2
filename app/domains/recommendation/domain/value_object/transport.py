from enum import Enum


class Transport(Enum):
    WALK = "walk"
    PUBLIC_TRANSIT = "public_transit"
    CAR = "car"

    @property
    def base_move_minutes(self) -> int:
        _move_times = {
            Transport.WALK: 20,
            Transport.PUBLIC_TRANSIT: 15,
            Transport.CAR: 10,
        }
        return _move_times[self]
