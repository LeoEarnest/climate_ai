"""
超輕量 Flask 應用 - 清晰易懂的路由管理
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from simple_rag import SimpleRAG

# 載入環境變數
load_dotenv()

# Flask 應用設置
CHATBOT = Flask(__name__)
CORS(CHATBOT)

# 全域 RAG 系統
rag_system = None

def init_system():
    """初始化 RAG 系統"""
    global rag_system
    
    # 檢查 API 金鑰
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 錯誤: 請在 .env 檔案中設置 GOOGLE_API_KEY")
        return False
    
    print("🚀 正在初始化 RAG 系統...")
    
    # 建立 RAG 系統
    rag_system = SimpleRAG(api_key)
    
    # 載入語言模型
    if not rag_system.load_llm():
        return False
    
    # 載入向量資料庫
    if not rag_system.load_vectorstore():
        print("⚠️  向量資料庫未找到，請先運行 simple_vectorstore.py 建立資料庫")
        return False
    
    print("✅ RAG 系統初始化完成！")
    return True

# ================================
# 路由定義
# ================================

@CHATBOT.route('/')
def home():
    """主頁 - 返回 HTML 檔案"""
    return send_from_directory('.', 'index.html')

@CHATBOT.route('/chat', methods=['POST'])
def chat():
    """聊天 API - 處理用戶訊息"""
    # 檢查系統狀態
    if not rag_system or not rag_system.is_ready():
        return jsonify({
            "success": False,
            "error": "系統未準備就緒"
        }), 503
    
    # 獲取請求數據
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        # 驗證訊息
        if not message:
            return jsonify({
                "success": False,
                "error": "訊息不能為空"
            }), 400
        
        if len(message) > 500:
            return jsonify({
                "success": False,
                "error": "訊息長度不能超過 500 字"
            }), 400
        
        # 處理聊天
        result = rag_system.chat(message, session_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"處理請求時發生錯誤: {str(e)}"
        }), 500

@CHATBOT.route('/clear', methods=['POST'])
def clear_history():
    """清除對話歷史"""
    if not rag_system:
        return jsonify({"success": False, "error": "系統未初始化"}), 503
    
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default') if data else 'default'
        
        rag_system.clear_history(session_id)
        return jsonify({
            "success": True,
            "message": "對話歷史已清除"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@CHATBOT.route('/status')
def status():
    """系統狀態檢查"""
    if not rag_system:
        return jsonify({
            "ready": False,
            "error": "系統未初始化"
        })
    
    return jsonify({
        "ready": rag_system.is_ready(),
        "llm_loaded": rag_system.llm is not None,
        "vectorstore_loaded": rag_system.vectorstore is not None
    })

# ================================
# 錯誤處理
# ================================

@CHATBOT.errorhandler(404)
def not_found(error):
    return jsonify({"error": "頁面不存在"}), 404

@CHATBOT.errorhandler(500)
def server_error(error):
    return jsonify({"error": "服務器錯誤"}), 500

# ================================
# 應用啟動
# ================================

if __name__ == '__main__':
    print("🤖 RAG 聊天機器人")
    print("=" * 30)
    
    # 檢查必要檔案
    if not os.path.exists('index.html'):
        print("❌ 找不到 index.html 檔案")
        print("請確保在同一目錄下有 index.html")
        exit()
    
    # 初始化系統
    if init_system():
        print("\n🌐 啟動 Flask 服務器...")
        print("📱 訪問地址: http://localhost:5000")
        print("🛑 按 Ctrl+C 停止服務\n")
        
        CHATBOT.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    else:
        print("\n❌ 系統初始化失敗，無法啟動服務")
        print("\n📋 請檢查:")
        print("1. .env 檔案中的 GOOGLE_API_KEY 是否正確")
        print("2. 是否已建立向量資料庫 (運行 simple_vectorstore.py)")
        print("3. 網路連接是否正常")