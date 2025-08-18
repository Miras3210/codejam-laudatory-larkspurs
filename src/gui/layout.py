from typing import Any

from gui.components.description import Description
from gui.components.image_preview import ImagePreview
from gui.components.separator import Separator
from gui.components.terminal_gui import TerminalGui
from gui.element import Element, HTMLElement
from image import PaintImage
from terminal import Terminal


class Layout(Element):
    """Main layout component that manages image preview and terminal sections with a resizable separator.

    ---

    Authors:
        - Jont
        - Ricky
    """

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        """Initialize the main layout component.

        Args:
            parent: Optional parent element that will contain this layout. If `None`, it becomes a
                root component.
        ---

        :author: Jont

        """
        super().__init__(
            tag_name="div",
            parent=parent,
            style="""
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100%;
            """,
        )

        self.description = Description(parent=self)
        self.image_preview = ImagePreview(parent=self)
        self.separator = Separator(parent=self, on_resize=self._handle_resize)
        self.terminal_gui = TerminalGui(parent=self)

        image = PaintImage(self.image_preview)
        self.image_preview.image = image

        image.load()

        # create a terminal
        self.terminal = Terminal(image, self.terminal_gui)

    def _handle_resize(self, mouse_y: int) -> None:
        """Handle resizing of the image preview section.

        Args:
            mouse_y: Mouse Y position for calculating new height

        ---

        :author: Ricky

        """
        self.image_preview["style"].height = f"{mouse_y}px"

    def handle_global_mouse_up(self, event: Any) -> None:  # noqa: ANN401
        """Handle global mouse up event to stop separator dragging.

        Args:
            event: Mouse event data triggering the end of the drag.

        ---

        :author: Ricky

        """
        self.separator.handle_mouse_up(event)

    def handle_global_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Handle global mouse move event for separator dragging.

        Args:
            event: Mouse event data triggering the start of the drag.

        ---

        :author: Ricky

        """
        self.separator.handle_mouse_move(event)
