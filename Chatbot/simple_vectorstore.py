"""
簡化向量資料庫 - 使用 FAISS 避免編譯問題
"""
import os
import pickle
import numpy as np
from typing import List, Dict, Any
import bs4
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import WebBaseLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SimpleVectorStore:
    """簡化版向量資料庫 - 使用 FAISS"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.encoder = SentenceTransformer(model_name)
        self.documents = []  # 儲存原始文檔
        self.embeddings = None  # 儲存向量
        self.index = None  # FAISS 索引
        
    def add_documents(self, docs: List[str]):
        """添加文檔到向量庫"""
        print(f"📄 正在處理 {len(docs)} 個文檔...")
        
        # 儲存文檔
        self.documents.extend(docs)
        
        # 計算向量
        print("🔢 正在計算向量嵌入...")
        new_embeddings = self.encoder.encode(docs, show_progress_bar=True)
        
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        # 建立 FAISS 索引
        self._build_index()
        print(f"✅ 已添加 {len(docs)} 個文檔，總計 {len(self.documents)} 個")
    
    def _build_index(self):
        """建立 FAISS 索引"""
        try:
            import faiss
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # 使用內積相似度
            
            # 正規化向量
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)
            
        except ImportError:
            print("⚠️ FAISS 未安裝，使用簡單的 numpy 搜尋")
            self.index = None
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """搜尋相似文檔"""
        if len(self.documents) == 0:
            return []
        
        # 計算查詢向量
        query_embedding = self.encoder.encode([query])
        
        if self.index is not None:
            # 使用 FAISS 搜尋
            import faiss
            faiss.normalize_L2(query_embedding)
            scores, indices = self.index.search(query_embedding, k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'content': self.documents[idx],
                        'score': float(score)
                    })
            return results
        else:
            # 使用 numpy 計算相似度
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # 獲取前 k 個最相似的文檔
            top_indices = np.argsort(similarities)[-k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    'content': self.documents[idx],
                    'score': float(similarities[idx])
                })
            return results
    
    def save(self, path: str):
        """儲存向量庫"""
        data = {
            'documents': self.documents,
            'embeddings': self.embeddings,
            'model_name': self.model_name
        }
        
        # 修正路徑問題
        dir_path = os.path.dirname(path)
        if dir_path:  # 只有當目錄路徑不為空時才建立
            os.makedirs(dir_path, exist_ok=True)
            
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f"💾 向量庫已儲存至: {path}")
    
    def load(self, path: str) -> bool:
        """載入向量庫"""
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
            
            self.documents = data['documents']
            self.embeddings = data['embeddings']
            self.model_name = data['model_name']
            
            # 重新載入模型
            self.encoder = SentenceTransformer(self.model_name)
            
            # 重建索引
            if self.embeddings is not None:
                self._build_index()
            
            print(f"📂 向量庫已載入: {len(self.documents)} 個文檔")
            return True
            
        except Exception as e:
            print(f"❌ 載入失敗: {e}")
            return False


class DocumentProcessor:
    """文檔處理器"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
    
    def process_web_urls(self, urls: List[str]) -> List[str]:
        """處理網頁 URL"""
        all_chunks = []
        
        for url in urls:
            try:
                print(f"🌐 載入網頁: {url}")
                loader = WebBaseLoader(
                    web_paths=[url],
                    bs_kwargs=dict(
                        parse_only=bs4.SoupStrainer(["p", "h1", "h2", "h3", "article"])
                    )
                )
                docs = loader.load()
                
                for doc in docs:
                    chunks = self.text_splitter.split_text(doc.page_content)
                    all_chunks.extend(chunks)
                    
                print(f"  ✅ 已處理，獲得 {len(chunks)} 個文字塊")
                
            except Exception as e:
                print(f"  ❌ 處理失敗: {e}")
        
        return [chunk for chunk in all_chunks if len(chunk.strip()) > 50]
    
    def process_text_files(self, file_paths: List[str]) -> List[str]:
        """處理文字檔案"""
        all_chunks = []
        
        for file_path in file_paths:
            try:
                print(f"📄 載入檔案: {file_path}")
                
                if file_path.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                else:
                    loader = TextLoader(file_path, encoding='utf-8')
                
                docs = loader.load()
                
                for doc in docs:
                    chunks = self.text_splitter.split_text(doc.page_content)
                    all_chunks.extend(chunks)
                
                print(f"  ✅ 已處理，獲得 {len(chunks)} 個文字塊")
                
            except Exception as e:
                print(f"  ❌ 處理失敗: {e}")
        
        return [chunk for chunk in all_chunks if len(chunk.strip()) > 50]


