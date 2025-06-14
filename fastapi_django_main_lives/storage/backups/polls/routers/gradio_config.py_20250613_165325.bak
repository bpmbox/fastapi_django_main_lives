import shutil
import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
from routers.chat.chat import demo44 as demo4
from mysite.gradio.chat import chat

def include_gradio_interfaces():
    package_dir = "/home/user/app/routers"
    gradio_interfaces = []
    gradio_names = set()

    for module_info in pkgutil.walk_packages([package_dir], "routers."):
        sub_module_name = module_info.name
        try:
            print(f"Trying to import {sub_module_name}")
            module = importlib.import_module(sub_module_name)
            if hasattr(module, "gradio_interface"):
                print(f"Found gradio_interface in {sub_module_name}")
                interface_name = module_info.name.split(".")[-1]
                if interface_name not in gradio_names:
                    gradio_interfaces.append(module.gradio_interface)
                    gradio_names.add(interface_name)
                else:
                    unique_name = f"{interface_name}_{len(gradio_names)}"
                    gradio_interfaces.append(module.gradio_interface)
                    gradio_names.add(unique_name)
        except ModuleNotFoundError:
            print(f"ModuleNotFoundError: {sub_module_name}")
            pass
        except Exception as e:
            print(f"Failed to import {sub_module_name}: {e}")

    print(f"Collected Gradio Interfaces: {gradio_names}")
    return gradio_interfaces, list(gradio_names)

def setup_gradio_interfaces():

    democs = gr.Interface(
        fn=process_file,
        inputs=[
            "file",
            gr.Textbox(label="Additional Notes", lines=10),
            gr.Textbox(label="Folder Name"),
        ],
        outputs="text",
    )

    from routers.postg.gradio_app import crud_interface

    default_interfaces = [chat,demo4,democs,crud_interface()]#,demo]
    default_names = ["Chat","OpenInterpreter","仕様書から作成","Database",]#"demo"]

    gradio_interfaces, gradio_names = include_gradio_interfaces()

    all_interfaces = default_interfaces + gradio_interfaces
    all_names = default_names + gradio_names

    tabs = gr.TabbedInterface(all_interfaces, all_names)
    tabs.queue()
    return tabs
