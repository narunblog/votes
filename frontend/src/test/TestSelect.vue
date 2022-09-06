<template>
	<div>
		<v-select
		v-model="testComputed"
		:items="items"
		item-text="text"
		item-value="value"
		return-object
		outlined
		:menu-props="{ bottom: true, offsetY: true }"
		dense
		hide-details
		@change="changeValue">
	</v-select>
	これは孫の値です{{ testComputed }}
	</div>
</template>


<script>
export default {
	name: 'TestSelect',
	data() {
		return {
		}
	},
	props: {
		items: {
			type: Array,
			required:true,
		},
		value: {
			type:null,
		},
	},
	computed: {
		testComputed: {
            get () {
                return this.value
            },
            set (value) {
                this.$emit('update:value', value)
            }
        }
	},
	methods: {
		changeValue(object) {
			console.log('子供から親のemitを起動しました。')
			this.$emit('changeValue',object)
		},
	},
	
}
</script>