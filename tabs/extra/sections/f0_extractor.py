import os
import librosa
import gradio as gr
from matplotlib import pyplot as plt

from rvc.lib.predictors.F0Extractor import F0Extractor
from tabs.inference.inference import sup_audioext
from assets.i18n.i18n import I18nAuto

i18n = I18nAuto()

def validate_upload(path):
    if not path:
        return gr.update(interactive=False)
    if all((
        path,
        os.path.isfile(path),
        path.lower().endswith(tuple(sup_audioext))
    )):
        return gr.update(interactive=True)
    return gr.update(interactive=False)

def extract_f0_curve(audio_path: str, method: str):
    print("Extracting F0 Curve...")
    image_path = os.path.join("logs", "f0_plot.png")
    txt_path = os.path.join("logs", "f0_curve.txt")
    y, sr = librosa.load(audio_path, sr=None)
    hop_length = 160

    librosa.note_to_hz("C1")
    librosa.note_to_hz("C8")

    f0_extractor = F0Extractor(audio_path, sample_rate=sr, method=method)
    f0 = f0_extractor.extract_f0()

    plt.figure(figsize=(10, 4))
    plt.plot(f0)
    plt.title(method)
    plt.xlabel("Time (frames)")
    plt.ylabel("Frequency (Hz)")
    plt.savefig(image_path)
    plt.close()

    with open(txt_path, "w") as txtfile:
        for i, f0_value in enumerate(f0):
            frequency = i * sr / hop_length
            txtfile.write(f"{frequency},{f0_value}\n")

    print("F0 Curve extracted successfully!")
    return image_path, txt_path


def f0_extractor_tab():
    audio = gr.Audio(label=i18n("Upload Audio"), type="filepath")
    f0_method = gr.Radio(
        label=i18n("Pitch extraction algorithm"),
        info=i18n(
            "Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases."
        ),
        choices=["crepe", "fcpe", "rmvpe"],
        value="rmvpe",
    )
    button = gr.Button(i18n("Extract F0 Curve"), interactive=False)

    with gr.Row():
        txt_output = gr.File(label="F0 Curve", type="filepath")
        image_output = gr.Image(type="filepath", interactive=False)

    button.click(
        fn=extract_f0_curve,
        inputs=[
            audio,
            f0_method,
        ],
        outputs=[image_output, txt_output],
    )

    audio.change(
        fn=validate_upload,
        inputs=[audio],
        outputs=[button],
    )

    audio.clear(
        lambda: gr.update(interactive=False),
        outputs=[button],
    )
