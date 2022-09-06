<template>
  <div>
    <Table v-if="currentVote" :tableData="tableItems" :tableHeaders="tableHeaders" :vote="currentVote" :isNewVote="isNewVote" @changeValue="changeValue"></Table>
  </div>
</template>


<script>
import Table from '../tables/Table.vue'
import { axiosAPI } from '@/mixins/AxiosAPI';


  export default {
  name: 'NewVote',
  components: {
    Table,
  },
  data () {
    return {
      tableItems: [],
      tableHeaders: [
        { text: 'ID', value: 'id' , width: '1%'},
        { text: '商品名', value: 'name', align: 'start' , width: '29%'},
        { text: 'イメージ', value: 'image', sortable: false , width: '20%'},
        { text: 'サイズ', value: 'size', sortable: false , width: '15%'},
        { text: '数量', value: 'quantity', sortable: false ,width: '15%' },
        { text: '操作', value: 'actions' , sortable: false ,width: '20%'},
      ],
      currentVote: null,
      isNewVote: false,
    }
  },
  methods: {
    getItem() {
      const endpoint = '/api/votes/item/'
      axiosAPI.get(endpoint)
        .then(response => {
          //javascriptのオブジェクトは参照渡しのためスプレッド構文にしてから再度配列とする
          this.tableItems = [...response.data]
          this.tableItems.forEach((obj, index) => {
            this.$set(obj, "size", {value:'--',choice:['--',...obj['size']]})
            this.$set(obj, "quantity", { value:'--',choice:['--',1,2]})
          })
        })
        .catch(response => {
          console.log('error')
          console.log(response)
        })
    },
    getCurrentVote() {
      const endpoint = '/api/votes/vote/current/'
      axiosAPI.get(endpoint)
        .then(response => {
          this.currentVote = Object.assign({}, this.currentVote, { ...response.data })
      })
    },
    changeValue(data) {
      let item = this.tableItems.find(v => v.id == data.id)
      if (data.type == 'quantity') {
        this.$set(item.quantity, "value", data.value);
      } else {
        this.$set(item.size,"value",data.value)
      }
    },
  },
  created() {
    this.getItem()
    this.getCurrentVote()
  },
  }
</script>