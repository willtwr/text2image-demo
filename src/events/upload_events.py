import os
import io
from nicegui import events, ui
from PIL import Image
from utils import create_temp_folder


def upload_handler(e: events.UploadEventArguments, img_holder: ui.interactive_image) -> None:
    """Handler for image upload."""
    tempfolder = create_temp_folder()
    imgpth = os.path.join(tempfolder, 'tempimg.png')
    img = Image.open(io.BytesIO(e.content.read()))
    img.save(imgpth)
    e.sender.reset()
    img_holder.set_source(imgpth)
    img_holder.set_content("")
    img_holder.force_reload()
