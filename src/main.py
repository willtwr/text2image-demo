from nicegui import ui, run, app, events
from contextlib import contextmanager
from diffusers.utils import load_image
import os
import io
from PIL import Image
import gc
import torch

from events.mouse_events import mouse_draw_handler
from utils import create_temp_folder, save_svg_to_png
from models.imagefill.imagefill_factory import get_imagefill_model, get_imagefill_models_list
from models.text2image.text2image_factory import get_t2i_model, get_t2i_models_list


t2imodel = None  # Not implementing app.storage here to avoid accidentally load multiple models into my potato GPU.


@contextmanager
def disable_when_init_model(
    init_model_spinner: ui.spinner, 
    init_model_button1: ui.button, 
    init_model_button2: ui.button, 
    draw_button: ui.button,
    fill_button: ui.button
):
    init_model_button1.disable()
    init_model_button2.disable()
    init_model_spinner.set_visibility(True)
    fill_button.disable()
    draw_button.disable()
    try:
        yield
    finally:
        init_model_button1.enable()
        init_model_button2.enable()
        init_model_spinner.set_visibility(False)
        fill_button.enable()
        draw_button.enable()


@contextmanager
def disable_when_generating(
    draw_button: ui.button, 
    drawing_spinner: ui.spinner, 
    img_desc: ui.textarea, 
    model_selector: ui.select, 
    init_model_button: ui.button,
    draw_button2: ui.button,
    init_model_button2: ui.button
):
    draw_button.disable()
    drawing_spinner.set_visibility(True)
    img_desc.disable()
    model_selector.disable()
    init_model_button.disable()
    draw_button2.disable()
    init_model_button2.disable()
    try:
        yield
    finally:
        draw_button.enable()
        drawing_spinner.set_visibility(False)
        img_desc.enable()
        model_selector.enable()
        init_model_button.enable()
        draw_button2.enable()
        init_model_button2.enable()


async def draw_button_clicked(
        draw_button: ui.button, 
        drawing_spinner: ui.spinner,
        img_desc: ui.textarea, 
        img_holder: ui.interactive_image,
        draw_notification: ui.label,
        model_selector: ui.select,
        init_model_button: ui.button,
        init_model_notification: ui.label,
        draw_button2: ui.button,
        init_model_button2: ui.button
) -> None:
    if t2imodel is None:
        draw_notification.set_text("Please select and initialize a model.")
        draw_notification.set_visibility(True)
        return
    
    if app.storage.user['current_model'] not in get_t2i_models_list():
        draw_notification.set_text("Please select and initialize a T2I model instead.")
        draw_notification.set_visibility(True)
        return

    init_model_notification.set_visibility(False)
    with disable_when_generating(draw_button, drawing_spinner, img_desc, model_selector, init_model_button, draw_button2, init_model_button2):
        image = await run.io_bound(t2imodel, prompt=img_desc.value)
        tempfolder = create_temp_folder()
        imgpth = os.path.join(tempfolder, 'tempimg.png')
        image.save(imgpth)
        del image
        img_holder.set_source(imgpth)
        img_holder.set_content("")
        img_holder.force_reload()


async def inpaint_button_clicked(
        inpaint_button: ui.button, 
        drawing_spinner: ui.spinner,
        img_desc: ui.textarea, 
        img_holder: ui.interactive_image,
        draw_notification: ui.label,
        model_selector: ui.select,
        init_model_button: ui.button,
        init_model_notification: ui.label,
        draw_button2: ui.button,
        init_model_button2: ui.button
) -> None:
    if t2imodel is None:
        draw_notification.set_text("Please select and initialize a model.")
        draw_notification.set_visibility(True)
        return
    
    if app.storage.user['current_model'] not in get_imagefill_models_list():
        draw_notification.set_text("Please select and initialize a Fill model instead.")
        draw_notification.set_visibility(True)
        return

    init_model_notification.set_visibility(False)
    with disable_when_generating(inpaint_button, drawing_spinner, img_desc, model_selector, init_model_button, draw_button2, init_model_button2):
        tempfolder = create_temp_folder()
        imgpth = os.path.join(tempfolder, 'tempimg.png')
        mask_pth = save_svg_to_png(img_holder.content)
        image = await run.io_bound(t2imodel, prompt=img_desc.value, image=load_image(imgpth), mask=load_image(mask_pth))
        image.save(imgpth)
        del image
        img_holder.set_source(imgpth)
        img_holder.set_content("")
        img_holder.force_reload()


