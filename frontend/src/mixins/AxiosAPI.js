import store from "@/store"
import router from "@/router";
import axios from "axios";


const axiosAPI = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  responseType: "json",
  timeout: 10000,
});
// Add a request interceptor
axiosAPI.interceptors.request.use(function (config) {
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
axiosAPI.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.config && error.response && error.response.status === 401 && !isRetry) {
    isRetry = true
    return axiosAPI.post('/api/accounts/jwt/refresh/', {
      refresh: store.state.refreshToken
    }).then(response => {
      if (response.status === 200) {
        error.config.headers = {
          Authorization: store.state.accessToken
        } // ヘッダーに新しいトークンを追加
        store.dispatch('refresh', response.data.access) // トークンを更新
        console.log('retry request')
        return axiosAPI.request(error.config);
      }
    })
  } else {
    console.log('reject')
    return Promise.reject(error);
  }
})

export { axiosAPI };