"""
家庭财务管理系统 - 本地 Web 服务器

在同一局域网内提供网页访问，实现多设备数据同步。
数据保存在服务器端，确保所有设备看到的是同一份数据。
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 数据文件
DATA_FILE = 'finance_data.json'
HTML_FILE = 'family_finance_web.html'

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    initial_data = {
        'deposit': [],
        'loan': [],
        'tax': [],
        'tfsa': [],
        'education': [],
        'expense': []
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)


def read_data():
    """读取数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'deposit': [],
            'loan': [],
            'tax': [],
            'tfsa': [],
            'education': [],
            'expense': []
        }


def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    """主页 - 返回带服务器端支持的网页"""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 读取当前数据并注入到网页
    data = read_data()
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    
    # 替换网页中的初始化数据
    import re
    html_content = re.sub(
        r'let financeData = \{[^}]*\};',
        f'let financeData = {data_json};',
        html_content,
        count=1,
        flags=re.DOTALL
    )
    
    # 修改 saveData 函数，改为保存到服务器
    new_save_function = '''
        async function saveData() {
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(financeData)
                });
                const result = await response.json();
                if (result.success) {
                    console.log('数据已保存到服务器');
                } else {
                    console.error('保存失败:', result.error);
                }
            } catch (error) {
                console.error('保存异常:', error);
            }
        }
        
        // 在添加记录后自动保存
        const originalAddRecord = addRecord;
        addRecord = function(type) {
            originalAddRecord(type);
            saveData();
        }
    '''
    
    # 替换原有的 saveData 函数（如果存在）或在适当位置插入
    html_content = html_content.replace(
        '// 保存数据到本地存储\n        saveData();',
        '// 数据自动同步到服务器'
    )
    
    # 在 script 标签末尾添加新的保存函数
    html_content = html_content.replace(
        '// 页面加载时初始化\n    loadData();',
        f'''// 页面加载时初始化
    // 数据已从服务器加载，无需调用 loadData()
    
    {new_save_function}
    
    // 定期自动保存（每30秒）
    setInterval(saveData, 30000);'''
    )
    
    return render_template_string(html_content)


@app.route('/api/save', methods=['POST'])
def api_save():
    """保存数据接口"""
    try:
        data = request.json
        save_data(data)
        return jsonify({'success': True, 'message': '数据保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/data')
def api_data():
    """获取数据接口"""
    data = read_data()
    return jsonify(data)


@app.route('/api/export/excel')
def export_excel():
    """导出数据到 Excel"""
    try:
        data = read_data()
        
        # 使用现有的同步工具导出到 Excel
        import subprocess
        result = subprocess.run(
            ['python', 'sync_finance_data.py'],
            input='2\n',  # 选择网页 -> Excel
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Excel 导出成功'})
        else:
            return jsonify({'success': False, 'error': result.stderr})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/import/excel')
def import_excel():
    """从 Excel 导入数据"""
    try:
        # 使用现有的同步工具从 Excel 导入
        import subprocess
        result = subprocess.run(
            ['python', 'sync_finance_data.py'],
            input='1\n',  # 选择 Excel -> 网页
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # 读取同步后的数据
            data = read_data()
            return jsonify({'success': True, 'message': 'Excel 导入成功', 'data': data})
        else:
            return jsonify({'success': False, 'error': result.stderr})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def get_local_ip():
    """获取本机 IP 地址"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == '__main__':
    print("="*60)
    print("家庭财务管理系统 - Web 服务器")
    print("="*60)
    
    local_ip = get_local_ip()
    port = 5000
    
    print(f"\n📱 手机访问地址: http://{local_ip}:{port}")
    print(f"💻 电脑访问地址: http://localhost:{port}")
    print(f"\n⚠️  确保手机和电脑在同一 WiFi 网络")
    print("⚠️  不要关闭此窗口，服务器运行期间数据会自动同步")
    print("="*60)
    
    # 运行服务器
    app.run(host='0.0.0.0', port=port, debug=False)
