from nicegui import ui, run, app
from contextlib import contextmanager
from models.text2image.factory import T2IFactory


t2ifactory = T2IFactory()
t2imodel = None  # Not implementing app.storage here to avoid accidentally load multiple models into my potato GPU.


@contextmanager
def disable_when_init_model(init_model_button: ui.button, init_model_spinner: ui.spinner, model_selector: ui.select, draw_button: ui.button):
    init_model_button.disable()
    init_model_spinner.set_visibility(True)
    model_selector.disable()
    draw_button.disable()
    try:
        yield
    finally:
        init_model_button.enable()
        init_model_spinner.set_visibility(False)
        model_selector.enable()
        draw_button.enable()


@contextmanager
def disable_when_generating(draw_button: ui.button, drawing_spinner: ui.spinner, img_desc: ui.textarea, model_selector: ui.select, init_model_button: ui.button):
    draw_button.disable()
    drawing_spinner.set_visibility(True)
    img_desc.disable()
    model_selector.disable()
    init_model_button.disable()
    try:
        yield
    finally:
        draw_button.enable()
        drawing_spinner.set_visibility(False)
        img_desc.enable()
        model_selector.enable()
        init_model_button.enable()


async def draw_button_clicked(
        draw_button: ui.button, 
        drawing_spinner: ui.spinner,
        img_desc: ui.textarea, 
        img_holder: ui.image,
        draw_notification: ui.label,
        model_selector: ui.select,
        init_model_button: ui.button,
        init_model_notification: ui.label
) -> None:
    if t2imodel is None:
        draw_notification.set_text("Please select and initialize a model.")
        draw_notification.set_visibility(True)
        return

    init_model_notification.set_visibility(False)
    with disable_when_generating(draw_button, drawing_spinner, img_desc, model_selector, init_model_button):
        image = await run.io_bound(t2imodel, prompt=img_desc.value)
        img_holder.set_source(image)


async def init_model_button_clicked(
    init_model_button: ui.button,
    init_model_spinner: ui.spinner,
    model_selector: ui.select,
    draw_button: ui.button,
    draw_notification: ui.label,
    init_model_notification: ui.label
) -> None:
    draw_notification.set_visibility(False)
    if app.storage.user['current_model'] == model_selector.value:
        init_model_notification.set_text("Already loaded this model.")
        init_model_notification.set_visibility(True)
        return

    app.storage.user['current_model'] = model_selector.value
    init_model_notification.set_visibility(False)
    with disable_when_init_model(init_model_button, init_model_spinner, model_selector, draw_button):
        global t2imodel
        t2imodel = t2ifactory.get_t2i_model(model_selector.value)
        t2imodel = await run.io_bound(t2imodel)


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    app.storage.user['current_model'] = None

    with ui.column().classes('w-full items-center'):
        ui.label("Text to Image Demo").style('color: #6E93D6; font-size: 300%; font-weight: 300')
        with ui.card().classes('w-full max-w-screen-lg'):
            img_desc = ui.textarea(placeholder="Describe what you want to draw here...").classes('w-full').props('rounded outlined clearable')
            with ui.row():
                model_selector = ui.select(list(t2ifactory.get_t2i_models_list().keys()), value='Flux.1', on_change=lambda: init_model_button.enable()).props('outlined')
                
                with ui.column():
                    init_model_button = ui.button('Initialize Model', on_click=lambda e: init_model_button_clicked(e.sender, init_model_spinner, model_selector, draw_button, draw_notification, init_model_notification))
                    init_model_notification = ui.label()
                    init_model_notification.set_visibility(False)
                
                init_model_spinner = ui.spinner(size='lg')
                init_model_spinner.set_visibility(False)

                with ui.column():
                    draw_button = ui.button('Draw', on_click=lambda e: draw_button_clicked(e.sender, drawing_spinner, img_desc, img_holder, draw_notification, model_selector, init_model_button, init_model_notification))
                    draw_notification = ui.label()
                    draw_notification.set_visibility(False)

                drawing_spinner = ui.spinner(size='lg')
                drawing_spinner.set_visibility(False)

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg'):
            img_holder = ui.image()


ui.run(storage_secret="local_secret_key")
