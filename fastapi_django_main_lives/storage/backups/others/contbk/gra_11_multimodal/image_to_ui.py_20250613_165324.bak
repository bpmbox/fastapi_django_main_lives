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
    画像からUI要素を動的に検出・分析
    実際の画像コンテンツに基づいてUIパターンを決定
    """
    import numpy as np
    from collections import Counter
    
    width, height = image.size
    
    # より詳細な画像分析
    analysis = {
        "image_size": (width, height),
        "aspect_ratio": width / height,
        "detected_elements": [],
        "color_scheme": "modern",
        "layout_type": "grid" if width > height else "vertical"
    }
    
    # カラーパレット抽出
    image_array = np.array(image)
    if len(image_array.shape) == 3:
        # カラー画像の場合
        pixels = image_array.reshape(-1, 3)
        # 主要な色を抽出（K-means的なアプローチの簡易版）
        unique_colors = []
        for i in range(0, len(pixels), max(1, len(pixels)//100)):  # サンプリング
            color = pixels[i]
            unique_colors.append(tuple(color))
        
        color_counts = Counter(unique_colors)
        dominant_colors = color_counts.most_common(5)
        
        # 主要色に基づいてテーマ決定
        avg_r = sum([color[0][0] * color[1] for color in dominant_colors]) / sum([color[1] for color in dominant_colors])
        avg_g = sum([color[0][1] * color[1] for color in dominant_colors]) / sum([color[1] for color in dominant_colors])
        avg_b = sum([color[0][2] * color[1] for color in dominant_colors]) / sum([color[1] for color in dominant_colors])
        
        # HSVベースの分析
        max_rgb = max(avg_r, avg_g, avg_b)
        min_rgb = min(avg_r, avg_g, avg_b)
        saturation = (max_rgb - min_rgb) / max_rgb if max_rgb > 0 else 0
        
    else:
        # グレースケール画像
        avg_r = avg_g = avg_b = np.mean(image_array)
        saturation = 0
    
    # 明度計算
    brightness = (avg_r + avg_g + avg_b) / 3
    
    # 画像の複雑さを分析（エッジ検出的アプローチ）
    grayscale = image.convert('L')
    gray_array = np.array(grayscale)
    
    # 簡易エッジ検出
    edges = 0
    for i in range(1, gray_array.shape[0]-1):
        for j in range(1, gray_array.shape[1]-1):
            grad_x = abs(int(gray_array[i+1, j]) - int(gray_array[i-1, j]))
            grad_y = abs(int(gray_array[i, j+1]) - int(gray_array[i, j-1]))
            if grad_x + grad_y > 50:  # エッジ閾値
                edges += 1
    
    complexity = edges / (width * height)
    
    # 動的テーマ決定
    if brightness < 60:
        analysis["theme"] = "dark"
        analysis["bg_color"] = f"#1a1a1a"
        analysis["text_color"] = "#ffffff"
        analysis["accent_color"] = f"#{int(avg_r*0.8):02x}{int(avg_g*0.8):02x}{int(avg_b*0.8):02x}"
    elif brightness > 200:
        analysis["theme"] = "light" 
        analysis["bg_color"] = "#ffffff"
        analysis["text_color"] = "#333333"
        analysis["accent_color"] = f"#{int(avg_r*0.6):02x}{int(avg_g*0.6):02x}{int(avg_b*0.6):02x}"
    else:
        analysis["theme"] = "modern"
        analysis["bg_color"] = f"#{int(255-brightness*0.3):02x}{int(255-brightness*0.3):02x}{int(255-brightness*0.2):02x}"
        analysis["text_color"] = "#2c3e50"
        analysis["accent_color"] = f"#{int(avg_r):02x}{int(avg_g):02x}{int(avg_b):02x}"
    
    # 複雑さに基づくレイアウト決定
    if complexity > 0.1:
        analysis["layout_type"] = "complex_grid"
        analysis["components"] = ["header", "sidebar", "main_content", "footer", "cards"]
    elif complexity > 0.05:
        analysis["layout_type"] = "standard_grid"
        analysis["components"] = ["header", "navigation", "content_grid", "footer"]
    else:
        analysis["layout_type"] = "simple"
        analysis["components"] = ["header", "main_content", "actions"]
    
    # 色の彩度に基づく動的要素決定
    if saturation > 0.5:
        analysis["ui_style"] = "vibrant"
        analysis["has_animations"] = True
        analysis["gradient_style"] = "bold"
    elif saturation > 0.2:
        analysis["ui_style"] = "balanced"
        analysis["has_animations"] = True
        analysis["gradient_style"] = "subtle"
    else:
        analysis["ui_style"] = "minimal"
        analysis["has_animations"] = False
        analysis["gradient_style"] = "monochrome"
    
    # アスペクト比に基づくコンポーネント配置
    if width > height * 1.5:
        analysis["layout_orientation"] = "horizontal"
        analysis["nav_style"] = "horizontal"
    elif height > width * 1.5:
        analysis["layout_orientation"] = "vertical"
        analysis["nav_style"] = "vertical"
    else:
        analysis["layout_orientation"] = "square"
        analysis["nav_style"] = "compact"
    
    # 動的UI要素リスト生成
    base_elements = ["header", "navigation"]
    
    if complexity > 0.08:
        base_elements.extend(["sidebar", "search", "filters"])
    if saturation > 0.3:
        base_elements.extend(["hero_section", "call_to_action"])
    if width > 800:
        base_elements.extend(["content_grid", "cards"])
    else:
        base_elements.extend(["content_list"])
        
    analysis["detected_elements"] = [
        {"type": elem, "confidence": min(0.9, complexity + saturation + 0.3)}
        for elem in base_elements
    ]
    
    # メタデータ追加
    analysis["complexity_score"] = complexity
    analysis["saturation_score"] = saturation
    analysis["brightness_score"] = brightness / 255
    analysis["dominant_color"] = f"#{int(avg_r):02x}{int(avg_g):02x}{int(avg_b):02x}"
    
    return analysis

def generate_card_components(analysis, card_count=4):
    """動的なカードコンポーネント文字列を生成"""
    theme = analysis.get("theme", "modern")
    complexity = analysis.get("complexity_score", 0.05)
    ui_style = analysis.get("ui_style", "minimal")
    accent_color = analysis.get("accent_color", "#007bff")
    
    cards = []
    
    # 複雑さに基づいてカードの内容を動的生成
    card_types = [
        {
            "title": f"{theme.title()} Dashboard",
            "description": f"Image complexity: {complexity:.2f} - {ui_style} style interface",
            "action": "dashboard",
            "icon": "📊"
        },
        {
            "title": "Smart Analytics",
            "description": f"AI-detected layout: {analysis.get('layout_type', 'grid')}",
            "action": "analytics", 
            "icon": "🔍"
        },
        {
            "title": "Dynamic Controls",
            "description": f"Theme: {theme} | Animations: {analysis.get('has_animations', False)}",
            "action": "controls",
            "icon": "⚙️"
        },
        {
            "title": "Visual Elements",
            "description": f"Dominant color: {analysis.get('dominant_color', '#333')}",
            "action": "visual",
            "icon": "🎨"
        },
        {
            "title": "User Interface",
            "description": f"Navigation: {analysis.get('nav_style', 'horizontal')}",
            "action": "interface",
            "icon": "🖥️"
        },
        {
            "title": "Content Layout",
            "description": f"Aspect ratio: {analysis.get('aspect_ratio', 1):.2f}",
            "action": "layout",
            "icon": "📱"
        }
    ]
    
    for i in range(min(card_count, len(card_types))):
        card = card_types[i]
        card_jsx = f"""
                    <div className="feature-card dynamic-card-{i}">
                        <div className="card-icon">{card['icon']}</div>
                        <h3>{card['title']}</h3>
                        <p>{card['description']}</p>
                        <button 
                            onClick={{() => handleAction('{card['action']}')}}
                            disabled={{isLoading}}
                            className="action-button"
                            style={{{{background: '{accent_color}'}}}}
                        >
                            {{isLoading ? 'Processing...' : 'Execute'}}
                        </button>
                    </div>"""
        cards.append(card_jsx)
    
    return ''.join(cards)

def generate_react_from_analysis(analysis, description):
    """
    分析結果からReactコンポーネントを動的生成
    """
    component_name = "ImageGeneratedComponent"
    
    # 分析結果から動的値を取得
    theme = analysis.get("theme", "modern")
    bg_color = analysis.get("bg_color", "#f8f9fa")
    text_color = analysis.get("text_color", "#333333")
    accent_color = analysis.get("accent_color", "#007bff")
    ui_style = analysis.get("ui_style", "minimal")
    has_animations = analysis.get("has_animations", False)
    complexity = analysis.get("complexity_score", 0.05)
    layout_type = analysis.get("layout_type", "grid")
    
    # 動的グラデーション
    gradient_bg = f"linear-gradient(135deg, {accent_color}, {bg_color})"
    if theme == "dark":
        gradient_bg = f"linear-gradient(135deg, #2c3e50, #34495e)"
    elif theme == "light":
        gradient_bg = f"linear-gradient(135deg, #ecf0f1, #bdc3c7)"
    
    # 複雑さに基づくレイアウト決定
    grid_columns = "repeat(auto-fit, minmax(300px, 1fr))" if complexity > 0.1 else "repeat(auto-fit, minmax(250px, 1fr))"
    card_count = 6 if complexity > 0.08 else 4 if complexity > 0.05 else 2
    
    # 動的カードコンポーネント生成
    dynamic_cards = generate_card_components(analysis, card_count)
    
    # アニメーション用CSS
    animation_styles = ""
    if has_animations:
        animation_styles = """
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            .animate-fade { animation: fadeInUp 0.6s ease-out; }
            .animate-slide { animation: slideInLeft 0.4s ease-out; }
        """
    
    jsx_template = f"""import React, {{ useState, useEffect }} from 'react';
