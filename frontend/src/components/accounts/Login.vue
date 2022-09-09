<template>
  <v-card class="d-flex flex-column mx-auto my-6 flat" width="374" color="#fff">
    <v-img
      contain
      height="100"
      src="@/assets/logo-500px.png"
    ></v-img>
    <v-card-title class="d-flex justify-center pa-0 mt-6"
      >ログイン</v-card-title
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
                v-model.trim="$v.inputEmail.$model"
                :error-messages="errorMessagesEmail"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-text-field
                outlined
                dense
                label="パスワード"
                :type="show ? 'text' : 'password'"
                v-model="inputPassword"
                :error-messages="errorMessagesPassword"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show = !show"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12">
              <v-btn color="primary" block @click="submit">ログイン</v-btn>
            </v-col>
            <v-col
              cols="12">
              <v-divider class="mt-8"></v-divider>
              <v-btn class="mt-8" color="primary" block to="/password/reset">パスワードを忘れた</v-btn>
            </v-col>
            <v-col
              cols="12">
              <v-btn class="mt-2" color="primary" block to="/signup">新規会員登録</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'


export default {
  data() {
    return {
      inputEmail: null,
      inputPassword: null,
      valid: true,
      submitStatus: null,
      errorMessagesEmail: [],
      errorMessagesPassword: [],
      show:false,
    };
  },
  validations: {
    inputEmail: {
      required,
    },
    inputPassword: {
      required,
      minLength: minLength(8)
    }
  },
  methods: {
    submit() {
      this.$v.$touch()
      this.validateEmail()
      this.validatePassword()
      if (!this.$v.$invalid) {
        this.login() 
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
    login() {
      this.$store
        .dispatch("userLogin", {
          email: this.inputEmail,
          password: this.inputPassword,
        }).then(response => {
          if (this.$route.query.redirect) {
            this.$router.push(this.$route.query.redirect);
          }
          else {
            this.$router.push({ name: "vote" });
          }
        }).catch(error => {
          this.errorMessagesEmail.splice(0)
          this.errorMessagesEmail.push('メールアドレスまたはパスワードが間違っています。')
          this.errorMessagesPassword.splice(0)
          this.errorMessagesPassword.push('メールアドレスまたはパスワードが間違っています。')
        })
    }
  },
};
</script>