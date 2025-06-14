

import gradio as gr
import plantuml
import io

def generate_uml_diagram(plantuml_code):
    # Create a PlantUML object
    uml = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
    
    # Generate UML diagram
    output = io.BytesIO()
    uml.processes(plantuml_code, output=output)
    output.seek(0)
    
    return output

# Define Gradio interface
gradio_interfaces = gr.Interface(
    fn=generate_uml_diagram,
    inputs=gr.inputs.Textbox(lines=10, placeholder='Enter PlantUML code here...'),
    outputs=gr.outputs.Image(type="auto"),
    title="PlantUML Diagram Generator",
    description="Generate UML diagrams from PlantUML code using Gradio."
)