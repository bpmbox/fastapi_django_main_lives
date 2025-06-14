import shutil
import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
import async_timeout
import asyncio


def list_files_in_directory(directory):
    tree = []
    for root, dirs, files in os.walk(directory):
        path = root.split(os.sep)
        for dir_name in dirs:
            tree.append((os.path.join(root, dir_name), '/'.join(path + [dir_name])))
        for file_name in files:
            tree.append((os.path.join(root, file_name), '/'.join(path + [file_name])))
    return tree

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'rb') as file:
            content = file.read()
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return content.decode('latin-1')
            except UnicodeDecodeError:
                return "Cannot decode file content with utf-8 or latin-1 encoding."

def save_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return "File saved successfully"

def on_file_select(selected_file):
    if os.path.isfile(selected_file):
        return read_file(selected_file)
    return ""

def build_interface(base_directory):
    file_list = list_files_in_directory(base_directory)
    file_display = [f[1] for f in file_list]
    file_paths = {f[1]: f[0] for f in file_list}

    with gr.Blocks() as demo:
        gr.Markdown("## File Explorer and Editor")

        file_dropdown = gr.Dropdown(label="Select a file or folder", choices=file_display)
        file_editor = gr.Textbox(label="File Editor", lines=20)
        save_button = gr.Button("Save File")

        def update_editor(selected_display):
            selected_file = file_paths.get(selected_display, "")
            return on_file_select(selected_file)

        def on_edit_button_click(selected_display, new_content):
            selected_file = file_paths.get(selected_display, "")
            if os.path.isfile(selected_file):
                return save_file(selected_file, new_content)
            return "File not found"

        file_dropdown.change(fn=update_editor, inputs=file_dropdown, outputs=file_editor)
        save_button.click(fn=on_edit_button_click, inputs=[file_dropdown, file_editor], outputs=None)

    return demo




base_directory = "/home/user/app/routers"  # Here you can specify any directory you want to explore
demo = build_interface(base_directory)