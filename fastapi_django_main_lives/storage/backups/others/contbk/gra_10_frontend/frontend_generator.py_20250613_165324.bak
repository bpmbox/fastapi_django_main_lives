import gradio as gr
import os
import json
from pathlib import Path

def generate_react_component(component_name, props_description, styling_preference):
    """
    React コンポーネントを動的生成する関数
    """
    if not component_name:
        return "コンポーネント名を入力してください", "", ""
    
    # React コンポーネントの基本構造を生成
    react_jsx = f"""import React, {{ useState, useEffect }} from 'react';
import './{{component_name}}.css';

const {component_name} = (props) => {{
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {{
        // コンポーネント初期化処理
        console.log('{component_name} component mounted');
    }}, []);

    const handleAction = () => {{
        setLoading(true);
        // AI が生成したアクション処理
        setTimeout(() => {{
            setLoading(false);
            console.log('Action completed');
        }}, 1000);
    }};

    return (
        <div className="{component_name.lower()}-container">
            <div className="header">
                <h2>{component_name}</h2>
                <p>{{props_description}}</p>
            </div>
            
            <div className="content">
                {{loading ? (
                    <div className="loading">Loading...</div>
                ) : (
                    <div className="main-content">
                        <button 
                            onClick={{handleAction}}
                            className="action-button"
                            disabled={{loading}}
                        >
                            Execute Action
                        </button>
                    </div>
                )}}
            </div>
        </div>
    );
}};

export default {component_name};"""

    # CSS スタイルを生成
    css_styles = f""".{component_name.lower()}-container {{
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background: {get_background_color(styling_preference)};
}}

.header {{
    text-align: center;
    margin-bottom: 30px;
}}

.header h2 {{
    color: {get_text_color(styling_preference)};
    font-size: 2rem;
    margin-bottom: 10px;
}}

.header p {{
    color: {get_secondary_color(styling_preference)};
    font-size: 1.1rem;
}}

.content {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.action-button {{
    background: {get_primary_color(styling_preference)};
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.action-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}}

.action-button:disabled {{
    opacity: 0.6;
    cursor: not-allowed;
}}

.loading {{
    padding: 20px;
    text-align: center;
    font-style: italic;
    color: {get_secondary_color(styling_preference)};
}}

@media (max-width: 768px) {{
    .{component_name.lower()}-container {{
        margin: 10px;
        padding: 15px;
    }}
    
    .header h2 {{
        font-size: 1.5rem;
    }}
}}"""

    # パッケージ.json の設定
    package_json = {
        "name": f"{component_name.lower()}-component",
        "version": "1.0.0",
        "description": f"AI generated React component: {component_name}",
        "main": f"{component_name}.jsx",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@vitejs/plugin-react": "^4.0.0",
            "vite": "^4.0.0"
        },
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "ai_generated": True,
        "created_by": "AI Auto-Generation System",
        "component_description": props_description
    }

    return (
        f"✅ React component '{component_name}' generated successfully!",
        react_jsx,
        css_styles,
        json.dumps(package_json, indent=2)
    )

def get_background_color(style):
    styles = {
        "Modern": "#ffffff",
        "Dark": "#1a1a1a", 
        "Colorful": "#f0f8ff",
        "Minimal": "#fafafa"
    }
    return styles.get(style, "#ffffff")

def get_text_color(style):
    styles = {
        "Modern": "#2c3e50",
        "Dark": "#ffffff",
        "Colorful": "#2c3e50", 
        "Minimal": "#333333"
    }
    return styles.get(style, "#2c3e50")

def get_primary_color(style):
    styles = {
        "Modern": "#3498db",
        "Dark": "#e74c3c",
        "Colorful": "#9b59b6",
        "Minimal": "#95a5a6"
    }
    return styles.get(style, "#3498db")

def get_secondary_color(style):
    styles = {
        "Modern": "#7f8c8d",
        "Dark": "#bdc3c7",
        "Colorful": "#34495e",
        "Minimal": "#666666"
    }
    return styles.get(style, "#7f8c8d")