import './ImageGeneratedComponent.css';

const {component_name} = () => {{
    const [activeTab, setActiveTab] = useState('home');
    const [isLoading, setIsLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState(null);

    useEffect(() => {{
        // 画像分析データをシミュレート
        setAnalysisData({{
            theme: '{theme}',
            complexity: {complexity:.3f},
            uiStyle: '{ui_style}',
            layoutType: '{layout_type}',
            dominantColor: '{analysis.get("dominant_color", "#333")}',
            hasAnimations: {str(has_animations).lower()}
        }});
    }}, []);

    const handleAction = (action) => {{
        setIsLoading(true);
        console.log(`Executing AI-detected action: ${{action}}`);
        
        // AIが画像から推定したアクション処理
        setTimeout(() => {{
            setIsLoading(false);
            console.log(`Action completed: ${{action}}`);
        }}, 1000 + Math.random() * 2000);
    }};

    const tabs = ['home', 'features', 'analytics', 'settings'];

    return (
        <div className="image-generated-container">
            <header className="app-header {('animate-fade' if has_animations else '')}">
                <h1>AI Generated {theme.title()} UI</h1>
                <p className="description">{description}</p>
                {{analysisData && (
                    <div className="analysis-info">
                        <span>Complexity: {complexity:.2f}</span>
                        <span>Style: {ui_style}</span>
                        <span>Layout: {layout_type}</span>
                    </div>
                )}}
            </header>

            <nav className="app-navigation {('animate-slide' if has_animations else '')}">
                {{tabs.map(tab => (
                    <button
                        key={{tab}}
                        onClick={{() => setActiveTab(tab)}}
                        className={{`nav-button ${{activeTab === tab ? 'active' : ''}}`}}
                    >
                        {{tab.charAt(0).toUpperCase() + tab.slice(1)}}
                    </button>
                ))}}
            </nav>

            <main className="app-main">
                <div className="content-grid" style={{{{
                    gridTemplateColumns: '{grid_columns}',
                    gap: '{("2rem" if complexity > 0.1 else "1.5rem")}'
                }}}}>
                    {dynamic_cards}
                </div>
                
                {{theme === 'dark' && (
                    <div className="dark-mode-indicator">
                        🌙 Dark theme detected from image
                    </div>
                )}}
                
                {{complexity > 0.1 && (
                    <div className="complexity-notice">
                        ⚡ High complexity interface - Advanced features enabled
                    </div>
                )}}
            </main>

            <footer className="app-footer">
                <p>Generated by AI from image analysis • Theme: {theme} • Style: {ui_style}</p>
                <small>Complexity Score: {complexity:.3f} | Animations: {{analysis.get("has_animations", False)}}</small>
            </footer>
        </div>
    );
}};

export default {component_name};"""

    # 動的CSS生成
    css_template = f""".image-generated-container {{
    min-height: 100vh;
    background: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease;
}}

{animation_styles}

.app-header {{
    text-align: center;
    padding: 40px 20px;
    background: {gradient_bg};
    color: white;
    border-bottom: 3px solid {accent_color};
}}

.app-header h1 {{
    font-size: {("3rem" if complexity > 0.1 else "2.5rem")};
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}

.description {{
    font-size: 1.1rem;
    margin: 10px 0;
    opacity: 0.9;
}}

.analysis-info {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 15px;
    font-size: 0.9rem;
}}

.analysis-info span {{
    background: rgba(255,255,255,0.2);
    padding: 5px 12px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}}

.app-navigation {{
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    flex-wrap: wrap;
}}

.nav-button {{
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    background: transparent;
    color: {text_color};
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    font-size: 1rem;
}}

.nav-button:hover,
.nav-button.active {{
    background: {accent_color};
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

.app-main {{
    max-width: {("1400px" if complexity > 0.1 else "1200px")};
    margin: 0 auto;
    padding: 40px 20px;
}}

.content-grid {{
    display: grid;
    margin-top: 30px;
}}

.feature-card {{
    background: {("linear-gradient(135deg, #fff, #f8f9fa)" if theme == "light" else "#2c3e50" if theme == "dark" else "white")};
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, {("0.3" if theme == "dark" else "0.1")});
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid {accent_color}22;
}}

.feature-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, {("0.4" if theme == "dark" else "0.15")});
}}

