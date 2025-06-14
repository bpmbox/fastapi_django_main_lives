import gradio as gr
import base64
import io
from PIL import Image
import json
import re

def analyze_image_and_generate_ui(image, description, framework_choice):
    """
    アップロードされた画像を解析してUIコードを自動生成
    """
    if image is None:
        return "画像をアップロードしてください", "", "", ""
    
    # 画像解析（実際のAIモデルの代わりにルールベースで実装）
    analysis_result = analyze_ui_elements(image)
    
    # 選択されたフレームワークに応じてコード生成
    if framework_choice == "React":
        status, jsx_code, css_code = generate_react_from_analysis(analysis_result, description)
        return status, jsx_code, css_code, ""
    elif framework_choice == "Vue":
        status, vue_code = generate_vue_from_analysis(analysis_result, description)
        return status, vue_code, "", ""
    elif framework_choice == "HTML/CSS":
        status, html_code, css_code = generate_html_from_analysis(analysis_result, description)
        return status, html_code, css_code, ""
    else:
        return "フレームワークを選択してください", "", "", ""

def analyze_ui_elements(image):
    """
    画像からUI要素を検出（簡易版実装）
    実際の実装では、YOLOやCNNベースのモデルを使用
    """
    width, height = image.size
    
    # 基本的な画像分析
    analysis = {
        "image_size": (width, height),
        "aspect_ratio": width / height,
        "detected_elements": [],
        "color_scheme": "modern",
        "layout_type": "grid" if width > height else "vertical"
    }
    
    # 画像の明度から背景色を推定
    grayscale = image.convert('L')
    pixels = list(grayscale.getdata())
    avg_brightness = sum(pixels) / len(pixels)
    
    if avg_brightness < 85:
        analysis["theme"] = "dark"
        analysis["bg_color"] = "#1a1a1a"
        analysis["text_color"] = "#ffffff"
    elif avg_brightness > 200:
        analysis["theme"] = "light"
        analysis["bg_color"] = "#ffffff" 
        analysis["text_color"] = "#333333"
    else:
        analysis["theme"] = "modern"
        analysis["bg_color"] = "#f8f9fa"
        analysis["text_color"] = "#2c3e50"
    
    # UI要素の検出（簡易版）
    analysis["detected_elements"] = [
        {"type": "header", "confidence": 0.9},
        {"type": "button", "confidence": 0.8},
        {"type": "card", "confidence": 0.7},
        {"type": "navigation", "confidence": 0.6}
    ]
    
    return analysis

def generate_react_from_analysis(analysis, description):
    """
    分析結果からReactコンポーネントを生成
    """
    component_name = "ImageGeneratedComponent"
    
    # Template strings to avoid f-string complexity
    jsx_template = """import React, { useState } from 'react';
import './ImageGeneratedComponent.css';

const COMPONENT_NAME = () => {
    const [activeTab, setActiveTab] = useState('home');
    const [isLoading, setIsLoading] = useState(false);

    const handleAction = (action) => {
        setIsLoading(true);
        // AIが画像から推定したアクション処理
        setTimeout(() => {
            setIsLoading(false);
            console.log(`Executed action: ${action}`);
        }, 1000);
    };

    return (
        <div className="image-generated-container">
            <header className="app-header">
                <h1>AI Generated UI</h1>
                <p>DESCRIPTION_PLACEHOLDER</p>
            </header>

            <nav className="app-navigation">
                {['home', 'features', 'about'].map(tab => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`nav-button ${activeTab === tab ? 'active' : ''}`}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                ))}
            </nav>

            <main className="app-main">
                <div className="content-grid">
                    <div className="feature-card">
                        <h3>Feature 1</h3>
                        <p>AIが画像から検出した機能</p>
                        <button 
                            onClick={() => handleAction('feature1')}
                            disabled={isLoading}
                            className="action-button"
                        >
                            {isLoading ? 'Processing...' : 'Execute'}
                        </button>
                    </div>
                    
                    <div className="feature-card">
                        <h3>Feature 2</h3>
                        <p>画像解析に基づく機能</p>
                        <button 
                            onClick={() => handleAction('feature2')}
                            disabled={isLoading}
                            className="action-button secondary"
                        >
                            {isLoading ? 'Processing...' : 'Execute'}
                        </button>
                    </div>
                </div>
            </main>

            <footer className="app-footer">
                <p>Generated by AI from image analysis</p>
            </footer>
        </div>
    );
};

export default COMPONENT_NAME;"""

    css_template = """.image-generated-container {
    min-height: 100vh;
    background: BG_COLOR_PLACEHOLDER;
    color: TEXT_COLOR_PLACEHOLDER;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.app-header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.app-navigation {
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.nav-button {
    padding: 10px 20px;
    border: none;
    border-radius: 25px;
    background: transparent;
    color: TEXT_COLOR_PLACEHOLDER;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.nav-button:hover,
.nav-button.active {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
}

.app-main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
}

.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 30px;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.5rem;
}

.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.action-button.secondary {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    color: #8b4513;
}

.action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.app-footer {
    text-align: center;
    padding: 30px;
    background: BG_COLOR_PLACEHOLDER;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    margin-top: 50px;
}

@media (max-width: 768px) {
    .app-navigation {
        flex-direction: column;
        align-items: center;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
    }
    
    .app-header h1 {
        font-size: 2rem;
    }
}"""

    # Replace placeholders
    jsx_code = jsx_template.replace("COMPONENT_NAME", component_name)
    jsx_code = jsx_code.replace("DESCRIPTION_PLACEHOLDER", description)
    
    css_code = css_template.replace("BG_COLOR_PLACEHOLDER", analysis['bg_color'])
    css_code = css_code.replace("TEXT_COLOR_PLACEHOLDER", analysis['text_color'])

    return "✅ React component generated from image analysis!", jsx_code, css_code

