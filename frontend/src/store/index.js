import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import { axiosBase } from "@/mixins/AxiosBase"


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
  },
  getters: {},
  mutations: {
    updateLoginToken(state, { access, refresh }) {
      state.accessToken = `JWT ${access}`
      state.refreshToken = refresh
      state.isAuthenticated = true
    },
    refreshAccessToken(state, { access }) {
      state.accessToken = `JWT ${access}`
    },
    removeLoginToken(state,) {
      state.accessToken = null
      state.refreshToken = null
      state.isAuthenticated = false
    },
  },
  actions: {
    userLogin(context, usercredentials) {
      return new Promise((resolve, reject) => {
        const endpoint = '/api/accounts/jwt/create/'
        axiosBase.post(endpoint, {
          email: usercredentials.email,
          password: usercredentials.password,
        })
          .then(response => {
            context.commit('updateLoginToken', { access: response.data.access, refresh: response.data.refresh })
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    },
  },
  modules: {},
  plugins: [createPersistedState({
    key: 'Votes',
    paths: ['accessToken', 'refreshToken', 'isAuthenticated'],
    storage: window.localStorage,
  })],
});
