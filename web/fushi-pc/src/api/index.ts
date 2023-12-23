// 封装axios
// 实例化  请求拦截器  响应拦截器
import axios from 'axios'
import { baseURL } from '@/config/common';

const http = axios.create({
  baseURL: baseURL,
  timeout: 10000
})

// 响应拦截
http.interceptors.response.use(res=>{
    return res.data; //直接将数据返回
}, err=>{
    return Promise.reject(err)
});

export default http