def generate_vue_from_analysis(analysis, description):
    """
    分析結果からVue.jsコンポーネントを生成
    """
    vue_template = """<template>
  <div class="image-generated-container">
    <header class="app-header">
      <h1>AI Generated Vue UI</h1>
      <p>DESCRIPTION_PLACEHOLDER</p>
    </header>

    <nav class="app-navigation">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="['nav-button', { active: activeTab === tab }]"
      >
        {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
      </button>
    </nav>

    <main class="app-main">
      <div class="content-grid">
        <div 
          v-for="feature in features"
          :key="feature.id"
          class="feature-card"
        >
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <button 
            @click="handleAction(feature.action)"
            :disabled="isLoading"
            :class="['action-button', feature.variant]"
          >
            {{ isLoading ? 'Processing...' : 'Execute' }}
          </button>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <p>Generated by AI from image analysis using Vue.js</p>
    </footer>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'ImageGeneratedComponent',
  setup() {
    const activeTab = ref('home')
    const isLoading = ref(false)
    
    const tabs = ['home', 'features', 'about']
    
    const features = reactive([
      {
        id: 1,
        title: 'Feature 1',
        description: 'AIが画像から検出した機能',
        action: 'feature1',
        variant: 'primary'
      },
      {
        id: 2, 
        title: 'Feature 2',
        description: '画像解析に基づく機能',
        action: 'feature2',
        variant: 'secondary'
      }
    ])

    const handleAction = (action) => {
      isLoading.value = true
      setTimeout(() => {
        isLoading.value = false
        console.log(`Executed action: ${action}`)
      }, 1000)
    }

    return {
      activeTab,
      isLoading,
      tabs,
      features,
      handleAction
    }
  }
}
</script>

<style scoped>
.image-generated-container {
  min-height: 100vh;
  background: BG_COLOR_PLACEHOLDER;
  color: TEXT_COLOR_PLACEHOLDER;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  color: white;
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.app-navigation {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.nav-button {
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  background: transparent;
  color: TEXT_COLOR_PLACEHOLDER;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-button:hover,
.nav-button.active {
  background: #42b883;
  color: white;
  transform: translateY(-2px);
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.5rem;
}

.action-button {
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 15px;
  color: white;
}

.action-button.primary {
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
}

.action-button.secondary {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #8b4513;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(66, 184, 131, 0.4);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.app-footer {
  text-align: center;
  padding: 30px;
  background: BG_COLOR_PLACEHOLDER;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  margin-top: 50px;
}

@media (max-width: 768px) {
  .app-navigation {
    flex-direction: column;
    align-items: center;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .app-header h1 {
    font-size: 2rem;
  }
}
</style>"""

    vue_code = vue_template.replace("DESCRIPTION_PLACEHOLDER", description)
    vue_code = vue_code.replace("BG_COLOR_PLACEHOLDER", analysis['bg_color'])
    vue_code = vue_code.replace("TEXT_COLOR_PLACEHOLDER", analysis['text_color'])

    return "✅ Vue.js component generated from image analysis!", vue_code

