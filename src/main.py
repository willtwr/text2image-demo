from nicegui import ui, app
from events.mouse_events import mouse_draw_handler
from events.button_events import draw_button_clicked, inpaint_button_clicked, init_model_button_clicked
from events.upload_events import upload_handler
from models.imagefill.imagefill_factory import get_imagefill_model, get_imagefill_models_list
from models.text2image.text2image_factory import get_t2i_model, get_t2i_models_list


@ui.page("/", dark=True, title="Text to Image Demo")
def main():
    app.storage.user['current_model'] = None
    app.storage.client['t2imodel'] = None

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
                    ui.upload(on_upload=lambda e: upload_handler(e, img_holder)).props('accept=".png, image/*"')

    with ui.column().classes('w-full items-center'):
        with ui.card().classes('w-full max-w-screen-lg items-center'):
            img_holder = ui.interactive_image(
                on_mouse=mouse_draw_handler,
                events=['mousedown', 'mouseup', 'mousemove'],
                cross=False
            )
            img_holder.is_drawing = False


ui.run(storage_secret="local_secret_key")
