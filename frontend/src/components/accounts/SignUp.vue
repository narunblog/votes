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
                :type="show1 ? 'text' : 'password'"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :error-messages="errorMessagesPassword">
                <template v-slot:append>
                  <button @click="show1 = !show1" tabindex="-1">
                    <v-icon v-if="show1" >mdi-eye</v-icon>
                    <v-icon v-else >mdi-eye-off</v-icon>
                  </button>
                </template>
              </v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード（確認）"
                v-model="inputRePassword"
                :type="show2 ? 'text' : 'password'"
                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show2 = !show2"
                :error-messages="errorMessagesRePassword">
                <template v-slot:append>
                  <button @click="show2 = !show2" tabindex="-1">
                    <v-icon v-if="show2" >mdi-eye</v-icon>
                    <v-icon v-else >mdi-eye-off</v-icon>
                  </button>
                </template>
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
import { axiosBase } from '@/mixins/AxiosBase';


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
      errorMessagesRePassword: [],
      show1: false,
      show2:false,
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
      this.validateFirstName()
      this.validateLastName()
      this.validateUserNumber()
      this.validateEmail()
      this.validatePassword()
      this.validateRePassword()
      if (!this.$v.$invalid) {
        this.signup() 
      }
    },
    validateFirstName() {
      this.errorMessagesFirstName.splice(0)
      if (!this.$v.inputFirstName.required) {
        this.errorMessagesFirstName.push('性は必須です。')
      }
    },
    validateLastName() {
      this.errorMessagesLastName.splice(0)
      if (!this.$v.inputLastName.required) {
        this.errorMessagesLastName.push('名は必須です。')
      }
    },
    validateUserNumber() {
      this.errorMessagesUserNumber.splice(0)
      if (!this.$v.inputUserNumber.required) {
        this.errorMessagesUserNumber.push('社員番号は必須です。')
      }
    },
    validateEmail() {
      this.errorMessagesEmail.splice(0)
      if (!this.$v.inputEmail.required) {
        this.errorMessagesEmail.push('メールアドレスは必須です。')
      }
      const value = this.$v.inputEmail.$model
      if (!/.+@.+\..+/.test(value)) {
        this.errorMessagesEmail.push('メールアドレスの形式が違います。')
      }
    },
    validatePassword() {
      this.errorMessagesPassword.splice(0)
      if (!this.$v.inputPassword.required) {
        this.errorMessagesPassword.push('パスワードは必須です。')
      }
      if (!this.$v.inputPassword.minLength) {
        this.errorMessagesPassword.push('8文字以上入力してください。')
      }
    },
    validateRePassword() {
      this.errorMessagesRePassword.splice(0)
      if (!this.$v.inputRePassword.required) {
        this.errorMessagesRePassword.push('パスワード（確認）は必須です。')
      }
      const isMatch = this.inputPassword == this.inputRePassword
      if (!isMatch) {
        this.errorMessagesRePassword.push('パスワードが一致しません。')
      }
    },
    signup() {
      axiosBase.post("/api/accounts/users/", {
        first_name: this.inputFirstName,
        last_name: this.inputLastName,
        user_number: this.inputUserNumber,
        email: this.inputEmail,
        password: this.inputPassword,
        re_password:this.inputRePassword,
      }).then(response => {
        this.$router.push({ name: "signUpDone" });
        })
        .catch(error => {
          console.log(error.response)
          const data = error.response.data
          if (data.email) {
            this.errorMessagesEmail.splice(0)
            this.errorMessagesEmail.push(...data.email)
          }
          if (data.first_name) {
            this.errorMessagesFirstName.splice(0)
            this.errorMessagesFirstName.push(data.first_name)
          }
          if (data.last_name) {
            this.errorMessagesLastName.splice(0)
            this.errorMessagesLastName.push(data.last_name)
          }
          if (data.user_number) {
            this.errorMessagesUserNumber.splice(0)
            this.errorMessagesUserNumber.push(data.user_number)
          }
          if (data.password) {
            this.errorMessagesPassword.splice(0)
            this.errorMessagesPassword.push(data.password)
          }
          if (data.re_password) {
            this.errorMessagesRePassword.splice(0)
            this.errorMessagesRePassword.push(data.re_password)
          }
        })
    },
  },
};
</script>