def generate_html_from_analysis(analysis, description):
    """
    分析結果からHTML/CSSを生成
    """
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated UI</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="image-generated-container">
        <header class="app-header">
            <h1>AI Generated HTML UI</h1>
            <p>DESCRIPTION_PLACEHOLDER</p>
        </header>

        <nav class="app-navigation">
            <button class="nav-button active" onclick="setActiveTab('home')">Home</button>
            <button class="nav-button" onclick="setActiveTab('features')">Features</button>
            <button class="nav-button" onclick="setActiveTab('about')">About</button>
        </nav>

        <main class="app-main">
            <div class="content-grid">
                <div class="feature-card">
                    <h3>Feature 1</h3>
                    <p>AIが画像から検出した機能</p>
                    <button class="action-button" onclick="handleAction('feature1')">
                        Execute
                    </button>
                </div>
                
                <div class="feature-card">
                    <h3>Feature 2</h3>
                    <p>画像解析に基づく機能</p>
                    <button class="action-button secondary" onclick="handleAction('feature2')">
                        Execute
                    </button>
                </div>
            </div>
        </main>

        <footer class="app-footer">
            <p>Generated by AI from image analysis using HTML/CSS</p>
        </footer>
    </div>

    <script>
        function setActiveTab(tab) {
            // すべてのボタンからactiveクラスを削除
            document.querySelectorAll('.nav-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // クリックされたボタンにactiveクラスを追加
            event.target.classList.add('active');
            
            console.log('Active tab:', tab);
        }
        
        function handleAction(action) {
            const button = event.target;
            button.disabled = true;
            button.textContent = 'Processing...';
            
            // AIが画像から推定したアクション処理
            setTimeout(() => {
                button.disabled = false;
                button.textContent = 'Execute';
                console.log('Executed action:', action);
            }, 1000);
        }
    </script>
</body>
</html>"""

    css_template = """.image-generated-container {
    min-height: 100vh;
    background: BG_COLOR_PLACEHOLDER;
    color: TEXT_COLOR_PLACEHOLDER;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.app-header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.app-navigation {
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.nav-button {
    padding: 10px 20px;
    border: none;
    border-radius: 25px;
    background: transparent;
    color: TEXT_COLOR_PLACEHOLDER;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.nav-button:hover,
.nav-button.active {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
}

.app-main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
}

.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 30px;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.5rem;
}

.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.action-button.secondary {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    color: #8b4513;
}

.action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.app-footer {
    text-align: center;
    padding: 30px;
    background: BG_COLOR_PLACEHOLDER;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    margin-top: 50px;
}

@media (max-width: 768px) {
    .app-navigation {
        flex-direction: column;
        align-items: center;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
    }
    
    .app-header h1 {
        font-size: 2rem;
    }
}"""

    html_code = html_template.replace("DESCRIPTION_PLACEHOLDER", description)
    css_code = css_template.replace("BG_COLOR_PLACEHOLDER", analysis['bg_color'])
    css_code = css_code.replace("TEXT_COLOR_PLACEHOLDER", analysis['text_color'])

    return "✅ HTML/CSS generated from image analysis!", html_code, css_code

# AI指示による自動検出のための必須オブジェクト
with gr.Blocks(title="Multimodal UI Generator") as gradio_interface:
    gr.Markdown("# 🖼️ Multimodal UI Code Generator")
    gr.Markdown("画像をアップロードしてフロントエンドコードを自動生成します")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                label="UI Design Image",
                type="pil",
                height=400
            )
            
            description_input = gr.Textbox(
                label="Implementation Details",
                placeholder="このUIの機能や動作について説明してください...",
                lines=4,
                value="モダンなダッシュボード画面を作成"
            )
            
            framework_choice = gr.Radio(
                label="Target Framework",
                choices=["React", "Vue", "HTML/CSS"],
                value="React"
            )
            
            generate_btn = gr.Button("Generate UI Code", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            status_output = gr.Textbox(label="Generation Status", interactive=False)
            
            with gr.Tabs():
                with gr.Tab("Primary Code"):
                    primary_code_output = gr.Code(label="Main Component Code")
                    
                with gr.Tab("Styles"):
                    css_code_output = gr.Code(label="CSS Styles", language="css")
                    
                with gr.Tab("Additional Files"):
                    additional_output = gr.Code(label="Additional Configuration")
    
    # Event binding
    generate_btn.click(
        fn=analyze_image_and_generate_ui,
        inputs=[image_input, description_input, framework_choice],
        outputs=[status_output, primary_code_output, css_code_output, additional_output]
    )
    
    # サンプル例
    gr.Examples(
        examples=[
            [None, "シンプルなログイン画面", "React"],
            [None, "データ可視化ダッシュボード", "Vue"],
            [None, "商品一覧ページ", "HTML/CSS"]
        ],
        inputs=[image_input, description_input, framework_choice]
    )

# テスト用のスタンドアロン実行（コメントアウト - 自動検出システムとの競合を防ぐため）
# if __name__ == "__main__":
#     gradio_interface.launch()
