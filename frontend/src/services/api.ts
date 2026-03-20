import axios, { AxiosInstance } from "axios";

const api: AxiosInstance = axios.create({
  baseURL: "/api",
  timeout: 10000,
}) as AxiosInstance;

export default api;