.card-icon {{
    font-size: 2.5rem;
    margin-bottom: 15px;
    display: block;
}}

.feature-card h3 {{
    color: {accent_color};
    margin-bottom: 15px;
    font-size: 1.5rem;
}}

.feature-card p {{
    color: {text_color}88;
    line-height: 1.6;
    margin-bottom: 20px;
}}

.action-button {{
    background: {accent_color};
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 15px;
    font-size: 1rem;
}}

.action-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px {accent_color}66;
    filter: brightness(110%);
}}

.action-button:disabled {{
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}}

.dark-mode-indicator,
.complexity-notice {{
    text-align: center;
    padding: 15px;
    margin: 30px 0;
    background: {accent_color}11;
    border-radius: 10px;
    border-left: 4px solid {accent_color};
}}

.app-footer {{
    text-align: center;
    padding: 30px;
    background: {bg_color};
    border-top: 1px solid {accent_color}22;
    margin-top: 50px;
}}

.app-footer small {{
    display: block;
    margin-top: 10px;
    opacity: 0.7;
}}

@media (max-width: 768px) {{
    .app-navigation {{
        flex-direction: column;
        align-items: center;
    }}
    
    .content-grid {{
        grid-template-columns: 1fr !important;
    }}
    
    .app-header h1 {{
        font-size: 2rem;
    }}
    
    .analysis-info {{
        flex-direction: column;
        gap: 10px;
    }}
}}"""

    # プレースホルダーの置換
    jsx_code = jsx_template
    css_code = css_template

    return f"✅ Dynamic React component generated! Theme: {theme}, Complexity: {complexity:.2f}, Style: {ui_style}", jsx_code, css_code

def generate_vue_from_analysis(analysis, description):
    """
    分析結果からVue.jsコンポーネントを動的生成
    """
    
    # 分析結果から動的値を取得
    theme = analysis.get("theme", "modern")
    bg_color = analysis.get("bg_color", "#f8f9fa")
    text_color = analysis.get("text_color", "#333333")
    accent_color = analysis.get("accent_color", "#42b883")
    ui_style = analysis.get("ui_style", "minimal")
    has_animations = analysis.get("has_animations", False)
    complexity = analysis.get("complexity_score", 0.05)
    layout_type = analysis.get("layout_type", "grid")
    components = analysis.get("components", ["header", "main_content"])
    
    # 複雑さに基づいて機能を動的生成
    features = []
    feature_templates = [
        {
            "title": f"{theme.title()} Dashboard",
            "description": f"Image complexity: {complexity:.2f} - {ui_style} style",
            "action": "dashboard",
            "variant": "primary",
            "icon": "📊"
        },
        {
            "title": "Smart Analytics", 
            "description": f"Layout: {layout_type} | Theme: {theme}",
            "action": "analytics",
            "variant": "secondary",
            "icon": "🔍"
        },
        {
            "title": "Dynamic Controls",
            "description": f"Animations: {has_animations} | Style: {ui_style}",
            "action": "controls", 
            "variant": "primary",
            "icon": "⚙️"
        },
        {
            "title": "Visual Elements",
            "description": f"Color: {analysis.get('dominant_color', '#333')}",
            "action": "visual",
            "variant": "accent",
            "icon": "🎨"
        }
    ]
    
    # 複雑さに基づいて表示する機能数を決定
    feature_count = 4 if complexity > 0.08 else 3 if complexity > 0.05 else 2
    features = feature_templates[:feature_count]
    
    # アニメーション設定
    transition_class = "transition-all duration-300" if has_animations else ""
    
    vue_template = f"""<template>
  <div class="image-generated-container">
    <header class="app-header {transition_class}">
      <h1>AI Generated {theme.title()} Vue UI</h1>
      <p class="description">{description}</p>
      <div class="analysis-info" v-if="analysisData">
        <span>Complexity: {{{{ analysisData.complexity.toFixed(2) }}}}</span>
        <span>Style: {{{{ analysisData.uiStyle }}}}</span>
        <span>Layout: {{{{ analysisData.layoutType }}}}</span>
      </div>
    </header>

    <nav class="app-navigation {transition_class}">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="setActiveTab(tab)"
        :class="['nav-button', {{ active: activeTab === tab }}]"
        :style="tabButtonStyle"
      >
        {{{{ tab.charAt(0).toUpperCase() + tab.slice(1) }}}}
      </button>
    </nav>

    <main class="app-main">
      <div class="content-grid" :style="gridStyle">
        <div 
          v-for="feature in features"
          :key="feature.id"
          :class="['feature-card', '{transition_class}', `card-${{feature.variant}}`]"
        >
          <div class="card-icon">{{{{ feature.icon }}}}</div>
          <h3>{{{{ feature.title }}}}</h3>
          <p>{{{{ feature.description }}}}</p>
          <button 
            @click="handleAction(feature.action)"
            :disabled="isLoading"
            :class="['action-button', feature.variant]"
            :style="getButtonStyle(feature.variant)"
          >
            {{{{ isLoading ? 'Processing...' : 'Execute' }}}}
          </button>
        </div>
      </div>
      
      <div v-if="theme === 'dark'" class="theme-indicator">
        🌙 Dark theme detected from image analysis
      </div>
      
      <div v-if="complexity > 0.1" class="complexity-notice">
        ⚡ High complexity interface - Advanced features enabled
      </div>
    </main>

    <footer class="app-footer">
      <p>Generated by AI from image analysis using Vue.js</p>
      <small>Theme: {theme} | Style: {ui_style} | Complexity: {{{{ complexity.toFixed(3) }}}}</small>
    </footer>
  </div>
