import os
from tqdm import tqdm

from .YOLO import imgs2pseudoimgs, img2pseudoimg, convert_all_pdf_to_pngs, delete_png_and_images_dir
from .GPT import process_image, process_paper

def find_peudo_code(path_to_paper):

    convert_all_pdf_to_pngs(path_to_paper)
    count = imgs2pseudoimgs()
    delete_png_and_images_dir()

    pseudo_codes = process_paper()

    if pseudo_codes:
        pseudo_codes_list = []
        for pseudo_code in pseudo_codes:
            pseudo_codes_list.append(pseudo_code)
        return count, pseudo_codes_list
    else:
        return 0, []
