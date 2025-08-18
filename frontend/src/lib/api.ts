const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:5000';

// 通用 API 請求函式
async function apiRequest(endpoint: string) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API 請求錯誤:', error);
    throw error;
  }
}

// 具體的 API 函式
export const weatherAPI = {
  // 測試 API 連接
  test: () => apiRequest('/api/test'),
  
  // 取得歷史資料
  getHistoryData: (year: number, month: number, colId: number, rowId: number) =>
    apiRequest(`/data/${year}/${month}/${colId}+${rowId}`),
  
  // 取得 NDVI 資料
  getNDVIData: (month: number, vegetation: number, colId: number, rowId: number) =>
    apiRequest(`/NDVI/${month}/${vegetation}/${colId}+${rowId}`),
};
