<template>
	<v-select
		:items="items"
		:value="quantityValue"
		outlined
		:menu-props="{ bottom: true, offsetY: true }"
		dense
		hide-details
		@change="changeValue">
	</v-select>
</template>


<script>
export default {
	name: 'SizeSelectInput',
	props: {
		items: {
			type: Array,
			required: true,
		},
		quantityValue: {
			type: [String,Number],
			required: true,
		},
	},
	data() {
		return {
		}
	},
	computed: {
	},
	methods: {
		changeValue(event) {
			this.$emit('update:quantityValue',event)
		}
		
	},
	
}
</script>