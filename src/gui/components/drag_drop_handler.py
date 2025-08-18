from collections.abc import Callable
from typing import Any

from gui.element import Element


class DragDropHandler:
    """Handles drag and drop functionality for file uploads.

    ---

    Authors:
        - Ricky
    """

    def __init__(
        self,
        element: Element,
        on_file_drop: Callable[[Any], None],
        on_drag_enter: Callable[[], None] | None = None,
        on_drag_leave: Callable[[], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """Initialize drag drop handler element.

        Args:
            element: The element to attach drag/drop events to
            on_file_drop: Callback function when a file is dropped
            on_drag_enter: Optional callback when drag enters
            on_drag_leave: Optional callback when drag leaves
            on_error: Optional callback for error handling

        ---

        :author: Ricky

        """
        self.element = element
        self.on_file_drop = on_file_drop
        self.on_drag_enter = on_drag_enter
        self.on_drag_leave = on_drag_leave
        self.on_error = on_error
        self.drag_overlay = None

    def setup_drag_overlay(self) -> Element:
        """Create and return the drag overlay element.

        ---

        :author: Ricky

        """
        self.drag_overlay = Element(
            "div",
            parent=self.element,
            style="""
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 123, 255, 0.1);
            border: 2px dashed #007bff;
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 10;
            """,
        )

        overlay_text = Element(
            "div",
            parent=self.drag_overlay,
            style="""
            font-size: 24px;
            color: #007bff;
            font-weight: bold;
            text-align: center;
            user-select: none;
            """,
        )
        overlay_text.text = "Drop image here"

        return self.drag_overlay

    def setup_events(self) -> None:
        """Set up drag and drop event handlers.

        ---

        :author: Ricky

        """
        self.element.on("dragover", self._handle_drag_over)
        self.element.on("dragenter", self._handle_drag_enter)
        self.element.on("dragleave", self._handle_drag_leave)
        self.element.on("drop", self._handle_drop)

    def _handle_drag_over(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag over event.

        Args:
            event: The mouse drag event

        ---

        :author: Ricky

        """
        event.preventDefault()
        event.stopPropagation()

    def _handle_drag_enter(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag enter event.

        Args:
            event: The mouse drag event

        ---

        :author: Ricky

        """
        event.preventDefault()
        event.stopPropagation()

        if self.drag_overlay:
            self.drag_overlay["style"].display = "flex"
        self.element["style"].borderColor = "#007bff"

        # Call the optional drag enter callback
        if self.on_drag_enter:
            self.on_drag_enter()

    def _handle_drag_leave(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag leave event.

        Args:
            event: The mouse drag event

        ---

        :author: Ricky

        """
        event.preventDefault()
        event.stopPropagation()

        # Only hide overlay if we're leaving the container
        try:
            related_target = event.relatedTarget
            if related_target is None or not self.element.html_element.contains(
                related_target,
            ):
                if self.drag_overlay:
                    self.drag_overlay["style"].display = "none"
                self.element["style"].borderColor = "transparent"

                # Call the optional drag leave callback
                if self.on_drag_leave:
                    self.on_drag_leave()
        except (AttributeError, TypeError):
            # If there's any issue accessing relatedTarget, just hide the overlay
            if self.drag_overlay:
                self.drag_overlay["style"].display = "none"
            self.element["style"].borderColor = "transparent"

            # Call the optional drag leave callback
            if self.on_drag_leave:
                self.on_drag_leave()

    def _handle_drop(self, event: Any) -> None:  # noqa: ANN401
        """Handle file drop event.

        Args:
            event: The mouse drag event

        ---

        :author: Ricky

        """
        event.preventDefault()
        event.stopPropagation()

        if self.drag_overlay:
            self.drag_overlay["style"].display = "none"
        self.element["style"].borderColor = "transparent"

        files = event.dataTransfer.files
        if files.length > 0:
            file = files.item(0)
            if file.type.startswith("image/"):
                self.on_file_drop(file)
            else:
                error_msg = "Please drop an image file (PNG, JPG, etc.)"
                if self.on_error:
                    self.on_error(error_msg)
                else:
                    print(error_msg)
