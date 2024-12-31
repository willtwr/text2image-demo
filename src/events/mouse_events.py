from nicegui import events


def mouse_draw_handler(e: events.MouseEventArguments) -> None:
    """Handler for brushing mask on image with mouse."""
    color = 'Black'
    if e.type == 'mousedown':
        e.sender.is_drawing = True

    if e.sender.is_drawing:
        e.sender.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="10" fill="{color}" stroke="{color}" stroke-width="4" />'

    if e.type == 'mouseup':
        e.sender.is_drawing = False
