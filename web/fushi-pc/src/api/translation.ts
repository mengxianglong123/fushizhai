import http from ".";

/**
 * 翻译接口
 * @param params 
 * @returns 
 */
export const translate = (params:any) => http.post('/translation/translate', params, {headers:{'Content-Type': 'application/x-www-form-urlencoded'}})