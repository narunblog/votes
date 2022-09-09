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
                :type="show1 ? 'text' : 'password'"
                v-model.trim="inputPassword"
                :error-messages="errorMessagesPassword"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show1 = !show1"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード（確認）"
                :type="show2 ? 'text' : 'password'"
                v-model="inputRePassword"
                :error-messages="errorMessagesRePassword"
                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show2 = !show2"
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
import { required, minLength,sameAs } from 'vuelidate/lib/validators'
import { axiosBase } from '@/mixins/AxiosBase';


export default {
  data() {
    return {
      inputPassword: null,
      inputRePassword: null,
      valid: true,
      errorMessagesPassword: [],
      errorMessagesRePassword: [],
      show1: false,
      show2:false,
    };
  },
  validations: {
    inputPassword: {
      required,
      minLength: minLength(8)
    },
    inputRePassword: {
      required,
      minLength: minLength(8),
      sameAsPassword:sameAs(function() {
            return this.inputPassword
          }) ,
    }
  },
  methods: {
    submit() {
      this.$v.$touch()
      this.validatePassword()
      this.validateRePassword()
      if (!this.$v.$invalid) {
        this.changePassword()
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
      if (!this.$v.inputRePassword.minLength) {
        this.errorMessagesRePassword.push('8文字以上入力してください。')
      }
      if (!this.$v.inputRePassword.sameAsPassword) {
        this.errorMessagesRePassword.push('パスワードとパスワード（確認）が一致しません。')
      }
    },
    changePassword() {
      const endpoint = '/api/accounts/users/reset_password_confirm/'
      axiosBase.post(endpoint, {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.inputPassword,
        re_new_password: this.inputRePassword,
      }).then(response => {
        console.log(response)
        this.$router.push({ name: "passwordResetConfirmDone" });
        })
        .catch(response => {
          console.log(response)
        })
    },
  },
};
</script>