from dataclasses import dataclass

@dataclass
class Ride:
    rideable_type: str
    start_station_id: int
    end_station_id: int
    ride_id: int = None
    start_station_name: str = None
    end_station_name: str = None
    started_at: str = None
    ended_at: str = None
    member_casual: str = None