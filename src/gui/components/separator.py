from collections.abc import Callable
from typing import Any

from gui.element import Element, HTMLElement


class Separator(Element):
    """A draggable separator component for resizing adjacent elements.

    ---

    Authors:
        - Jont
        - Ricky
    """

    def __init__(
        self,
        parent: HTMLElement | Element | None = None,
        on_resize: Callable[[int], None] | None = None,
    ) -> None:
        """Initialize the separator element.

        Args:
            parent: Parent element to attach to
            on_resize: Callback function called with mouse Y position during resize

        ---

        :author: Jont

        """
        super().__init__(
            tag_name="div",
            parent=parent,
            id="separator",
            style="""
            background-color: var(--separator-color);
            width: 100%;
            height: 3px;
            cursor: ns-resize;
            flex-shrink: 0;
            """,
        )
        self.class_name = "separator"

        self._is_dragging = False
        self._on_resize = on_resize

        # Set up event handlers
        self.on("mousemove", self._handle_mouse_move)
        self.on("mousedown", self._handle_mouse_down)
        self.on("mouseup", self._handle_mouse_up)

    def _handle_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse movement for resizing.

        Args:
            event: The mouse event containing the client Y position.

        ---

        :author: Jont

        """
        if not self._is_dragging:
            return

        # Prevent default to avoid interfering with other behaviors
        event.preventDefault()
        event.stopPropagation()

        mouse_y = event.clientY
        if self._on_resize:
            self._on_resize(mouse_y)

    def _handle_mouse_down(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse down to start dragging.

        Args:
            event: The mouse event containing the client Y position.

        ---

        :author: Jont

        """
        if event.button != 0:  # Only handle left mouse button
            return
        self._is_dragging = True
        self["parentElement"].style.userSelect = "none"

        # Prevent default to avoid interfering with other drag behaviors
        event.preventDefault()
        event.stopPropagation()

    def _handle_mouse_up(self, _event: Any) -> None:  # noqa: ANN401
        """Handle mouse up to stop dragging.

        Args:
            _event: The mouse event containing the client Y position.

        ---

        :author: Jont

        """
        if self._is_dragging:
            self._is_dragging = False
            self["parentElement"].style.userSelect = "auto"

    @property
    def is_dragging(self) -> bool:
        """Check if the separator is currently being dragged.

        ---

        :author: Ricky

        """
        return self._is_dragging

    def handle_mouse_up(self, event: Any) -> None:  # noqa: ANN401
        """Public method to handle mouse up event.

        Args:
            event: The mouse event containing the client Y position.

        ---

        :author: Ricky

        """
        self._handle_mouse_up(event)

    def handle_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Public method to handle mouse move event.

        Args:
            event: The mouse event containing the client Y position.

        ---

        :author: Ricky

        """
        self._handle_mouse_move(event)
