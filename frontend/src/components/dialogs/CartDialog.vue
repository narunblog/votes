<template>
	<v-dialog
		v-model="dialog"
		persistent
		width="50%">
		<v-card>
			<v-card-title>ショッピングカート</v-card-title>
			<v-card-text v-for="(cartItem,index) in cartItems" :key="index">
				<ItemCard :item="cartItem" @changeCartItem="changeCartItem" @deleteCartItem="deleteCartItem"></ItemCard>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn
					depressed
					@click="$emit('onClickClose')">
					追加する
				</v-btn>
				<v-btn
          depressed
					color="primary"
					@click="$emit('onClickSave')">
					注文する
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>


<script>
import ItemCard from '../cards/ItemCard.vue'


export default {
  name: 'CartDialog',
  components: {
      ItemCard
  },
  data: () => {
    return {

    }
  },
  computed: {},
  methods: {
    changeCartItem(data) {
      this.$emit('changeCartItem',data)
    },
    deleteCartItem(item) {
      this.$emit('deleteCartItem',item)
    }
  },
  props: {
    dialog: false,
    cartItems: {
      type: Array,
      required: true,
    },
  },
}
</script>