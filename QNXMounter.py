import PySimpleGUI as sg
import qnxmount
import os

def mount_qnx_image(image_path, mount_point):
    try:
        # Mount the QNX image using qnxmount library
        with qnxmount.Mount(image_path, mount_point, read_only=True):
            pass  # The image is mounted successfully
    except Exception as e:
        sg.popup_error(f'Error mounting QNX image: {e}', title='Error')

layout = [
    [sg.Text('')],
    [sg.Text('Select QNX Image File: (.bin, .dd, .001)')], 
    [sg.InputText(key='image_file'), sg.FileBrowse(file_types=".bin")],
    # [sg.Text('')],
    [sg.Text('Mount Point:')], 
    [sg.InputText(key='mount_point'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Button('Mount', key='mount_button')],
]

window = sg.Window('QNX Image Mounter (Read Only)', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'mount_button':
        image_file = values['image_file']
        mount_point = values['mount_point']

        if os.path.exists(image_file) and os.path.exists(mount_point):
            # Call the function to mount the QNX image using qnxmount library
            mount_qnx_image(image_file, mount_point)
            sg.popup('QNX Image mounted successfully!', title='Success')
        else:
            sg.popup_error('Invalid image file or mount point. Please check the paths.')

window.close()
