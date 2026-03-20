import axios, { AxiosInstance } from "axios";

const api: AxiosInstance = axios.create({
  baseURL: "/api",
  timeout: 35000,
}) as AxiosInstance;

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API请求错误:", error);
    if (error.response) {
      console.error("响应状态码:", error.response.status);
      console.error("响应数据:", error.response.data);
    } else if (error.request) {
      console.error("请求已发送但无响应:", error.request);
    } else {
      console.error("请求配置错误:", error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

