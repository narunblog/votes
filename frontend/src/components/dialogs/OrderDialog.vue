<template>
	<v-dialog
		v-model="dialog"
		persistent
		width="50%">
		<v-card>
			<v-card-title>オーダーアイテム</v-card-title>
			<v-card-text v-for="(item,index) in items" :key="index">
				<ItemCard :src="item.item.image" :title="item.item.name" :size="item.size" :quantity.sync="item.quantity"></ItemCard>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn
					depressed
					@click="$emit('onClickClose')">
					キャンセル
				</v-btn>
				<v-btn
          depressed
					color="primary"
					@click="$emit('onClickSave',formData)">
          変更する
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
  data: () => ({}),
  computed: {},
  methods: {},
  props: {
    dialog: false,
    items: {
      type: Array,
      required: true,
    },
  },
}
</script>