def create_vectorstore_from_urls(urls: List[str], save_path: str = "vectorstore.pkl"):
    """從 URL 建立向量庫"""
    processor = DocumentProcessor()
    vectorstore = SimpleVectorStore()
    
    # 處理網頁
    chunks = processor.process_web_urls(urls)
    
    if chunks:
        vectorstore.add_documents(chunks)
        vectorstore.save(save_path)
        return vectorstore
    else:
        print("❌ 沒有成功處理任何文檔")
        return None


# 簡單的命令列工具
if __name__ == "__main__":
    print("🛠️ 簡化向量資料庫工具")
    print("=" * 40)
    
    # 初始化
    processor = DocumentProcessor()
    vectorstore = SimpleVectorStore()
    
    while True:
        print("\n請選擇操作：")
        print("1. 載入網頁文檔")
        print("2. 載入本地檔案")
        print("3. 載入整個目錄")
        print("4. 測試搜尋")
        print("0. 退出")
        
        choice = input("\n請輸入選項: ").strip()
        
        if choice == "0":
            break
            
        elif choice == "1":
            url = input("請輸入網頁 URL: ").strip()
            if url:
                chunks = processor.process_web_urls([url])
                if chunks:
                    vectorstore.add_documents(chunks)
                    vectorstore.save("vectorstore.pkl")
                    print("✅ 向量庫建立完成！")
                    
        elif choice == "2":
            files = input("請輸入檔案路徑 (用逗號分隔): ").strip()
            if files:
                file_list = [f.strip() for f in files.split(",")]
                chunks = processor.process_text_files(file_list)
                if chunks:
                    vectorstore.add_documents(chunks)
                    vectorstore.save("vectorstore.pkl")
                    print("✅ 向量庫建立完成！")
                    
        elif choice == "3":
            directory = input("請輸入目錄路徑: ").strip()
            if os.path.exists(directory):
                from pathlib import Path
                file_paths = []
                for ext in ['.txt', '.md', '.pdf', '.docx']:
                    files = list(Path(directory).glob(f"**/*{ext}"))
                    file_paths.extend([str(f) for f in files])
                
                if file_paths:
                    print(f"找到 {len(file_paths)} 個檔案")
                    chunks = processor.process_text_files(file_paths)
                    if chunks:
                        vectorstore.add_documents(chunks)
                        vectorstore.save("vectorstore.pkl")
                        print("✅ 向量庫建立完成！")
                else:
                    print("❌ 目錄中沒有找到支援的檔案")
            else:
                print("❌ 目錄不存在")
                
        elif choice == "4":
            if vectorstore.load("vectorstore.pkl"):
                while True:
                    query = input("\n請輸入搜尋關鍵字 (或 'quit' 退出): ")
                    if query.lower() == 'quit':
                        break
                    
                    results = vectorstore.search(query, k=3)
                    print(f"\n🔍 搜尋結果 ({len(results)} 筆):")
                    for i, result in enumerate(results, 1):
                        print(f"{i}. [相似度: {result['score']:.3f}]")
                        print(f"   {result['content'][:150]}...\n")
            else:
                print("❌ 請先建立向量庫")
                
        else:
            print("❌ 無效選項")