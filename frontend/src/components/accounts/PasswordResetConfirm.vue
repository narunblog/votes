<template>
  <v-card class="d-flex flex-column mx-auto my-6 flat" width="374" color="#fff">
    <v-img
      contain
      height="100"
      src="@/assets/logo-500px.png"
    ></v-img>
    <v-card-title class="d-flex justify-center pa-0 mt-6"
      >パスワード変更</v-card-title
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
                label="パスワード"
                v-model.trim="inputPassword"
                :error-messages="errorMessagesPassword"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード（確認）"
                v-model="inputRePassword"
                :error-messages="errorMessagesRePassword"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-btn color="primary" block @click="submit">変更する</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'
import axios from "axios";


export default {
  data() {
    return {
      inputPassword: null,
      inputRePassword: null,
      valid: true,
      errorMessagesPassword: [],
      errorMessagesRePassword:[],
    };
  },
  validations: {
    inputPassword: {
      required,
      minLength: minLength(8)
    },
    inputRePassword: {
      required,
      minLength: minLength(8)
    }
  },
  methods: {
    submit() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        this.validatePassword()
        this.validateRePassword()
        console.log('error!')
      } else {
        this.changePassword()
        console.log('submit!')
      }
    },
    validatePassword() {
      this.errorMessagesPassword = []
      if (!this.$v.inputPassword.required) {
        this.errorMessagesPassword.push('パスワードは必須です。')
      }
      if (!this.$v.inputPassword.minLength) {
        this.errorMessagesPassword.push('8文字以上入力してください。')
      }
    },
    validateRePassword() {
      this.errorMessagesRePassword = []
      if (!this.$v.inputRePassword.required) {
        this.errorMessagesRePassword.push('パスワード（確認）は必須です。')
      }
      if (!this.$v.inputRePassword.minLength) {
        this.errorMessagesRePassword.push('8文字以上入力してください。')
      }
    },
    changePassword() {
      const axiosBase = axios.create({
        baseURL: "http://127.0.0.1:8000",
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "json",
        timeout: 1000,
      });
      axiosBase.post("/api/accounts/users/reset_password_confirm/", {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.inputPassword,
        re_new_password: this.inputRePassword,
      }).then(response => {
        console.log(response)
        this.$router.push({ name: "passwordResetDone" });
        })
        .catch(response => {
          console.log(response)
        })
    },
  },
};
</script>