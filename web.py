import gradio as gr
from main import agent_chat

notes_store = {"content": ""}


def chat_response(user_input, chat_history):
    if not user_input.strip():
        return "", chat_history
    try:
        ai_result = agent_chat(user_input)
    except Exception as e:
        ai_result = f"运行出错：{str(e)}"
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": ai_result})
    return "", chat_history


def save_note(content):
    notes_store["content"] = content
    return gr.update(value="✓ 已保存", interactive=False), content


def reset_save_btn():
    return gr.update(value="保存笔记", interactive=True)


def clear_chat():
    return []


css = """
* { box-sizing: border-box; }

body, .gradio-container {
    background: #f5f7fa !important;
    font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif !important;
    color: #1f2937 !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

#topbar {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    gap: 12px;
}

#topbar .logo {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border-radius: 8px;
    display: inline-block;
}

#topbar h1 {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #111827 !important;
    margin: 0 !important;
}

#topbar .subtitle {
    font-size: 12px;
    color: #9ca3af;
    margin-left: auto;
}

#tool-tags {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 10px 28px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.ttag {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 500;
}

#input-box textarea {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #1f2937 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    resize: none !important;
    padding: 10px 14px !important;
    line-height: 1.5 !important;
    transition: border-color 0.2s !important;
}

#input-box textarea:focus {
    border-color: #2563eb !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

#send-btn {
    background: #2563eb !important;
    border: none !important;
    color: #fff !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    height: 44px !important;
    transition: background 0.2s !important;
}

#send-btn:hover { background: #1d4ed8 !important; }

#clear-btn {
    background: transparent !important;
    border: 1px solid #d1d5db !important;
    color: #9ca3af !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    height: 44px !important;
    transition: all 0.2s !important;
}

#clear-btn:hover {
    border-color: #ef4444 !important;
    color: #ef4444 !important;
}

#note-header {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 14px 20px;
    font-size: 13px;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

#note-box textarea {
    background: #fafafa !important;
    border: none !important;
    box-shadow: none !important;
    color: #374151 !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    resize: none !important;
    padding: 16px 20px !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
}

#note-box textarea:focus {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}

#save-btn {
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    color: #16a34a !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    height: 34px !important;
    transition: all 0.2s !important;
}

#save-btn:hover { background: #dcfce7 !important; }

.gr-samples-table { display: flex !important; gap: 6px !important; flex-wrap: wrap !important; }
.gr-samples-table td { padding: 0 !important; }
.gr-samples-table button {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    color: #6b7280 !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 4px 12px !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
}
.gr-samples-table button:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
}
"""

with gr.Blocks(title="AI Agent 智能助手") as demo:

    gr.HTML("""
    <div id="topbar">
        <span class="logo"></span>
        <h1>AI Agent 智能助手</h1>
        <span class="subtitle">ReAct · 多工具 · 长期记忆</span>
    </div>
    <div id="tool-tags">
        <span class="ttag">数学计算</span>
        <span class="ttag">维基百科</span>
        <span class="ttag">文件读写</span>
        <span class="ttag">网页抓取</span>
        <span class="ttag">时间查询</span>
        <span class="ttag">单位换算</span>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                elem_id="chatbot",
                height=500,
                show_label=False,
                placeholder="<div style='text-align:center;color:#d1d5db;padding:60px 0;font-size:14px'>发送消息开始对话</div>",
            )
            with gr.Row():
                input_box = gr.Textbox(
                    elem_id="input-box",
                    placeholder="输入问题，按 Enter 发送…",
                    show_label=False,
                    scale=8,
                    lines=1,
                    max_lines=4,
                )
                send_btn = gr.Button("发送", elem_id="send-btn", scale=1, min_width=80)
                clear_btn = gr.Button("清空", elem_id="clear-btn", scale=1, min_width=60)

            with gr.Row():
                gr.Examples(
                    examples=[
                        ["今天是几号？"],
                        ["查一下爱因斯坦出生年份，算他活了多少岁"],
                        ["把 100 摄氏度换算成华氏度"],
                        ["抓取 https://example.com 写入 result.txt"],
                    ],
                    inputs=input_box,
                    label="",
                )

        with gr.Column(scale=1):
            gr.HTML('<div id="note-header">📝 &nbsp;笔记本</div>')
            note_box = gr.Textbox(
                elem_id="note-box",
                container=False,
                placeholder="在此记录重要信息、思路或 Agent 返回的结果…",
                show_label=False,
                lines=22,
                max_lines=40,
            )
            save_btn = gr.Button("保存笔记", elem_id="save-btn")

    input_box.submit(chat_response, [input_box, chatbot], [input_box, chatbot])
    send_btn.click(chat_response, [input_box, chatbot], [input_box, chatbot])
    clear_btn.click(clear_chat, None, chatbot)
    save_btn.click(save_note, [note_box], [save_btn, note_box]).then(
        reset_save_btn, None, save_btn
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        css=css,
    )
