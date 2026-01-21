"""
家庭财务管理系统 - 轻量级 Web 服务器（使用 Python 标准库）

无需安装任何依赖，直接运行即可。
在同一局域网内提供网页访问，实现多设备数据同步。
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime
import socket

# 配置
PORT = 5000
DATA_FILE = 'finance_data.json'
HTML_FILE = 'family_finance_web.html'


class FinanceHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义 HTTP 请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # 主页 - 返回 HTML
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.send_html()
        
        # API: 获取数据
        elif parsed_path.path == '/api/data':
            self.send_api_data()
        
        # API: 导出到 Excel
        elif parsed_path.path == '/api/export/excel':
            self.send_api_export()
        
        # API: 从 Excel 导入
        elif parsed_path.path == '/api/import/excel':
            self.send_api_import()
        
        # 静态文件（如果有 CSS、JS 等）
        else:
            # 尝试作为静态文件服务
            super().do_GET()
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API: 保存数据
        if parsed_path.path == '/api/save':
            self.send_api_save()
        else:
            self.send_error(404, "API not found")
    
    def send_html(self):
        """返回带有服务器数据的 HTML"""
        try:
            # 读取 HTML 模板
            if not os.path.exists(HTML_FILE):
                self.send_error(404, f"HTML file not found: {HTML_FILE}")
                return
            
            with open(HTML_FILE, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 读取当前数据
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
            
            # 注入服务器同步脚本
            server_script = '''
        // ========== 服务器同步功能 ==========
        
        // 保存数据到服务器
        async function saveToServer() {
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
                    console.log('✓ 数据已同步到服务器', new Date().toLocaleTimeString());
                    showToast('数据已保存');
                } else {
                    console.error('✗ 保存失败:', result.error);
                    showToast('保存失败: ' + result.error);
                }
            } catch (error) {
                console.error('✗ 同步异常:', error);
                showToast('网络连接失败');
            }
        }
        
        // 从服务器刷新数据
        async function refreshFromServer() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                financeData = data;
                renderAll();
                console.log('✓ 数据已从服务器刷新', new Date().toLocaleTimeString());
                showToast('数据已刷新');
                
            } catch (error) {
                console.error('✗ 刷新失败:', error);
                showToast('刷新失败');
            }
        }
        
        // 显示提示信息
        function showToast(message) {
            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #4472C4;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            `;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }, 2000);
        }
        
        // 添加动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        // 添加刷新按钮到页面右上角
        const refreshBtn = document.createElement('button');
        refreshBtn.innerHTML = '🔄 刷新数据';
        refreshBtn.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: white;
            border: 2px solid #4472C4;
            color: #4472C4;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.2s;
        `;
        refreshBtn.onmouseover = function() {
            this.style.background = '#4472C4';
            this.style.color = 'white';
        };
        refreshBtn.onmouseout = function() {
            this.style.background = 'white';
            this.style.color = '#4472C4';
        };
        refreshBtn.onclick = refreshFromServer;
        document.body.appendChild(refreshBtn);
        
        // 重写原始的 addRecord 函数，添加自动保存
        const originalAddRecord = addRecord;
        addRecord = function(type) {
            originalAddRecord(type);
            setTimeout(saveToServer, 100); // 延迟保存，确保数据已更新
        }
        
        // 定期自动保存（每60秒）
        setInterval(saveToServer, 60000);
        
        // 页面卸载前保存
        window.addEventListener('beforeunload', saveToServer);
        
        // 替换原有的 loadData 调用
        console.log('服务器模式启动 - 数据已从服务器加载');
'''
            
            # 在 script 标签末尾添加服务器脚本
            html_content = html_content.replace(
                '// 页面加载时初始化\n    loadData();',
                f'{server_script}\n        // 页面加载时初始化\n        // 数据已从服务器加载，无需调用 loadData()\n'
            )
            
            # 返回 HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def send_api_data(self):
        """返回当前数据"""
        try:
            data = read_data()
            response = json.dumps(data, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def send_api_save(self):
        """保存数据"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            save_data(data)
            
            response = json.dumps({
                'success': True,
                'message': '数据保存成功',
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            response = json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
    
    def send_api_export(self):
        """导出数据到 Excel（调用同步脚本）"""
        try:
            import subprocess
            
            # 调用同步脚本
            result = subprocess.run(
                ['python', 'sync_finance_data.py'],
                input='2\n',
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                response = json.dumps({
                    'success': True,
                    'message': 'Excel 导出成功',
                    'output': result.stdout
                }, ensure_ascii=False)
            else:
                response = json.dumps({
                    'success': False,
                    'error': result.stderr or '导出失败'
                }, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            response = json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
    
    def send_api_import(self):
        """从 Excel 导入数据"""
        try:
            import subprocess
            
            # 调用同步脚本
            result = subprocess.run(
                ['python', 'sync_finance_data.py'],
                input='1\n',
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                # 读取更新后的数据
                data = read_data()
                response = json.dumps({
                    'success': True,
                    'message': 'Excel 导入成功',
                    'data': data
                }, ensure_ascii=False)
            else:
                response = json.dumps({
                    'success': False,
                    'error': result.stderr or '导入失败'
                }, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            response = json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))


def read_data():
    """读取数据文件"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    # 返回默认数据
    return {
        'deposit': [],
        'loan': [],
        'tax': [],
        'tfsa': [],
        'education': [],
        'expense': []
    }


def save_data(data):
    """保存数据到文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_local_ip():
    """获取本机 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def main():
    """启动服务器"""
    # 初始化数据文件
    if not os.path.exists(DATA_FILE):
        save_data(read_data())
    
    # 检查 HTML 文件
    if not os.path.exists(HTML_FILE):
        print(f"✗ 错误: 找不到网页文件 {HTML_FILE}")
        return
    
    # 获取本机 IP
    local_ip = get_local_ip()
    
    print("="*70)
    print("家庭财务管理系统 - Web 服务器")
    print("="*70)
    print(f"\n✓ 服务器启动成功！")
    print(f"\n📱 手机访问地址: http://{local_ip}:{PORT}")
    print(f"💻 电脑访问地址: http://localhost:{PORT}")
    print(f"\n⚠️  重要提示:")
    print(f"   1. 确保手机和电脑在同一 WiFi 网络")
    print(f"   2. 不要关闭此窗口，关闭窗口后服务器停止运行")
    print(f"   3. 数据自动保存到服务器，所有设备实时同步")
    print(f"   4. 页面右上角有'刷新数据'按钮，点击可手动刷新")
    print("\n" + "="*70)
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), FinanceHTTPRequestHandler) as httpd:
        print(f"\n🚀 服务器正在运行... (按 Ctrl+C 停止)\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ 服务器已停止")
            print("感谢使用家庭财务管理系统！")


if __name__ == "__main__":
    main()
