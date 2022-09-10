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
    <v-card>
      <v-card-title>
        <v-col cols="12">
          <span v-if="isNewVote">新規投稿</span>
          <span v-else>投稿編集</span>
          :{{ vote.title }}
        </v-col>
				<!-- 検索フォーム -->
        <v-col cols="8">
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="検索"
            single-line
            hide-details
          />
        </v-col>
        <v-spacer/>
        <!-- カートボタン -->
        <v-col class="text-right" cols="4">
          <v-badge
            color="green"
            :content="cartItems.length"
            :value="cartItems.length"
            overlap>
            <v-btn color="primary" v-on:click.stop="cartDialogOpen">
              <v-icon>mdi-cart</v-icon>
            </v-btn>
          </v-badge>
          <CartDialog ref="cartDialog" :dialog="dialog" :cartItems="cartItems" @onClickClose="dialog=false" @onClickSave="formAction" @changeCartItem="changeCartItem" @deleteCartItem="deleteCartItem"></CartDialog>
        </v-col>
      </v-card-title>
      <!-- テーブル -->
      <v-data-table
        class="text-no-wrap"
        :headers="tableHeaders"
        :items="tableData"
        :search="search"
        :loading="loading"
        sort-by="id"
        :items-per-page="-1"
        :mobile-breakpoint="0"
      >
        <template v-slot:item.image="{ item }">
          <v-img
            :src="item.image"
            max-height="100px"
            min-height="100px"
            max-width="100px"
            min-width="100px">
          </v-img>
        </template>
        <template v-slot:item.size="{ item }">
          <SelectInput :items="item.size.choice" value="--" :id="item.id" type="size" itemText="text" itemValue="value" @changeValue="changeValue"></SelectInput>
        </template>
        <template v-slot:item.quantity="{ item }">
          <SelectInput :items="item.quantity.choice" value="--" :id="item.id" type="quantity" itemText="text" itemValue="value" @changeValue="changeValue"></SelectInput>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn color="primary" @click="addCart(item)">カートに追加</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>


<script>
import SelectInput from '../selects/SelectInput.vue'
import QuantitySelectInput from '../selects/QuantitySelectInput.vue'
import CartDialog from '../dialogs/CartDialog.vue'
import { axiosAPI } from '@/mixins/AxiosAPI';


export default {
  name: 'Home',
  components: {
    SelectInput,
    QuantitySelectInput,
    CartDialog,
},
  props: {
    tableData: {
      type: Array,
      required: true,
    },
    tableHeaders: {
      type: Array,
      required: true,
    },
    vote: {
      type:Object,
      required: true,
    },
    isNewVote: {
      type: Boolean,
      required: true,
    },
  },
  data () {
    const today = new Date()
    const year = today.getFullYear()
    const month = ('0' + (today.getMonth() + 1)).slice(-2)

    return {
      /** ローディング状態 */
      loading: false,
      /** 月選択メニューの状態 */
      menu: false,
      /** 検索文字 */
      search: '',
      /** 選択年月 */
      yearMonth: `${year}-${month}`,

      dialog: false,
      cartItems: [],
      alert: false,
      alertMessages: [],
    }
  },
  methods: {
    formAction() {
      if (this.isNewVote == true) {
        let endpoint = '/api/votes/item/cart/checkout/'
        const params = {
          vote: this.vote.id
        }
        axiosAPI.get(endpoint, { params: params })
          .then(response => {
            this.getItem()
          })
          .catch(error => {
            this.alertMessages.splice(0)
            for (let [key, value] of Object.entries(error.response.data)) {
              this.alertMessages.push(...value)
            }
            this.alert = true
          })
          .finally(() => {
            this.dialog = false
          })
      } else {
        let endpoint = '/api/votes/item/cart/checkout/'
        const modify = {
          putItems: this.cartItems,
          vote:this.vote.id,
        }
        axiosAPI.put(endpoint, modify)
          .then(response => {
            console.log(response)
            this.cartItems.splice(0)
          })
        this.dialog = false
      }
    },
    cartDialogOpen() {
      this.dialog = true
    },
    getItem() {
      if (this.isNewVote == true) {
        let endpoint = '/api/votes/item/cart/all/'
        axiosAPI.get(endpoint)
          .then(response => {
            //配列を初期化する
            this.cartItems.splice(0)
            this.cartItems.push(...response.data)
            console.log(this.cartItems)
          })
      } else {
        let endpoint = '/api/votes/order/'
        const params = {
          vote:this.vote.id
        }
        axiosAPI.get(endpoint,{params:params})
          .then(response => {
            this.cartItems.splice(0)
            this.cartItems.push(...response.data)
            console.log(this.cartItems)
          })
        
      }
    },
    addCart(item) {
      if (this.isNewVote == true) {
        this.alertMessages.splice(0)
        if (item.size.value == "--") {
          this.alertMessages.push("サイズを選択してください")
        }
        if (item.quantity.value == "--") {
          this.alertMessages.push("数量を選択してください")
        }
        if (this.alertMessages.length) {
          this.alert = true
          return 
        }
          let endpoint = 'api/votes/item/cart/'
          let data = {
            item: item.id,
            size: item.size.value,
            quantity: item.quantity.value,
          }
          axiosAPI.post(endpoint, data)
            .then(response => {
              console.log(response)
              this.getItem()
            })
            .catch(error => {
              this.alertMessages.splice(0)
              for (let [key, value] of Object.entries(error.response.data)) {
                this.alertMessages.push(...value)
              }
              this.alert = true
            })
      } else {
        console.log(this.cartItems)
        this.cartItems.push({item:{image:item.image,name:item.name,id:item.id},quantity:item.quantity.value,size:item.size.value})
      }
    },
    changeValue(data) {
      this.$emit('changeValue',data)
    },
    changeCartItem(data) {
      if (this.isNewVote == true) {
        let endpoint = 'api/votes/item/cart/'
        let payload = {
          item: data.id,
          size: data.size,
          quantity: data.value,
        }
        axiosAPI.post(endpoint, payload).then(response => {
          this.getItem()
        })
      } else {
        const index = this.cartItems.findIndex(v => v.item.id == data.id && v.size == data.size)
        console.log(data)
        console.log(index)
        this.$set(this.cartItems[index],'quantity',data.value)
      }
    },
    deleteCartItem(item) {
      if (this.isNewVote == true) {
        let endpoint = 'api/votes/item/cart/'
        let payload = {
          item: item.item.id,
          size: item.size,
          quantity: item.quantity,
        }
        axiosAPI.delete(endpoint, { data: payload }).then(response => {
          this.getItem()
        })
      } else {
        const index = this.cartItems.findIndex(v => v.item.name == item.item.name && v.size == item.size)
        console.log(item)
        console.log(index)
        this.cartItems.splice(index,1)
      }
    },
  },
  created() {
    this.getItem()
  },
}
</script>