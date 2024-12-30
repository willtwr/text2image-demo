import os
from cairosvg import svg2png
from PIL import Image, ImageOps


def create_temp_folder():
    tempfolder = "./tempfolder"
    if not os.path.exists(tempfolder):
        os.mkdir(tempfolder)

    return tempfolder


def save_svg_to_png(content):
    svg_code = f"""
    <svg viewBox="0 0 783 783" style="position: absolute; top: 0px; left: 0px; pointer-events: none;">
    <g>
    {content}
    </g>
    </svg>
    """
    tempfolder = create_temp_folder()
    mask_pth = os.path.join(tempfolder, "mask.png")
    svg2png(bytestring=svg_code, write_to=mask_pth, background_color="white")
    mask = ImageOps.invert(Image.open(mask_pth))
    mask.save(mask_pth)
    return mask_pth
