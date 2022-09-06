<template>
  <v-card
		outlined>
		<v-row>
			<v-col cols="4" class="d-flex align-center">
				<v-img :src="item.item.image"
					max-height="125"
          contain></v-img>
			</v-col>
			<v-col cols="8">
				<v-row>
					<v-col>
						<v-card-title>{{ item.item.name }}</v-card-title>
					</v-col>
				</v-row>
				<v-row>
					<v-col>
						<v-card-text>サイズ:{{ item.size }}</v-card-text>
					</v-col>
				</v-row>
				<v-card-text>
				<v-row dense>
					
					<v-col>数量:</v-col>
					<v-col>
						<SelectInput :items="[1,2]" :value="item.quantity" :id="item.item.id" type="quantity" item-text="text" item-value="value" @changeValue="changeCartItem($event,item)"></SelectInput>
					</v-col>
					<v-col>
							<v-btn
								outlined
								height="100%"
								color="error"
								@click="deleteCartItem(item)">
								削除
							</v-btn>
					</v-col>
				</v-row>
				</v-card-text>
			</v-col>
		</v-row>
  </v-card>
</template>


<script>
import SelectInput from '../selects/SelectInput.vue'


  export default {
	data: () => {
			return {

			}
		},
	props: {
		item: {
			type: Object,
			required:true,
		}
		},
	components: {
		SelectInput,
	},
	methods: {
		changeCartItem(data, item) {
			data.size = item.size
			this.$emit('changeCartItem', data)
		},
		deleteCartItem(item) {
			this.$emit('deleteCartItem',item)
		}
	},
	}
</script>