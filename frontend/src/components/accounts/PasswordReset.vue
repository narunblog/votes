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
import { axiosBase } from '@/mixins/AxiosBase';


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
      this.validateEmail()
      if (!this.$v.$invalid) {
        this.resetPassword()
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
    resetPassword() {
      const endpoint = "/api/accounts/users/reset_password/"
      axiosBase.post(endpoint, {
        email: this.inputEmail
      }).then(response => {
        this.$router.push({ name: "passwordResetDone" });
      }).catch(error => {
        this.errorMessagesEmail.splice(0)
        this.errorMessagesEmail.push('このメールアドレスは登録されていません。')
      })
    },
  },
};
</script>