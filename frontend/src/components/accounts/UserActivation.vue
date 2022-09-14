<template>
  <v-container>
    <div v-if="!processing">
      <div v-if="isActivate">
        <h1>アクティベーションに成功しました。</h1>
        <p>ログイン画面に移動して、ログインを行なってください。</p>
        <router-link to="/login">ログイン画面へ</router-link>
      </div>
      <div v-else>
        <h1>アクティベーションに失敗しました。時間を置いて再度アクセスしてください。</h1>
      </div>
    </div>
  </v-container>
</template>


<script>
import { axiosBase } from '@/mixins/AxiosBase';


export default {
  data() {
    return {
      isActivate: false,
      processing:true,
    };
  },
  methods: {
    activate() {
      return axiosBase.post("/api/accounts/users/activation/", {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      }).then(response => {
        this.isActivate = true
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => {
          this.processing = false
        })
    },
  },
  created() {
    this.activate()
  },
};
</script>