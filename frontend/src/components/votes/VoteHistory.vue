<template>
  <div v-if="!loading">
    <div v-if="order_history.length">
      <v-row v-for="(order,index) in order_history" :key="index" justify="center">
        <v-col cols="8">
          <v-card
            outlined>
            <v-card-title>
              <v-row>
                <v-col class="d-flex align-center">
                  {{ order.vote.title }}<v-chip class="ma-2" :color="btnColor(order.vote.status)" text-color="white">{{ statusToString(order.vote.status) }}</v-chip>
                </v-col>
                <v-col class="d-flex align-center">
                  <v-btn :disabled="order.vote.status != 1" color="primary" right absolute to="vote/re-vote">注文内容変更</v-btn>
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-subtitle>
              注文日:{{ formatDate(new Date(order.order_datetime),'yyyy/MM/dd') }}
            </v-card-subtitle>
            <v-card-text>
              <v-row v-for="(orderItem,index) in order.order_items" :key=index no-gutters class="mb-2">
                <v-col cols="12">
                  <ItemCardForOrderHistory :orderItem="orderItem"></ItemCardForOrderHistory>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <div class="text-h4 d-flex justify-center">
        投票履歴はありません。
      </div>
    </div>
  </div>
</template>


<script>
import ItemCardForOrderHistory from '../cards/ItemCardForOrderHistory.vue'
import { axiosAPI } from '../../mixins/AxiosAPI'


export default {
  name: 'VoteHistory',
  components: {
    ItemCardForOrderHistory,
},
  data: () => ({
    loading : true,
    order_history: [],
    dialog: false,
    editOrderItems:[],
  }),
  computed:{
    statusToString(){
      return(status) => {
        if (status == 1) {
          return '開催中'
        } else if (status == 2) {
          return '終了'
        }
      }
    },
    btnColor() {
      return (status) => {
        if (status == 1) {
          return 'green'
        } else if (status == 2) {
          return undefined
        }
      }
    }
  },
  methods: {
    getOrderHistory() {
      const endopoint = '/api/votes/order/history/'
      axiosAPI.get(endopoint)
        .then(response => {
          this.order_history = [...response.data]
          this.loading = false
      })
    },
    formatDate (date, format) {
      format = format.replace(/yyyy/g, date.getFullYear());
      format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2));
      format = format.replace(/dd/g, ('0' + date.getDate()).slice(-2));
      format = format.replace(/HH/g, ('0' + date.getHours()).slice(-2));
      format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2));
      format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2));
      format = format.replace(/SSS/g, ('00' + date.getMilliseconds()).slice(-3));
      return format;
    },
    dialogOpen(orderItems) {
      this.editOrderItems = orderItems
      console.log(this.editOrderItems)
      this.dialog = true
    },
  },
  created() {
    this.getOrderHistory()
  },
}

</script>