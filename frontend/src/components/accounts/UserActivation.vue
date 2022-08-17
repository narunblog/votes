<template>
  <v-container>
    <h1>UserActivation</h1>
  </v-container>
</template>


<script>
import axios from "axios";


export default {
  data() {
    return {};
  },
  methods: {
    activate() {
      const axiosBase = axios.create({
        baseURL: "http://127.0.0.1:8000",
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "json",
        timeout: 1000,
      });
      axiosBase.post("/api/accounts/users/activation/", {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      }).then(response => {
        console.log(response)
        console.log('アクティベーションに成功しました。')
        })
        .catch(response => {
          console.log(response)
          console.log('アクティベーションに失敗しました。時間を置いて再度アクセスしてください。')
        })
    },
  },
  created: function () {
    this.activate()
  },
};
</script>