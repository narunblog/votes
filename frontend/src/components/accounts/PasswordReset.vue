<template>
  <v-card class="d-flex flex-column mx-auto my-6 flat" width="374" color="#fff">
    <v-img
      contain
      height="100"
      src="@/assets/logo-500px.png"
    ></v-img>
    <v-card-title class="d-flex justify-center pa-0 mt-6"
      >パスワードリセット</v-card-title
    >
    <v-card-text class="d-flex justify-center flex-column">
      <v-form class="mx-9" ref="form" v-model="valid">
        <v-container fluid>
          <v-row no-gutters>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="メールアドレス"
                v-model.trim="inputEmail"
                :error-messages="errorMessagesEmail"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-btn color="primary" block @click="submit">リセットする</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import axios from "axios";


export default {
  data() {
    return {
      inputEmail: null,
      valid: true,
      errorMessagesEmail: [],
    };
  },
  validations: {
    inputEmail: {
      required,
    },
  },
  methods: {
    submit() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        this.validateEmail()
        console.log('error!')
      } else {
        this.resetPassword()
        console.log('submit!')
      }
    },
    validateEmail() {
      this.errorMessagesEmail = []
      if (!this.$v.inputEmail.required) {
        this.errorMessagesEmail.push('メールアドレスは必須です。')
      }
      const value = this.$v.inputEmail.$model
      if (!/.+@.+\..+/.test(value)) {
        this.errorMessagesEmail.push('メールアドレスの形式が違います。')
      }
    },
    resetPassword() {
      const axiosBase = axios.create({
        baseURL: "http://127.0.0.1:8000",
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "json",
        timeout: 1000,
      });
      axiosBase.post("/api/accounts/users/reset_password/", {
        email: this.inputEmail
      }).then(response => {
        console.log(response)
        console.log('success')
      }).catch(response => {
          console.log(response)
      })
    },
  },
};
</script>