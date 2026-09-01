#!/bin/env python3

"""A tiny Python DSL for expressing railway-system tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import unittest


@dataclass(frozen=True)
class SetRoute:
    """Request that the interlocking sets a route between two signals."""

    start_signal: str
    end_signal: str


@dataclass(frozen=True)
class CancelRoute:
    """Request that an already-set route is cancelled."""

    route_name: str


@dataclass(frozen=True)
class MovePoints:
    """Request that points are moved to a target position."""

    point_name: str
    position: str


RailwayAction = SetRoute | CancelRoute | MovePoints


class RailwayTest:
    """Collect railway actions in the order a test should execute them."""

    def __init__(self) -> None:
        self._actions: list[RailwayAction] = []

    def set_route(self, start_signal: str, end_signal: str) -> RailwayTest:
        self._actions.append(SetRoute(start_signal, end_signal))
        return self

    def cancel_route(self, route_name: str) -> RailwayTest:
        self._actions.append(CancelRoute(route_name))
        return self

    def move_points(self, point_name: str, position: str) -> RailwayTest:
        self._actions.append(MovePoints(point_name, position))
        return self

    @property
    def actions(self) -> tuple[RailwayAction, ...]:
        return tuple(self._actions)

    def extend(self, actions: Iterable[RailwayAction]) -> RailwayTest:
        self._actions.extend(actions)
        return self


class RailwayTestDslTests(unittest.TestCase):
    def test_expresses_route_and_point_actions_in_order(self) -> None:
        scenario = (
            RailwayTest()
            .set_route("S1", "S2")
            .move_points("P1", "normal")
            .cancel_route("S1-S2")
        )

        self.assertEqual(
            scenario.actions,
            (
                SetRoute("S1", "S2"),
                MovePoints("P1", "normal"),
                CancelRoute("S1-S2"),
            ),
        )

    def test_can_extend_with_prebuilt_actions(self) -> None:
        scenario = RailwayTest().extend(
            [
                MovePoints("P2", "reverse"),
                SetRoute("S3", "S4"),
            ]
        )

        self.assertEqual(
            scenario.actions,
            (
                MovePoints("P2", "reverse"),
                SetRoute("S3", "S4"),
            ),
        )


if __name__ == "__main__":
    unittest.main()
