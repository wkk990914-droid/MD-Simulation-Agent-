from flask import Flask, request, jsonify, render_template, send_from_directory
import sys
import os

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from agentframework.agent.molecular_agent import molec_prep_agent

app = Flask(__name__)

# 配置静态文件目录，让Flask能够访问generated_files目录
app.config['UPLOAD_FOLDER'] = 'generated_files'
app.static_folder = 'generated_files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """提供文件下载功能"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # 调用分子模拟agent
        final_response = ""
        for chunk in molec_prep_agent.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            # 处理chunk格式，参考pretty_print_messages函数
            for node_name, node_update in chunk.items():
                if 'messages' in node_update:
                    messages = node_update["messages"]
                    for msg in messages:
                        if hasattr(msg, 'content') and hasattr(msg, 'role'):
                            # 如果是对象格式，且有content和role属性
                            if msg.role == 'assistant':
                                final_response = msg.content
                        elif hasattr(msg, 'content'):
                            # 如果只有content属性（如工具调用结果）
                            final_response = msg.content
                        elif isinstance(msg, dict):
                            # 如果是字典格式
                            if msg.get('role') == 'assistant':
                                final_response = msg.get('content', '')
                        else:
                            # 简单处理：将消息转换为字符串
                            final_response = str(msg)
        return jsonify({'response': final_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
