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