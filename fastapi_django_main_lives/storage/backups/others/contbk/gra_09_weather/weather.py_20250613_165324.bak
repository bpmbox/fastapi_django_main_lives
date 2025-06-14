import gradio as gr

def weather_forecast(city):
    """
    簡単な天気予報機能のデモ
    """
    # この関数は実際の天気予報APIの代わりにダミーデータを返します
    weather_data = {
        "Tokyo": "晴れ 25°C",
        "Osaka": "曇り 22°C", 
        "Kyoto": "雨 18°C",
        "Hiroshima": "晴れ 27°C",
        "Sapporo": "雪 -2°C"
    }
    
    result = weather_data.get(city, f"{city}の天気情報は現在利用できません")
    return f"🌤️ {city}の天気: {result}"

def temperature_converter(celsius):
    """
    摂氏から華氏への変換
    """
    if celsius is None:
        return "温度を入力してください"
    
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius}°C = {fahrenheit:.1f}°F"

# AI指示による自動作成テスト: 天気予報インターフェース
# この名前でないと自動検出されません
with gr.Blocks(title="天気予報システム") as gradio_interface:
    gr.Markdown("# 🌤️ 天気予報 & 温度変換システム")
    gr.Markdown("このインターフェースは AI指示による自動作成のテストです")
    
    with gr.Tab("天気予報"):
        with gr.Row():
            city_input = gr.Textbox(
                label="都市名", 
                placeholder="Tokyo, Osaka, Kyoto, Hiroshima, Sapporo",
                value="Tokyo"
            )
            weather_btn = gr.Button("天気を確認", variant="primary")
        
        weather_output = gr.Textbox(label="天気予報結果", interactive=False)
        
        weather_btn.click(
            fn=weather_forecast,
            inputs=city_input,
            outputs=weather_output
        )
    
    with gr.Tab("温度変換"):
        with gr.Row():
            celsius_input = gr.Number(
                label="摂氏温度 (°C)", 
                value=25
            )
            convert_btn = gr.Button("華氏に変換", variant="secondary")
        
        fahrenheit_output = gr.Textbox(label="華氏温度結果", interactive=False)
        
        convert_btn.click(
            fn=temperature_converter,
            inputs=celsius_input,
            outputs=fahrenheit_output
        )
    
    # サンプル用の例
    gr.Examples(
        examples=[
            ["Tokyo"],
            ["Osaka"], 
            ["Kyoto"],
            ["Hiroshima"],
            ["Sapporo"]
        ],
        inputs=city_input
    )

# テスト用のスタンドアロン実行
if __name__ == "__main__":
    gradio_interface.launch()
