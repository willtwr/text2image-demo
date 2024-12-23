import replicate 
from nicegui import ui
from nicegui.events import UploadEventArguments


ui.dark_mode()


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    def draw_button_clicked():
        desc.set_text(img_desc.value)
        img.set_source('./assets/sd-example1.png')

    with ui.column().classes('w-full items-center'):
        ui.label("Text to Image Demo").style('color: #6E93D6; font-size: 300%; font-weight: 300')
        with ui.card().classes('w-full max-w-screen-lg'):
            img_desc = ui.textarea(placeholder="Describe what you want to draw here...").classes('w-full').props('rounded outlined clearable')

            with ui.button_group():
                ui.button('Draw', on_click=lambda: draw_button_clicked())

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg'):
            img = ui.image()
            desc = ui.label()

ui.run()
