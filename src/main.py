"""
GUI for image pipeline.
"""
import tkinter as tk
from tkinter import PhotoImage, StringVar, IntVar
from tkinter.messagebox import showerror
from tkinter import ttk
import img_processor as img_processor

def create_im_label_input() -> None:
    """Creates the label and input entry for the image to be processed"""
    global im_fp_var
    im_fp_var = StringVar()
    im_fp_label = ttk.Label(root, text="Image file path: ")
    im_fp_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    im_fp_entry = ttk.Entry(root, textvariable=im_fp_var)
    im_fp_entry.grid(column=1, row=0, padx=5, pady=5)

def create_cropped_width_label_input() -> None:
    """Creates the label and input entry for the width of the proposed cropped image"""
    global cropped_width_var
    cropped_width_var = IntVar()
    cropped_width_label = ttk.Label(root, text="Desired cropped image width: ")
    cropped_width_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    cropped_width_entry = ttk.Entry(root, textvariable=cropped_width_var)
    cropped_width_entry.grid(column=1, row=1, padx=5, pady=5)

def create_cropped_height_label_input() -> None:
    """Creates a label and input entry for the height of the proposed image"""
    global cropped_height_var
    cropped_height_var = IntVar()
    cropped_height_label = ttk.Label(root, text="Desired cropped image height: ")
    cropped_height_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

    cropped_height_entry = ttk.Entry(root, textvariable=cropped_height_var)
    cropped_height_entry.grid(column=1, row=2, padx=5, pady=5)

def create_blurb_label() -> None:
    """Creates a label for a blurb explaining the programme."""
    blurb_text = "This programme transforms images.\n\nSpecifically, it does the following:\n1.) It converts a source image (SI) to greyscale\n2.) It crops the SI into 3 non-overlapping images\n3.) And finally, it rotates the SI by 180 degrees.\n\nTo crop several images, enter the filepaths like this: assets/surgical_robot.jpeg,assets/tsp_scissors.png.\n\nOnce the image processing is complete, the programme shows you the cropped images.\nIt stores them in the data folder associated with this directory.\n\nHAPPY IMAGE PROCESSING!"
    blurb_label = tk.Label(root, text=blurb_text)
    blurb_label.grid(column=2, row=0, rowspan=3)

def crop_image() -> None:
    """Executes the main function from img_processing.py with the inputs from the GUI"""
    try:
        fnames = im_fp_var.get()
        fnames = fnames.split(',')
        cropped_width = cropped_width_var.get()
        cropped_height = cropped_height_var.get()
    except ValueError as error:
        showerror(title='Error', message=error)
    else:
        img_processor.main(filenames=fnames, c_width=cropped_width, c_height=cropped_height)

def create_crop_button() -> None:
    """Creates a button that executes the cropping and other bits of image processing"""
    crop_button = ttk.Button(root, text='Click to crop image', command=crop_image)
    crop_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

def main() -> None:
    """Creates the main window"""
    global root, im
    root = tk.Tk()
    root.title("Image cropper")
    im = PhotoImage(file='assets/tsp_scissors.png')
    root.iconphoto(False, im)

    # Configuring the grid
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.columnconfigure(2, weight=1)

    create_im_label_input()
    create_cropped_width_label_input()
    create_cropped_height_label_input()
    create_blurb_label()
    create_crop_button()

    root.mainloop()

if __name__ == "__main__":
    main()