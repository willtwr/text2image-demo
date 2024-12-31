from contextlib import contextmanager
from nicegui import ui


@contextmanager
def disable_when_init_model(
    init_model_spinner: ui.spinner, 
    init_model_button1: ui.button, 
    init_model_button2: ui.button, 
    draw_button: ui.button,
    fill_button: ui.button
):
    """Temporary disable buttons when initializing model"""
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
    """Temporary disable buttons when generating image"""
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
