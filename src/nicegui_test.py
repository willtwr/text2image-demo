from nicegui import ui, run
from contextlib import contextmanager
from models.text2image.factory import T2IFactory


t2ifactory = T2IFactory()
t2imodel = None


@contextmanager
def disable_when_init_model(init_model_button: ui.button, init_model_spinner: ui.spinner, model_selector: ui.select, draw_button: ui.button):
    init_model_button.disable()
    init_model_spinner.set_visibility(True)
    model_selector.disable()
    draw_button.disable()
    try:
        yield
    finally:
        init_model_spinner.set_visibility(False)
        model_selector.enable()
        draw_button.enable()


@contextmanager
def disable_when_generating(draw_button: ui.button, drawing_spinner: ui.spinner, img_desc: ui.textarea):
    draw_button.disable()
    drawing_spinner.set_visibility(True)
    img_desc.disable()
    try:
        yield
    finally:
        draw_button.enable()
        drawing_spinner.set_visibility(False)
        img_desc.enable()


async def draw_button_clicked(
        draw_button: ui.button, 
        drawing_spinner: ui.spinner,
        img_desc: ui.textarea, 
        img_holder: ui.image,
        notification: ui.label
) -> None:
    if t2imodel is None:
        notification.set_text("Please select and initialize a model.")
        notification.set_visibility(True)
        return

    with disable_when_generating(draw_button, drawing_spinner, img_desc):
        image = await run.io_bound(t2imodel, prompt=img_desc.value)
        img_holder.set_source(image)


async def init_model_button_clicked(
    init_model_button: ui.button,
    init_model_spinner: ui.spinner,
    model_selector: ui.select,
    draw_button: ui.button,
    notification: ui.label
) -> None:
    notification.set_visibility(False)
    with disable_when_init_model(init_model_button, init_model_spinner, model_selector, draw_button):
        global t2imodel
        t2imodel = t2ifactory.get_t2i_model(model_selector.value)
        t2imodel = await run.io_bound(t2imodel)


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    with ui.column().classes('w-full items-center'):
        ui.label("Text to Image Demo").style('color: #6E93D6; font-size: 300%; font-weight: 300')
        with ui.card().classes('w-full max-w-screen-lg'):
            img_desc = ui.textarea(placeholder="Describe what you want to draw here...").classes('w-full').props('rounded outlined clearable')
            with ui.row():
                model_selector = ui.select(list(t2ifactory.get_t2i_models_list().keys()), value='Flux.1', on_change=lambda: init_model_button.enable()).props('outlined')
                
                init_model_button = ui.button('Initialize Model', on_click=lambda e: init_model_button_clicked(e.sender, init_model_spinner, model_selector, draw_button, notification))
                init_model_spinner = ui.spinner(size='lg')
                init_model_spinner.set_visibility(False)

                with ui.column():
                    draw_button = ui.button('Draw', on_click=lambda e: draw_button_clicked(e.sender, drawing_spinner, img_desc, img_holder, notification))
                    notification = ui.label()
                    notification.set_visibility(False)

                drawing_spinner = ui.spinner(size='lg')
                drawing_spinner.set_visibility(False)

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg'):
            img_holder = ui.image()


ui.run()
