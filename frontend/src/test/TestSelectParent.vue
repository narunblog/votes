<template>
    <v-container>
        <v-row>
					<Select @changeValue="changeValue" :items="items" :value.sync="testComputed"></Select>
        </v-row>
				<v-row>
					これは親の値です{{ testComputed }}
        </v-row>
    </v-container>
</template>

<script>
import Select from './TestSelect'

export default {
    components: {
        Select
    },
    data: () => ({
	}),
	props: {
		items: {
			type: Array,
			required:true,
		},
		value: {
			type:null,
		}
	},
	computed: {
		testComputed: {
            get () {
                return this.value
            },
            set (value) {
                this.$emit('update:value', value)
            }
        },
	},
	methods: {
		changeValue(object) {
			console.log('親からおじばのemitを起動しました')
			this.$emit('changeValue',object)
			}
		},
}
</script>