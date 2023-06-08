import gradio as gr
import os
import requests, uuid, json

endpoint = "https://api.cognitive.microsofttranslator.com"
LANGS = ["中文[简体]", "英语", "日语"]
key = os.environ["AZ_TRANSLATION_KEY"]
location = os.environ["AZ_TRANSLATION_REGION"]
path = "/translate"
constructed_url = endpoint + path

LAN_CODE_MAP = {"中文[简体]": "zh-Hans", "英语": "en", "日语": "ja"}


def translate(text, src_lang, tgt_lang):
    """
    Translate the text from source lang to target lang
    """
    params = {
        "api-version": "3.0",
        "from": f"{LAN_CODE_MAP[src_lang]}",
        "to": [f"{LAN_CODE_MAP[tgt_lang]}"],
    }
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        # location required if you're using a multi-service or regional (not global) resource.
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    body = [{"text": text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    # result = json.dumps(
    #     response, sort_keys=True, ensure_ascii=False, indent=4, separators=(",", ": ")
    # )
    return response[0]["translations"][0]["text"]


with gr.Blocks() as demo:
    gr.Markdown("# 将文本翻译为另一种语言")
    # gr.Markdown("""![logo](./images/translator.png =200x100 "Company Logo")""")
    gr.Markdown("+ 选择输入文本语言")
    gr.Markdown("+ 选择翻译目标语言")
    gr.Markdown("+ 输入要翻译的文本")
    gr.Markdown("+ 点击<翻译>按钮查看结果")
    with gr.Row():
        src_lan = gr.Dropdown(
            label="src", show_label=False, choices=LANGS, type="value"
        )
        tgt_lan = gr.Dropdown(
            label="tgt", show_label=False, choices=LANGS, type="value"
        )

    with gr.Row():
        txt_src = gr.Textbox(label="输入文本")
        txt_tgt = gr.Textbox(label="翻译结果")

    with gr.Row():
        btn = gr.Button("翻译").style(full_width=False)
        btn.click(translate, inputs=[txt_src, src_lan, tgt_lan], outputs=[txt_tgt])

    gr.Markdown("## 参考案例")
    gr.Markdown("点击以下案例观察结果")
    gr.Examples(
        [
            ["禁用功能时，也会显示文本框。", "中文[简体]", "日语"],
            ["The text box will also appear when you disable a feature.", "英语", "日语"],
            ["このテキスト ボックスは、機能を無効にしたときにも表示されます。", "日语", "英语"],
        ],
        [txt_src, src_lan, tgt_lan],
        txt_tgt,
        translate,
        # cache_examples=True,
        run_on_click=True,
    )

demo.launch()
