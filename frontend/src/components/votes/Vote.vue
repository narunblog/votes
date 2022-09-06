<template>
  <div>
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
      <div class="d-flex justify-center">
        <v-btn v-if="!hasVote" color="primary" to="/vote/new-vote">投票する</v-btn>
        <v-btn v-else color="primary" to="/vote/re-vote">選び直す</v-btn>
      </div>
    </div>
    <div v-else-if="vote.status==2">
      <v-sheet
        color="grey lighten-4">
          <div
            class="text-h4 d-flex justify-center">
            開催中の投票はありません。
          </div>
          <div
            class="text-caption d-flex justify-center">
            次回開催をお待ちください。
          </div>
      </v-sheet>
    </div>
  </div>
</template>


<script>
import { axiosAPI } from '@/mixins/AxiosAPI';
import Timer from '../timer/Timer.vue'


export default {
  name: 'Vote',
  components: {
    Timer,
  },
  data: () => ({
    vote:{},
    hasVote: false,
    currentVote:{},
  }),
  methods: {
    getCurrentVote() {
      const endpoint = "/api/votes/vote/current/"
      axiosAPI.get(endpoint)
        .then(response => {
          this.vote = Object.assign({}, response.data)
      })
    },
    getCurrentVoteOrderData() {
      const endpoint = 'api/votes/order/current/'
      axiosAPI.get(endpoint)
        .then(response => {
          this.hasVote = this.toBoolean(response.data)
      })
    },
    toBoolean (data) {
      return data.toLowerCase() === 'true';
    },
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
  created() {
    this.getCurrentVote()
    this.getCurrentVoteOrderData()
  },
}

</script>