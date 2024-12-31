import os
import gc
import torch
from diffusers.utils import load_image
from nicegui import ui, app, run

from context_manager.model_process import disable_when_generating, disable_when_init_model
from utils import create_temp_folder, save_svg_to_png
from models.imagefill.imagefill_factory import get_imagefill_models_list
from models.text2image.text2image_factory import get_t2i_models_list



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
    """Function for when draw button is pressed"""
    if app.storage.client['t2imodel'] is None:
        draw_notification.set_text("Please select and initialize a model.")
        draw_notification.set_visibility(True)
        return
    
    if app.storage.user['current_model'] not in get_t2i_models_list():
        draw_notification.set_text("Please select and initialize a T2I model instead.")
        draw_notification.set_visibility(True)
        return

    init_model_notification.set_visibility(False)
    with disable_when_generating(draw_button, drawing_spinner, img_desc, model_selector, init_model_button, draw_button2, init_model_button2):
        image = await run.io_bound(app.storage.client['t2imodel'], prompt=img_desc.value)
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
    """Function for when inpaint button is pressed"""
    if app.storage.client['t2imodel'] is None:
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
        image = await run.io_bound(app.storage.client['t2imodel'], prompt=img_desc.value, image=load_image(imgpth), mask=load_image(mask_pth))
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
    """Function for when initialize model button is pressed"""
    draw_notification.set_visibility(False)
    fill_notification.set_visibility(False)
    if app.storage.user['current_model'] == model_selector.value:
        init_model_notification.set_text("Already loaded this model.")
        init_model_notification.set_visibility(True)
        return

    app.storage.user['current_model'] = model_selector.value
    init_model_notification.set_visibility(False)
    with disable_when_init_model(init_model_spinner, init_model_button1, init_model_button2, draw_button, fill_button):
        del app.storage.client['t2imodel']
        gc.collect()
        torch.cuda.empty_cache()
        app.storage.client['t2imodel'] = await run.io_bound(model)
