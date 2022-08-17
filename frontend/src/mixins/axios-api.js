import axios from "axios";
import store from "@/store"
import router from "@/router";


const axiosApi = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  responseType: "json",
  timeout: 1000,
});

// Add a request interceptor
axiosApi.interceptors.request.use(function (config) {
  // Do something before request is sent
  if (store.state.accessToken) {
    config.headers = { Authorization: store.state.accessToken } // todo: ここでトークンを付与する
  } else {
    router.push({ name: "login" });
  }
  return config
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

let isRetry = false
axiosApi.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.config && error.response && error.response.status === 401 && !isRetry) {
    isRetry = true
    return axiosApi.post('/api/accounts/jwt/refresh/', {
      refresh: store.state.refreshToken
    }).then(response => {
      if (response.status === 200) {
        error.config.headers = {
          Authorization: store.state.accessToken
        } // ヘッダーに新しいトークンを追加
        store.dispatch('refresh', response.data.access) // トークンを更新
        console.log('retry request')
        return axiosApi.request(error.config);
      }
    })
  } else {
    console.log('reject')
    return Promise.reject(error);
  }
})

export { axiosApi };