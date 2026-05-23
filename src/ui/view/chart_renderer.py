from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.ui.view.renderer.base import BaseRenderer, create_renderer

if TYPE_CHECKING:
    from src.ui.view.projection import ViewProjection


class ChartRenderer(BaseRenderer):
    """
    Version-aware proxy renderer that delegates to the consolidated BaseRenderer logic.

    This class maintains compatibility with the existing ChartViewport lifecycle
    by lazily instantiating the core engine once the chart context is available.
    """

    def __init__(
        self,
        projection: ViewProjection,
        total_lanes: int = 16,
        visible_note_types: dict[str, bool] | None = None,
        subdivisions: int = 4,
    ) -> None:
        """Initialize the proxy renderer with its projection and visibility settings."""
        super().__init__(projection, total_lanes, visible_note_types, subdivisions)
        self._delegate: BaseRenderer | None = None

    def draw_notes(self, painter: Any, notes: list[Any], current_position: float) -> None:
        """
        Orchestrate note rendering by delegating to the version-aware engine.
        The engine is lazily instantiated once the chart context is available.
        """
        if not notes or not self.projection.timeline_engine:
            return

        if self._delegate is None:
            # Retrieve the chart from the timeline engine to determine the correct version behavior
            chart = self.projection.timeline_engine.chart
            self._delegate = create_renderer(
                chart, self.projection, self.total_lanes, self.visible_note_types, self.subdivisions
            )

        self._delegate.draw_notes(painter, notes, current_position)

    def draw_lane_lines(self, *args: Any, **kwargs: Any) -> None:
        if self._delegate:
            return self._delegate.draw_lane_lines(*args, **kwargs)
        return super().draw_lane_lines(*args, **kwargs)

    def draw_measure_lines(self, *args: Any, **kwargs: Any) -> None:
        if self._delegate:
            return self._delegate.draw_measure_lines(*args, **kwargs)
        return super().draw_measure_lines(*args, **kwargs)
