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

def calculate_pixel_ratios(image:Image.Image):
    """
    Calculates required ratio (with respecting original aspect ratio) to match pixel count
    """
    results = []
    original_pixel_count = image.size[0] * image.size[1]
    for pixel_counts in [768**2, 1024**2]:
        ratio_to_divide_squared = original_pixel_count / pixel_counts
        ratio_to_divide = ratio_to_divide_squared ** 0.5
        new_width = int(image.size[0] / ratio_to_divide)
        new_height = int(image.size[1] / ratio_to_divide)
        results.append(f"{new_width} x {new_height} ({pixel_counts} pixels) (matched for {int(pixel_counts**0.5)} pixels)")
    return results

def calculate_ratios(image):
    results = []
    for side_length in [512, 768, 896]:
        new_width, new_height = calculate_ratio(image, side_length)
        shorter_side = min(new_width, new_height)
        longer_side = max(new_width, new_height)
        ratio = longer_side / shorter_side
        # get 1:x or x:1 ratio
        if new_width == shorter_side:
            ratio_str = f"1:{ratio}"
        else:
            ratio_str = f"{ratio}:1"
        results.append(f"{new_width} x {new_height} ({ratio_str})")
    return results

def calculate_and_concat_ratios(image):
    r1 = calculate_ratios(image)
    r2 = calculate_pixel_ratios(image)
    return r1 + r2

def on_ui_tab_called():
    with gr.Blocks() as calculator_interface:
        with gr.Row():
            image = gr.Image(type="pil",source="upload")
            ratio_results_512 = gr.Textbox(lines=1, label="Results for 512")
            ratio_results_768 = gr.Textbox(lines=1, label="Results for 768")
            ratio_results_1024 = gr.Textbox(lines=1, label="Results for 1024")
            
            pixel_ratio_result_768 = gr.Textbox(lines=1, label="Pixel Ratios for 768**2")
            pixel_ratio_result_1024 = gr.Textbox(lines=1, label="Pixel Ratios for 1024**2")
            #button = gr.Button(text="Calculate")
            image.upload(
                fn=calculate_and_concat_ratios,
                inputs=[image],
                outputs=[ratio_results_512, ratio_results_768, ratio_results_1024, pixel_ratio_result_768, pixel_ratio_result_1024]
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
