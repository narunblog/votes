<template>
  <div>
    <v-alert
      v-for="(alertMessage,index) in alertMessages"
      :key="index"
      outlined
      type="error"
      prominent
      dense
      dismissible
      v-model="alert">
    {{ alertMessage }}
    </v-alert>
    <div v-if="vote.status==0">
      <v-sheet
        color="grey lighten-4">
          <div
            class="text-h4 d-flex justify-center">
            予約されている投票があります
          </div>
          <div
            class="text-caption d-flex justify-center">
            ※開始日{{formatDateComputed(new Date(vote.start_datetime),'yyyy年MM月dd日HH時mm分ss秒')}}まで残り
          </div>
      </v-sheet>
      <Timer :deadline="formatDateComputed(new Date(vote.start_datetime),'yyyy-MM-dd HH\:mm\:ss:')"></Timer>
    </div>
    <div v-else-if="vote.status==1">
      <v-sheet
        color="grey lighten-4">
          <div
            class="text-h4 d-flex justify-center">
            投票が開催されています
          </div>
          <div
            class="text-caption d-flex justify-center">
            ※終了日{{formatDateComputed(new Date(vote.end_datetime),'yyyy年MM月dd日HH時mm分ss秒')}}まで残り
          </div>
      </v-sheet>
      <Timer  :deadline="formatDateComputed(new Date(vote.end_datetime),'yyyy-MM-dd HH\:mm\:ss:')"></Timer>
    </div>
    <div v-else-if="vote.status==2">
      <v-sheet
        color="grey lighten-4">
          <div
            class="text-h4 d-flex justify-center">
            投票を新たに開始することができます
          </div>
          <div
            class="text-caption d-flex justify-center">
            ※投票を開始するには作成ボタンをクリックしてください。
          </div>
      </v-sheet>
      <div class="d-flex justify-center mt-4">
        <v-btn
          large
          color="primary"
          @click.stop="dialog=true">
          <v-icon>mdi-plus</v-icon>作成
        </v-btn>
      </div>
    </div>
    <v-row>
      
    </v-row>
    <VoteStartDialog
      ref="voteStartDialog"
      :dialog="dialog"
      @onClickClose="dialog=false"
      @onClickSave="formAction">
    </VoteStartDialog>
  </div>
</template>


<script>
import { axiosAPI } from '@/mixins/AxiosAPI';
import VoteStartDialog from '../dialogs/VoteStartDialog.vue'
import Timer from '../timer/Timer.vue'


export default {
  name: 'VoteStart',
  components: {
    VoteStartDialog,
    Timer,
  },
  data() {
    return {
      dialog: false,
      vote: {},
      alert: false,
      alertMessages:[],
    }
  },
  computed:{
    formatDateComputed() {
      return (date, format) => {
        format = format.replace(/yyyy/g, date.getFullYear());
        format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2));
        format = format.replace(/dd/g, ('0' + date.getDate()).slice(-2));
        format = format.replace(/HH/g, ('0' + date.getHours()).slice(-2));
        format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2));
        format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2));
        format = format.replace(/SSS/g, ('00' + date.getMilliseconds()).slice(-3));
        return format;
      }
    },
  },
  methods: {
    formAction(formData) {
      this.dialog = false
      this.createVote(formData)
    },
    createVote(formData) {
      const endpoint = "/api/votes/create/"
      const postData = {
        title: formData["title"],
        start_datetime: `${formData["startDate"]}T${formData["startTime"]}`,
        end_datetime: `${formData["endDate"]}T${formData["endTime"]}`,
      }
      axiosAPI.post(endpoint, postData)
        .then(response => {
          this.getCurrentVote()
          this.$refs.voteStartDialog.formDataInit()
        })
        .catch(error => {
          this.alertMessages.splice(0)
            for (let [key, value] of Object.entries(error.response.data)) {
              this.alertMessages.push(...value)
            }
          this.alertMessages.push("3秒後に画面を更新します。")
          this.alert = true
          //画面更新処理
          setTimeout(this.reloadPage, 3*1000);
        })
    },
    reloadPage() {
      this.$router.go({path: this.$router.currentRoute.path, force: true})
    },
    getCurrentVote() {
      const endpoint = "/api/votes/vote/current/"
      axiosAPI.get(endpoint)
        .then(response => {
          this.vote = Object.assign({}, response.data)
      })
    },
  },
  created() {
    this.getCurrentVote()
  }
};
</script>