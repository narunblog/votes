<template>
<div>
	<v-select
		v-model="defaultValue"
		:items="items"
		:item-value="itemValue"
		:item-text="itemText"
		return-object
		outlined
		:menu-props="{ bottom: true, offsetY: true }"
		dense
		hide-details
		@change="$emit('changeValue', { value:$event, id:id,type:type})">
	</v-select>
</div>
</template>


<script>
export default {
	name: 'SelectInput',
	props: {
		items: {
			type: Array,
			required: true,
		},
		value: {
			required: true,
		},
		id: {
			required:true,
		},
		type: {
			required:true
		},
		itemText: {
			type: String,
			required: true,
		},
		itemValue: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			defaultValue:this.value,
		}
	},
}
</script>