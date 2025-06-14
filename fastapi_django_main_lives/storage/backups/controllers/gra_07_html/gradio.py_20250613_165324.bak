import gradio as gr
def display_html():
    html_content = """
    <h1>Hello, Gradio!</h1>
    <p>This is an example of displaying HTML content using Gradio.</p>
    <ul>
        <li>Item 11</li>
        <li>Item 22</li>
        <li>Item 33</li>
        <a href="test">aaa</a>
    </ul>
    <script type="module">
	import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/chat.bundle.es.js';

	createChat({
	webhookUrl: 'https://kenken999-nodex-n8n-domain.hf.space/webhook/6264497c-6231-4023-abef-82b86f8e298b/chat',
	webhookConfig: {
		method: 'POST',
		headers: {}
	},
	target: '#n8n-chat',
	mode: 'window',
	chatInputKey: 'chatInput',
	chatSessionKey: 'sessionId',
	metadata: {},
	showWelcomeScreen: false,
	defaultLanguage: 'en',
	initialMessages: [
		'質問をどうぞ Hi there! 👋',
		'私の名前はリファスタアシスタントです今日は何の御用ですか？?'
	],
	i18n: {
		en: {
			title: 'こんにちわリファスタアシスタントです! 👋',
			subtitle: "Start a chat. We're here to help you 24/7.",
			footer: '',
			getStarted: 'New Conversation',
			inputPlaceholder: 'Type your question..',
		},
	},
});
</script>
    """
    return html_content

# Gradioのインターフェースを作成  
# Note: このInterfaceは使用せず、下のBlocksベースのgradio_interfaceを使用
# gradio_interfaces = gr.Interface(
#     fn=display_html,  # HTMLコンテンツを返す関数
#     inputs=[],  # 入力なし
#     outputs=gr.Markdown()  # HTMLコンテンツを表示
# )


# Gradioのインターフェースを作成
with gr.Blocks() as gradio_interface:
    gr.HTML(display_html())
# インターフェースを起動
#iface.launch()
