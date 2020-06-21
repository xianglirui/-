import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:8585',
  timeout: 5000
})

export function get_data(content) {
  return service({
    url: '/get_data',
    method: 'post',
    data:content
  });
}

export function get_label() {
  return service({
    url: '/get_label',
    method: 'get'
  });
}
