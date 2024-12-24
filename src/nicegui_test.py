from nicegui import ui, run, app
from contextlib import contextmanager
# from models.text2image.stable_diffusion_art import StableDiffusionArt
from models.text2image.stable_diffusion import StableDiffusion


def init_model() -> None:
    global model
    # model = StableDiffusionArt()
    model = StableDiffusion()


@contextmanager
def disable_when_generating(button: ui.button, spinner: ui.spinner, textbox: ui.textarea):
    button.disable()
    spinner.set_visibility(True)
    textbox.disable()
    try:
        yield
    finally:
        button.enable()
        spinner.set_visibility(False)
        textbox.enable()
    


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    async def draw_button_clicked(button: ui.button, spinner: ui.spinner, textbox: ui.textarea) -> None:
        with disable_when_generating(button, spinner, textbox):
            image = await run.io_bound(model, prompt=img_desc.value)
            img.set_source(image)
            desc.set_text(img_desc.value)

    with ui.column().classes('w-full items-center'):
        ui.label("Text to Image Demo").style('color: #6E93D6; font-size: 300%; font-weight: 300')
        with ui.card().classes('w-full max-w-screen-lg'):
            img_desc = ui.textarea(placeholder="Describe what you want to draw here...").classes('w-full').props('rounded outlined clearable')

            with ui.row():
                ui.button('Draw', on_click=lambda e: draw_button_clicked(e.sender, img_spinner, img_desc))
                img_spinner = ui.spinner(size='lg')
                img_spinner.set_visibility(False)

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg'):
            img = ui.image()
            desc = ui.label()


app.on_startup(init_model)
ui.run()
