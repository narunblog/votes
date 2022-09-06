<template>
	<v-card
		outlined>
		<v-row no-gutters>
			<v-col cols="4" class="d-flex align-center">
				<v-img max-height="100" contain :src="orderItem.item.image"></v-img>
			</v-col>
			<v-col cols="8">
				<v-row no-gutters>
					<v-col cols="12">
						<v-card-title class="text-h5">{{ orderItem.item.name }}</v-card-title>
					</v-col>
					<v-col cols="12">
						<v-card-text>サイズ:{{ orderItem.size }}</v-card-text>
					</v-col>
					<v-col cols="12">
						<v-card-text>数量:{{ orderItem.quantity }}</v-card-text>
					</v-col>
				</v-row>
			</v-col>
		</v-row>
  </v-card>
</template>


<script>
export default {
		data: () => ({}),
		props: {
			orderItem: {
				type: Object,
				require: true,
			},
		},
	}
</script>