async def init_model_button_clicked(
        model,
        init_model_spinner: ui.spinner,
        init_model_notification: ui.label,
        init_model_button1: ui.button,
        init_model_button2: ui.button,
        model_selector: ui.select,
        draw_button: ui.button,
        draw_notification: ui.label,
        fill_button: ui.button,
        fill_notification: ui.label
) -> None:
    draw_notification.set_visibility(False)
    fill_notification.set_visibility(False)
    if app.storage.user['current_model'] == model_selector.value:
        init_model_notification.set_text("Already loaded this model.")
        init_model_notification.set_visibility(True)
        return

    app.storage.user['current_model'] = model_selector.value
    init_model_notification.set_visibility(False)
    with disable_when_init_model(init_model_spinner, init_model_button1, init_model_button2, draw_button, fill_button):
        global t2imodel
        del t2imodel
        gc.collect()
        torch.cuda.empty_cache()
        t2imodel = await run.io_bound(model)


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    app.storage.user['current_model'] = None

    def upload_handler(e: events.UploadEventArguments):
        tempfolder = create_temp_folder()
        imgpth = os.path.join(tempfolder, 'tempimg.png')
        img = Image.open(io.BytesIO(e.content.read()))
        img.save(imgpth)
        e.sender.reset()
        img_holder.set_source(imgpth)
        img_holder.set_content("")
        img_holder.force_reload()

    with ui.column().classes('w-full items-center'):
        ui.label("Text to Image Demo").style('color: #6E93D6; font-size: 300%; font-weight: 300')
        with ui.card().classes('w-full max-w-screen-lg'):
            img_desc = ui.textarea(placeholder="Describe what you want to draw here...").classes('w-full').props('rounded outlined clearable')
            with ui.row():
                with ui.column().classes('w-8/12'):
                    with ui.row():
                        t2i_model_selector = ui.select(list(get_t2i_models_list()), value=list(get_t2i_models_list())[0]).props('outlined')
                        
                        with ui.column():
                            init_t2i_model_button = ui.button('Initialize T2I Model', 
                                                                on_click=lambda e: init_model_button_clicked(
                                                                    get_t2i_model(t2i_model_selector.value),
                                                                    init_t2i_model_spinner,
                                                                    init_t2i_model_notification,
                                                                    e.sender,
                                                                    init_fill_model_button,
                                                                    t2i_model_selector,
                                                                    draw_button,
                                                                    draw_notification,
                                                                    fill_button,
                                                                    fill_notification))
                            init_t2i_model_notification = ui.label()
                            init_t2i_model_notification.set_visibility(False)
                        
                        init_t2i_model_spinner = ui.spinner(size='lg')
                        init_t2i_model_spinner.set_visibility(False)

                        with ui.column():
                            draw_button = ui.button('Draw', 
                                                    on_click=lambda e: draw_button_clicked(
                                                        e.sender, 
                                                        drawing_spinner, 
                                                        img_desc, 
                                                        img_holder, 
                                                        draw_notification, 
                                                        t2i_model_selector, 
                                                        init_t2i_model_button, 
                                                        init_t2i_model_notification,
                                                        fill_button,
                                                        init_fill_model_button))
                            draw_notification = ui.label()
                            draw_notification.set_visibility(False)

                        drawing_spinner = ui.spinner(size='lg')
                        drawing_spinner.set_visibility(False)

                    with ui.row():
                        fill_model_selector = ui.select(list(get_imagefill_models_list()), value=list(get_imagefill_models_list())[0], on_change=lambda: init_fill_model_button.enable()).props('outlined')
                        
                        with ui.column():
                            init_fill_model_button = ui.button('Initialize Fill Model', 
                                                                on_click=lambda e: init_model_button_clicked(
                                                                    get_imagefill_model(fill_model_selector.value),
                                                                    init_fill_model_spinner,
                                                                    init_fill_model_notification,
                                                                    e.sender,
                                                                    init_t2i_model_button,
                                                                    fill_model_selector,
                                                                    draw_button,
                                                                    draw_notification,
                                                                    fill_button,
                                                                    fill_notification))
                            init_fill_model_notification = ui.label()
                            init_fill_model_notification.set_visibility(False)
                        
                        init_fill_model_spinner = ui.spinner(size='lg')
                        init_fill_model_spinner.set_visibility(False)

                        with ui.column():
                            fill_button = ui.button('Fill', 
                                                    on_click=lambda e: inpaint_button_clicked(
                                                        e.sender, 
                                                        filling_spinner, 
                                                        img_desc, 
                                                        img_holder, 
                                                        fill_notification, 
                                                        fill_model_selector, 
                                                        init_fill_model_button, 
                                                        init_fill_model_notification,
                                                        draw_button,
                                                        init_t2i_model_button))
                            fill_notification = ui.label()
                            fill_notification.set_visibility(False)

                        filling_spinner = ui.spinner(size='lg')
                        filling_spinner.set_visibility(False)

                with ui.column().classes('w-3/12'):
                    ui.upload(on_upload=upload_handler).props('accept=".png, image/*"')

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg items-center'):
            img_holder = ui.interactive_image(
                on_mouse=mouse_draw_handler,
                events=['mousedown', 'mouseup', 'mousemove'],
                cross=False
            )
            img_holder.is_drawing = False


ui.run(storage_secret="local_secret_key")
