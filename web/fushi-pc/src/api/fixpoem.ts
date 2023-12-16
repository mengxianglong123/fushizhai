import http from ".";

/**
 * 格律校验
 * @param params 
 * @returns 
 */
export const checkRhyme = (params:any) => http.post('/creation/checkPoemRhyme', params, {headers:{'Content-Type': 'application/x-www-form-urlencoded'}})