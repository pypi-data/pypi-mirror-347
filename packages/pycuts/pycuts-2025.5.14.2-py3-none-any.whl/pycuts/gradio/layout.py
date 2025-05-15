# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import gradio as gr

class _Spacer:
    """
    Internal Spacer class for layout spacing in Gradio blocks.
    """

    def __init__(
        self,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        scale: int | None = 1,
        height: int | str | None = None,
        max_height: int | str | None = None,
        min_width: int = 320,
        min_height: int | str | None = None,
    ) -> None:
        self.elem_id = elem_id
        self.elem_classes = elem_classes
        self.scale = scale
        self.height = height
        self.max_height = max_height
        self.min_width = min_width
        self.min_height = min_height

    def __call__(self) -> None:
        with gr.Row(
            elem_id=self.elem_id,
            elem_classes=self.elem_classes,
            scale=self.scale,
            height=self.height,
            max_height=self.max_height,
            min_height=self.min_height,
        ):
            with gr.Column(
                scale=max(1, self.scale or 0),
                min_width=self.min_width,
                visible=self.visible,
                elem_classes=self.elem_classes,
                show_progress=False,
            ):
                gr.Markdown(
                    "",
                    show_label=False,
                    elem_classes=self.elem_classes,
                    height=self.height,
                    max_height=self.max_height,
                    min_height=self.min_height,
                    show_copy_button=False,
                    container=False,
                )

@staticmethod
def Spacer(**kwargs) -> None:
    """
    Spacer utility to insert visual empty space in a Gradio layout.
    
    Args:
        elem_id (str): 
            An optional string that is assigned as the id of this component in the HTML DOM. 
            Can be used for targeting CSS styles.
        elem_classes (list[str]): 
            An optional string or list of strings that are assigned as the class of this component in the HTML DOM. 
            Can be used for targeting CSS styles.
        scale (int):
            Relative size compared to adjacent Components. 
            For example if Components A and B are in a Row, and A has `scale=2`, and B has `scale=1`, 
            A will be twice as wide as B. Should be an integer.
            scale applies in Rows, and to top-level Components in Blocks where `fill_height=True`.
        height (int):
            The height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. 
            If content exceeds the height, the row will scroll vertically. 
            If not set, the component will expand to fit the content.
        max_height (int):
            The maximum height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. 
            If content exceeds the height, the component will scroll vertically. 
            If content is shorter than the height, the component will shrink to fit the content. 
            Will not have any effect if `height` is set and is smaller than `max_height`.
        min_width (int):
            Minimum pixel width of the component, will wrap if not sufficient screen space to satisfy this value. 
            If a certain scale value results in a column narrower than `min_width`, the `min_width` parameter will be respected first.
        min_height (int):
            The minimum height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. 
            If content exceeds the height, the component will expand to fit the content. 
            Will not have any effect if `height` is set and is larger than `min_height`.
    """
    return _Spacer(**kwargs)()


