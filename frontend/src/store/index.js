import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import { axiosBase } from "@/mixins/AxiosBase"
import { axiosAPI } from "@/mixins/AxiosAPI";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    isStaff: null,
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
    updateIsStaff(state, { isStaff }) {
      state.isStaff = isStaff
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
            context.dispatch('isStaff')
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    isStaff(context) {
      return new Promise((resolve, reject) => {
        const endpoint = '/api/votes/user/my/'
        axiosAPI.get(endpoint)
          .then(response => {
            context.commit('updateIsStaff', { isStaff: response.data.is_staff })
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
    paths: ['accessToken', 'refreshToken', 'isAuthenticated', 'isStaff'],
    storage: window.localStorage,
  })],
});