</template>

<script>
import {{ ref, reactive, computed, onMounted }} from 'vue'

export default {{
  name: 'ImageGeneratedComponent',
  setup() {{
    const activeTab = ref('home')
    const isLoading = ref(false)
    const complexity = ref({complexity})
    
    const tabs = ['home', 'features', 'analytics', 'settings']
    
    const analysisData = reactive({{
      theme: '{theme}',
      complexity: {complexity},
      uiStyle: '{ui_style}',
      layoutType: '{layout_type}',
      dominantColor: '{analysis.get("dominant_color", "#333")}',
      hasAnimations: {str(has_animations).lower()}
    }})
    
    const features = reactive({features})

    const gridStyle = computed(() => ({{
      gridTemplateColumns: '{("repeat(auto-fit, minmax(300px, 1fr))" if complexity > 0.1 else "repeat(auto-fit, minmax(250px, 1fr))")}',
      gap: '{("2rem" if complexity > 0.1 else "1.5rem")}'
    }}))
    
    const tabButtonStyle = computed(() => ({{
      padding: '12px 24px',
      borderRadius: '25px',
      border: 'none',
      backgroundColor: 'transparent',
      color: '{text_color}',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      fontWeight: '500'
    }}))

    const setActiveTab = (tab) => {{
      activeTab.value = tab
    }}

    const handleAction = (action) => {{
      isLoading.value = true
      console.log(`Executing AI-detected action: ${{action}}`)
      
      setTimeout(() => {{
        isLoading.value = false
        console.log(`Action completed: ${{action}}`)
      }}, 1000 + Math.random() * 2000)
    }}
    
    const getButtonStyle = (variant) => {{
      const baseStyle = {{
        border: 'none',
        padding: '12px 25px',
        borderRadius: '8px',
        cursor: 'pointer',
        fontWeight: '600',
        transition: 'all 0.3s ease',
        marginTop: '15px',
        color: 'white'
      }}
      
      switch(variant) {{
        case 'primary':
          return {{ ...baseStyle, background: '{accent_color}' }}
        case 'secondary':
          return {{ ...baseStyle, background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)', color: '#8b4513' }}
        case 'accent':
          return {{ ...baseStyle, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
        default:
          return {{ ...baseStyle, background: '{accent_color}' }}
      }}
    }}

    onMounted(() => {{
      console.log('Vue component mounted with analysis data:', analysisData)
    }})

    return {{
      activeTab,
      isLoading,
      complexity,
      tabs,
      features,
      analysisData,
      gridStyle,
      tabButtonStyle,
      setActiveTab,
      handleAction,
      getButtonStyle
    }}
  }}
}}
</script>

<style scoped>
.image-generated-container {{
  min-height: 100vh;
  background: {bg_color};
  color: {text_color};
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

{("@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }" if has_animations else "")}
{(".transition-all { animation: fadeInUp 0.6s ease-out; }" if has_animations else "")}

.app-header {{
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, {accent_color} 0%, #35495e 100%);
  color: white;
  border-bottom: 3px solid {accent_color};
}}

.app-header h1 {{
  font-size: {("3rem" if complexity > 0.1 else "2.5rem")};
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}

.description {{
  font-size: 1.1rem;
  margin: 10px 0;
  opacity: 0.9;
}}

.analysis-info {{
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
  font-size: 0.9rem;
  flex-wrap: wrap;
}}

.analysis-info span {{
  background: rgba(255,255,255,0.2);
  padding: 5px 12px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}}

.app-navigation {{
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  flex-wrap: wrap;
}}

.nav-button:hover,
.nav-button.active {{
  background: {accent_color} !important;
  color: white !important;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

.app-main {{
  max-width: {("1400px" if complexity > 0.1 else "1200px")};
  margin: 0 auto;
  padding: 40px 20px;
}}

.content-grid {{
  display: grid;
  margin-top: 30px;
}}

.feature-card {{
  background: {("linear-gradient(135deg, #fff, #f8f9fa)" if theme == "light" else "#2c3e50" if theme == "dark" else "white")};
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, {("0.3" if theme == "dark" else "0.1")});
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid {accent_color}22;
}}

.feature-card:hover {{
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, {("0.4" if theme == "dark" else "0.15")});
}}

.card-icon {{
  font-size: 2.5rem;
  margin-bottom: 15px;
  display: block;
}}

.feature-card h3 {{
  color: {accent_color};
  margin-bottom: 15px;
  font-size: 1.5rem;
}}

.feature-card p {{
  color: {text_color}88;
  line-height: 1.6;
  margin-bottom: 20px;
}}

.action-button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(66, 184, 131, 0.4);
  filter: brightness(110%);
}}

.action-button:disabled {{
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}}

.theme-indicator,
.complexity-notice {{
  text-align: center;
  padding: 15px;
  margin: 30px 0;
  background: {accent_color}11;
  border-radius: 10px;
  border-left: 4px solid {accent_color};
}}

.app-footer {{
  text-align: center;
  padding: 30px;
  background: {bg_color};
  border-top: 1px solid {accent_color}22;
  margin-top: 50px;
}}

.app-footer small {{
  display: block;
  margin-top: 10px;
  opacity: 0.7;
}}

@media (max-width: 768px) {{
  .app-navigation {{
    flex-direction: column;
    align-items: center;
  }}
  
  .content-grid {{
    grid-template-columns: 1fr !important;
  }}
  
  .app-header h1 {{
    font-size: 2rem;
  }}
  
  .analysis-info {{
    flex-direction: column;
    gap: 10px;
  }}
}}
</style>"""

    return f"✅ Dynamic Vue.js component generated! Theme: {theme}, Complexity: {complexity:.2f}, Style: {ui_style}", vue_template

def generate_html_from_analysis(analysis, description):
    """
    分析結果からHTML/CSSを動的生成
    """
    
    # 分析結果から動的値を取得
    theme = analysis.get("theme", "modern")
    bg_color = analysis.get("bg_color", "#f8f9fa")
    text_color = analysis.get("text_color", "#333333")
    accent_color = analysis.get("accent_color", "#007bff")
    ui_style = analysis.get("ui_style", "minimal")
    has_animations = analysis.get("has_animations", False)
    complexity = analysis.get("complexity_score", 0.05)
    layout_type = analysis.get("layout_type", "grid")
    
    # 複雑さに基づいて機能カードを生成
    feature_cards = []
    feature_data = [
        {
            "title": f"{theme.title()} Dashboard",
            "description": f"Image complexity: {complexity:.2f} - {ui_style} style",
            "action": "dashboard",
            "icon": "📊"
        },
        {
            "title": "Smart Analytics",
            "description": f"Layout: {layout_type} | Theme: {theme}",
            "action": "analytics", 
            "icon": "🔍"
        },
        {
            "title": "Dynamic Controls",
            "description": f"Animations: {has_animations} | Navigation: {analysis.get('nav_style', 'horizontal')}",
            "action": "controls",
            "icon": "⚙️"
        },
        {
            "title": "Visual Elements",
            "description": f"Dominant color: {analysis.get('dominant_color', '#333')} | Brightness: {analysis.get('brightness_score', 0.5):.2f}",
            "action": "visual",
            "icon": "🎨"
        }
    ]
    
    # 複雑さに基づいてカード数を決定
    card_count = 4 if complexity > 0.08 else 3 if complexity > 0.05 else 2
    
    for i, feature in enumerate(feature_data[:card_count]):
        card_html = f"""
                <div class="feature-card dynamic-card-{i}" data-feature="{feature['action']}">
                    <div class="card-icon">{feature['icon']}</div>
                    <h3>{feature['title']}</h3>
                    <p>{feature['description']}</p>
                    <button class="action-button" onclick="handleAction('{feature['action']}', this)">
                        Execute
                    </button>
                </div>"""
        feature_cards.append(card_html)
    
    # グリッドスタイル
    grid_columns = "repeat(auto-fit, minmax(300px, 1fr))" if complexity > 0.1 else "repeat(auto-fit, minmax(250px, 1fr))"
    
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated {theme.title()} UI</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body data-theme="{theme}" data-complexity="{complexity:.3f}">
    <div class="image-generated-container">
        <header class="app-header {('animate-fade' if has_animations else '')}">
            <h1>AI Generated {theme.title()} HTML UI</h1>
            <p class="description">{description}</p>
            <div class="analysis-info">
                <span>Complexity: {complexity:.2f}</span>
                <span>Style: {ui_style}</span>
                <span>Layout: {layout_type}</span>
            </div>
        </header>

        <nav class="app-navigation {('animate-slide' if has_animations else '')}">
            <button class="nav-button active" onclick="setActiveTab('home', this)">Home</button>
            <button class="nav-button" onclick="setActiveTab('features', this)">Features</button>
            <button class="nav-button" onclick="setActiveTab('analytics', this)">Analytics</button>
            <button class="nav-button" onclick="setActiveTab('settings', this)">Settings</button>
        </nav>

        <main class="app-main">
            <div class="content-grid" style="grid-template-columns: {grid_columns}; gap: {('2rem' if complexity > 0.1 else '1.5rem')};">
                {''.join(feature_cards)}
            </div>
            
            {('<div class="theme-indicator">🌙 Dark theme detected from image analysis</div>' if theme == 'dark' else '')}
            {('<div class="complexity-notice">⚡ High complexity interface - Advanced features enabled</div>' if complexity > 0.1 else '')}
        </main>

        <footer class="app-footer">
            <p>Generated by AI from image analysis using HTML/CSS</p>
            <small>Theme: {theme} | Style: {ui_style} | Complexity: {complexity:.3f}</small>
        </footer>
    </div>

    <script>
        // グローバル変数
        let isLoading = false;
        let analysisData = {{
            theme: '{theme}',
            complexity: {complexity},
            uiStyle: '{ui_style}',
            layoutType: '{layout_type}',
            dominantColor: '{analysis.get("dominant_color", "#333")}',
            hasAnimations: {str(has_animations).lower()}
        }};
        
        function setActiveTab(tab, button) {{
            // すべてのボタンからactiveクラスを削除
            document.querySelectorAll('.nav-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // クリックされたボタンにactiveクラスを追加
            button.classList.add('active');
            
            console.log('Active tab:', tab);
            console.log('Analysis data:', analysisData);
        }}
        
        function handleAction(action, button) {{
            if (isLoading) return;
            
            isLoading = true;
            const originalText = button.textContent;
            button.disabled = true;
            button.textContent = 'Processing...';
            button.style.opacity = '0.6';
            
            console.log(`Executing AI-detected action: ${{action}}`);
            
            // AIが画像から推定したアクション処理
            const processingTime = 1000 + Math.random() * 2000;
            setTimeout(() => {{
                isLoading = false;
                button.disabled = false;
                button.textContent = originalText;
                button.style.opacity = '1';
                console.log(`Action completed: ${{action}}`);
                
                // 視覚的フィードバック
                const card = button.closest('.feature-card');
                card.style.transform = 'scale(1.05)';
                setTimeout(() => {{
                    card.style.transform = '';
                }}, 200);
            }}, processingTime);
        }}
        
        // 動的インタラクション
        function addDynamicEffects() {{
            const cards = document.querySelectorAll('.feature-card');
            cards.forEach((card, index) => {{
                card.addEventListener('mouseenter', () => {{
                    if (analysisData.hasAnimations) {{
                        card.style.transform = 'translateY(-10px) scale(1.02)';
                        card.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
                    }}
                }});
                
                card.addEventListener('mouseleave', () => {{
                    card.style.transform = '';
                    card.style.boxShadow = '';
                }});
            }});
        }}
        
        // ページ読み込み時の初期化
        document.addEventListener('DOMContentLoaded', () => {{
            console.log('HTML UI initialized with analysis data:', analysisData);
            addDynamicEffects();
            
            // テーマに基づく動的スタイル調整
            if (analysisData.theme === 'dark') {{
                document.body.classList.add('dark-theme');
            }}
            
            // 複雑さに基づく動的調整
            if (analysisData.complexity > 0.1) {{
                document.body.classList.add('high-complexity');
            }}
        }});
    </script>
</body>
</html>"""

    # 動的CSS生成
    css_template = f""".image-generated-container {{
    min-height: 100vh;
    background: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease;
}}

{("@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }" if has_animations else "")}
{("@keyframes slideInLeft { from { opacity: 0; transform: translateX(-50px); } to { opacity: 1; transform: translateX(0); } }" if has_animations else "")}
{(".animate-fade { animation: fadeInUp 0.6s ease-out; }" if has_animations else "")}
{(".animate-slide { animation: slideInLeft 0.4s ease-out; }" if has_animations else "")}

.app-header {{
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, {accent_color} 0%, {bg_color} 100%);
    color: white;
    border-bottom: 3px solid {accent_color};
}}

.app-header h1 {{
    font-size: {("3rem" if complexity > 0.1 else "2.5rem")};
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}

.description {{
    font-size: 1.1rem;
    margin: 10px 0;
    opacity: 0.9;
}}

.analysis-info {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 15px;
    font-size: 0.9rem;
    flex-wrap: wrap;
}}

.analysis-info span {{
    background: rgba(255,255,255,0.2);
    padding: 5px 12px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}}

.app-navigation {{
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    flex-wrap: wrap;
}}

.nav-button {{
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    background: transparent;
    color: {text_color};
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    font-size: 1rem;
}}

.nav-button:hover,
.nav-button.active {{
    background: {accent_color};
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

.app-main {{
    max-width: {("1400px" if complexity > 0.1 else "1200px")};
    margin: 0 auto;
    padding: 40px 20px;
}}

.content-grid {{
    display: grid;
    margin-top: 30px;
}}

.feature-card {{
    background: {("linear-gradient(135deg, #fff, #f8f9fa)" if theme == "light" else "#2c3e50" if theme == "dark" else "white")};
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, {("0.3" if theme == "dark" else "0.1")});
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid {accent_color}22;
    cursor: pointer;
}}

.feature-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, {("0.4" if theme == "dark" else "0.15")});
}}

.card-icon {{
    font-size: 2.5rem;
    margin-bottom: 15px;
    display: block;
}}

.feature-card h3 {{
    color: {accent_color};
    margin-bottom: 15px;
    font-size: 1.5rem;
}}

.feature-card p {{
    color: {text_color}88;
    line-height: 1.6;
    margin-bottom: 20px;
}}

.action-button {{
    background: {accent_color};
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 15px;
    font-size: 1rem;
    width: 100%;
}}

.action-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px {accent_color}66;
    filter: brightness(110%);
}}

.action-button:disabled {{
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}}

.theme-indicator,
.complexity-notice {{
    text-align: center;
    padding: 15px;
    margin: 30px 0;
    background: {accent_color}11;
    border-radius: 10px;
    border-left: 4px solid {accent_color};
}}

.app-footer {{
    text-align: center;
    padding: 30px;
    background: {bg_color};
    border-top: 1px solid {accent_color}22;
    margin-top: 50px;
}}

.app-footer small {{
    display: block;
    margin-top: 10px;
    opacity: 0.7;
}}

/* テーマ固有のスタイル */
.dark-theme .feature-card {{
    background: #34495e;
    color: #ecf0f1;
}}

.high-complexity .feature-card {{
    border-width: 2px;
}}

.high-complexity .action-button {{
    background: linear-gradient(135deg, {accent_color}, #8e44ad);
}}

@media (max-width: 768px) {{
    .app-navigation {{
        flex-direction: column;
        align-items: center;
    }}
    
    .content-grid {{
        grid-template-columns: 1fr !important;
    }}
    
    .app-header h1 {{
        font-size: 2rem;
    }}
    
    .analysis-info {{
        flex-direction: column;
        gap: 10px;
    }}
}}"""

    return f"✅ Dynamic HTML/CSS generated! Theme: {theme}, Complexity: {complexity:.2f}, Style: {ui_style}", html_template, css_template

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
