import http from ".";

/**
 * 根据类型获取
 * @param typeId 
 * @returns 
 */
export const getRhymeRulesByType = (typeId: string) => http.get("/creation/getRhymeRulesByType/" + typeId)

/**
 * 获取韵书名称列表
 * @returns 
 */
export const getRhymeBookNames = () => http.get("/creation/getRhymeBookNames")

/**
 * 获取规则的可以押的韵脚
 * @param params 
 * @returns 
 */
export const getPoemCanRhyme = (params:any) => http.get("/creation/getPoemCanRhyme", {params})

/**
 * 创作诗词
 * @param params 
 * @returns 
 */
export const createRhymePoem = (params:any) => http.post('/creation/createRhymePoem', params, {headers:{'Content-Type': 'application/x-www-form-urlencoded'}})