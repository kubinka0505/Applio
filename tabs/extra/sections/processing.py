import os
import sys
import gradio as gr

now_dir = os.getcwd()
sys.path.append(now_dir)

from core import run_model_information_script
from tabs.inference.inference import sup_audioext
from assets.i18n.i18n import I18nAuto

i18n = I18nAuto()

def validate_upload(path):
    if not path:
        return gr.update(interactive=False)
    if path.lower().endswith(".pth") and os.path.isfile(path):
        return gr.update(interactive=True)
    return gr.update(interactive=False)

def processing_tab():
    model_view_model_path = gr.Textbox(
        label=i18n("Path to Model"),
        info=i18n("Introduce the model pth path"),
        value="",
        interactive=True,
        placeholder=i18n("Enter path to model"),
    )

    model_view_output_info = gr.Textbox(
        label=i18n("Output Information"),
        info=i18n("The output information will be displayed here."),
        value="",
        max_lines=11,
    )
    model_view_button = gr.Button(i18n("View"), interactive=False)
    model_view_button.click(
        fn=run_model_information_script,
        inputs=[model_view_model_path],
        outputs=[model_view_output_info],
    )

    model_view_model_path.change(
        fn=validate_upload,
        inputs=[model_view_model_path],
        outputs=[model_view_button],
    )

    model_view_model_path.change(
        fn=validate_upload,
        inputs=[model_view_model_path],
        outputs=[model_view_button],
    )
