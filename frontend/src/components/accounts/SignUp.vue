<template>
  <v-card class="d-flex flex-column mx-auto my-6 flat" width="374" color="#fff">
    <v-img
      contain
      height="100"
      src="@/assets/logo-500px.png"
    ></v-img>
    <v-card-title class="d-flex justify-center pa-0 mt-6"
      >会員登録</v-card-title
    >
    <v-card-text class="d-flex justify-center flex-column">
      <v-form class="mx-9" ref="form" v-model="valid">
        <v-container fluid>
          <v-row no-gutters>
            <v-col
              cols="12"
              md="6">
              <v-text-field
                outlined
                dense
                label="性"
                v-model="inputFirstName"
                :error-messages="errorMessagesFirstName">
              </v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="6">
              <v-text-field
                outlined
                dense
                label="名"
                v-model="inputLastName"
                :error-messages="errorMessagesLastName">
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="社員番号"
                v-model="inputUserNumber"
                :error-messages="errorMessagesUserNumber">
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="メールアドレス"
                v-model="inputEmail"
                :error-messages="errorMessagesEmail">
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード"
                v-model="inputPassword"
                :error-messages="errorMessagesPassword">
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード（確認）"
                v-model="inputRePassword"
                :error-messages="errorMessagesRePassword">
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-btn color="primary" block @click="submit">アカウントを作成する</v-btn>
            </v-col>
            <v-col
              cols="12">
              <v-divider class="mt-8"></v-divider>
              <v-btn class="mt-8" color="primary" block to="/login">ログインする</v-btn>
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
      inputFirstName: null,
      inputLastName: null,
      inputUserNumber: null,
      inputEmail: null,
      inputPassword: null,
      inputRePassword: null,
      valid: true,
      errorMessagesFirstName: [],
      errorMessagesLastName: [],
      errorMessagesUserNumber: [],
      errorMessagesEmail: [],
      errorMessagesPassword: [],
      errorMessagesRePassword:[],
    };
  },
  validations: {
    inputFirstName: {
      required,
    },
    inputLastName: {
      required,
    },
    inputUserNumber: {
      required,
    },
    inputEmail: {
      required,
    },
    inputPassword: {
      required,
      minLength: minLength(8)
    },
    inputRePassword: {
      required,
      minLength: minLength(8)
    },
  },
  methods: {
    submit() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        this.validateFirstName()
        this.validateLastName()
        this.validateUserNumber()
        this.validateEmail()
        this.validatePassword()
        this.validateRePassword()
      } else {
        this.signup()
      }
    },
    validateFirstName() {
      this.errorMessagesFirstName = []
      if (!this.$v.inputFirstName.required) {
        this.errorMessagesFirstName.push('性は必須です。')
      }
    },
    validateLastName() {
      this.errorMessagesLastName = []
      if (!this.$v.inputLastName.required) {
        this.errorMessagesLastName.push('名は必須です。')
      }
    },
    validateUserNumber() {
      this.errorMessagesUserNumber = []
      if (!this.$v.inputUserNumber.required) {
        this.errorMessagesUserNumber.push('社員番号は必須です。')
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
      const isMatch = this.inputPassword == this.inputRePassword
      if (!isMatch) {
        this.errorMessagesRePassword.push('パスワードが一致しません。')
      }
    },
    signup() {
      const axiosBase = axios.create({
        baseURL: "http://127.0.0.1:8000",
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "json",
        timeout: 1000,
      });
      axiosBase.post("/api/accounts/users/", {
        first_name: this.inputFirstName,
        last_name: this.inputLastName,
        user_number: this.inputUserNumber,
        email: this.inputEmail,
        password: this.inputPassword,
        re_password:this.inputRePassword,
      }).then(response => {
        console.log(response)
        this.$router.push({ name: "signUpDone" });
        })
        .catch(response => {
          console.log(response)
        })
    },
  },
};
</script>