def generate_vue_component(component_name, props_description, styling_preference):
    """
    Vue.js コンポーネントを動的生成する関数
    """
    if not component_name:
        return "コンポーネント名を入力してください", ""
    
    vue_component = f"""<template>
  <div class="{component_name.lower()}-container">
    <div class="header">
      <h2>{component_name}</h2>
      <p>{props_description}</p>
    </div>
    
    <div class="content">
      <div v-if="loading" class="loading">
        Loading...
      </div>
      <div v-else class="main-content">
        <button 
          @click="handleAction"
          class="action-button"
          :disabled="loading"
        >
          Execute Action
        </button>
        
        <div v-if="result" class="result">
          {{{{ result }}}}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {{ ref, onMounted }} from 'vue'

export default {{
  name: '{component_name}',
  props: {{
    initialData: {{
      type: Object,
      default: () => ({{}})
    }}
  }},
  setup(props) {{
    const loading = ref(false)
    const result = ref(null)
    const data = ref(props.initialData)

    const handleAction = async () => {{
      loading.value = true
      try {{
        // AI が生成したアクション処理
        await new Promise(resolve => setTimeout(resolve, 1000))
        result.value = 'Action completed successfully!'
      }} catch (error) {{
        result.value = 'Action failed: ' + error.message
      }} finally {{
        loading.value = false
      }}
    }}

    onMounted(() => {{
      console.log('{component_name} component mounted')
    }})

    return {{
      loading,
      result,
      data,
      handleAction
    }}
  }}
}}
</script>

<style scoped>
.{component_name.lower()}-container {{
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: {get_background_color(styling_preference)};
}}

.header {{
  text-align: center;
  margin-bottom: 30px;
}}

.header h2 {{
  color: {get_text_color(styling_preference)};
  font-size: 2rem;
  margin-bottom: 10px;
}}

.header p {{
  color: {get_secondary_color(styling_preference)};
  font-size: 1.1rem;
}}

.content {{
  display: flex;
  flex-direction: column;
  align-items: center;
}}

.action-button {{
  background: {get_primary_color(styling_preference)};
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}}

.action-button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}}

.action-button:disabled {{
  opacity: 0.6;
  cursor: not-allowed;
}}

.loading {{
  padding: 20px;
  text-align: center;
  font-style: italic;
  color: {get_secondary_color(styling_preference)};
}}

.result {{
  margin-top: 20px;
  padding: 15px;
  border-radius: 6px;
  background: rgba(52, 152, 219, 0.1);
  color: {get_text_color(styling_preference)};
  text-align: center;
}}

@media (max-width: 768px) {{
  .{component_name.lower()}-container {{
    margin: 10px;
    padding: 15px;
  }}
  
  .header h2 {{
    font-size: 1.5rem;
  }}
}}
</style>"""

    return f"✅ Vue component '{component_name}' generated successfully!", vue_component

# AI指示による自動検出のための必須オブジェクト
with gr.Blocks(title="Frontend Framework Generator") as gradio_interface:
    gr.Markdown("# 🚀 Frontend Framework Auto-Generator")
    gr.Markdown("AIがReact・Vue.jsコンポーネントを自動生成します")
    
    with gr.Tab("⚛️ React Generator"):
        gr.Markdown("### React Component Generator")
        
        with gr.Row():
            react_name = gr.Textbox(
                label="Component Name",
                placeholder="MyAwesomeComponent",
                value="WeatherWidget"
            )
            react_props = gr.Textbox(
                label="Component Description", 
                placeholder="天気情報を表示するウィジェット",
                value="Interactive weather information display"
            )
            react_style = gr.Dropdown(
                label="Styling Preference",
                choices=["Modern", "Dark", "Colorful", "Minimal"],
                value="Modern"
            )
        
        react_generate_btn = gr.Button("Generate React Component", variant="primary")
        
        with gr.Row():
            react_status = gr.Textbox(label="Generation Status", interactive=False)
        
        with gr.Tabs():
            with gr.Tab("JSX Code"):
                react_jsx_output = gr.Code(label="React Component", language="javascript")
            with gr.Tab("CSS Styles"):
                react_css_output = gr.Code(label="CSS Styles", language="css")
            with gr.Tab("Package.json"):
                react_package_output = gr.Code(label="Package Configuration", language="json")
    
    with gr.Tab("🔧 Vue.js Generator"):
        gr.Markdown("### Vue.js Component Generator")
        
        with gr.Row():
            vue_name = gr.Textbox(
                label="Component Name",
                placeholder="MyVueComponent", 
                value="DataDashboard"
            )
            vue_props = gr.Textbox(
                label="Component Description",
                placeholder="データ可視化ダッシュボード",
                value="Interactive data visualization dashboard"
            )
            vue_style = gr.Dropdown(
                label="Styling Preference",
                choices=["Modern", "Dark", "Colorful", "Minimal"],
                value="Modern"
            )
        
        vue_generate_btn = gr.Button("Generate Vue Component", variant="primary")
        
        with gr.Row():
            vue_status = gr.Textbox(label="Generation Status", interactive=False)
        
        vue_output = gr.Code(label="Vue.js Component", language="javascript")
    
    # Event bindings
    react_generate_btn.click(
        fn=generate_react_component,
        inputs=[react_name, react_props, react_style],
        outputs=[react_status, react_jsx_output, react_css_output, react_package_output]
    )
    
    vue_generate_btn.click(
        fn=generate_vue_component,
        inputs=[vue_name, vue_props, vue_style], 
        outputs=[vue_status, vue_output]
    )

# テスト用のスタンドアロン実行（コメントアウト - 自動検出システムとの競合を防ぐため）
# if __name__ == "__main__":
#     gradio_interface.launch()
