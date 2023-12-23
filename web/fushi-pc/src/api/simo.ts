import http from ".";

/**
 * 获取灵感词汇
 * @param content 
 * @param num 
 * @returns 
 */
export const getWords = (content:string, num:number) => http.get("/simo/getWords/" + num + "/" + content)

/**
 * 获取灵感句子
 * @param content 
 * @param num 
 * @returns 
 */
export const getSentences = (content:string, num:number) => http.get("/simo/getSentences/" + num + "/" + content)

/**
 * 获取灵感诗词
 * @param content 
 * @param num 
 * @returns 
 */
export const getPoems = (content:string, num:number) => http.get("/simo/getPoems/" + num + "/" + content)
