import gradio as gr
from PIL import Image

def calculate_ratio(image, shorter_side_length: int):
    width, height = image.size
    if width < height:
        new_width = shorter_side_length
        new_height = int(shorter_side_length * height / width)
    else:
        new_height = shorter_side_length
        new_width = int(shorter_side_length * width / height)
    return new_width, new_height

def calculate_ratios(image):
    results = []
    for side_length in [512, 768, 896]:
        new_width, new_height = calculate_ratio(image, side_length)
        results.append(f"{new_width} x {new_height}")
    return results

def on_ui_tab_called():
    with gr.Blocks() as calculator_interface:
        with gr.Row():
            image = gr.Image(type="pil",source="upload")
            ratio_results_512 = gr.Textbox(lines=1, label="Results for 512")
            ratio_results_768 = gr.Textbox(lines=1, label="Results for 768")
            ratio_results_1024 = gr.Textbox(lines=1, label="Results for 1024")
            #button = gr.Button(text="Calculate")
            image.upload(
                fn=calculate_ratios,
                inputs=[image],
                outputs=[ratio_results_512, ratio_results_768, ratio_results_1024]
            )

    return (calculator_interface, "calculator", "calculator_interface"),
try:
    from modules import script_callbacks, postprocessing
    script_callbacks.on_ui_tabs(on_ui_tab_called)
except (ImportError, ModuleNotFoundError):
    # context not in webui, run as separate script
    if __name__ == "__main__":
        interface, _, _ = on_ui_tab_called()[0]
        interface.launch()
