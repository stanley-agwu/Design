# Design a Ride Sharing System

# A ride sharing system manages requests from riders and availability
# from drivers. Riders request ride, and drivers become available over 
# time. The system should match riders and drivers in the order they arrive.

from collections import deque
from enum import Enum

class State(Enum):
    WAITING = 'Waiting'
    MATCHED = 'Matched'
    CANCELLED = 'Cancelled'

class RideSharingSystem:
    def __init__(self):
        self.riders = deque() # Riders Queue
        self.drivers = deque() # Drivers Queue
        # state: 1 = waiting, 2 = matched, 3 = canceled
        self.state: dict[int, str] = {}

    def add_ride(self, rider_id: int) -> None:
        self.riders.append(rider_id)
        self.state[rider_id] = State.WAITING

    def add_driver(self, driver_id: int) -> None:
        self.drivers.append(driver_id)

    def _remove_canceled_rides_before_match(self) -> None:
        # remove canceled rides still sitting in Queue
        while self.riders and self.state.get(self.riders[0], '') == State.CANCELLED:
            self.riders.popleft()

    def match_driver_with_rider(self) -> list[int]:
        if not self.riders or not self.drivers:
            return [-1, -1]
        self._remove_canceled_rides_before_match()

        rider_id = self.riders.popleft()
        driver_id = self.drivers.popleft()
        self.state[rider_id] = State.MATCHED # matched
        return [driver_id, rider_id]

    def cancel_ride(self, rider_id: int) -> None:
        # only cancel if rider exists and is still waiting
        if self.state.get(rider_id, '') == State.WAITING:
            self.state[rider_id] = State.CANCELLED

# Complexities
"""
Let R = Number of Riders, D = Number of Drivers

Time complexity
addRide, addDriver, cancelRide: O(1)
matchDriverWithRider: amortized O(1) (each canceled rider is popped at most once)

Space Complexity: O(R + D) for queued IDs and state map.
"""