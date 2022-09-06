<template>
    <v-container>
        <v-row>
					<Parent @changeValue="changeValue" :items="items" :value.sync="testComputed"></Parent>
        </v-row>
        <v-row>
            <v-btn @click="pushItems">
            itemsを増やす
        </v-btn>
        </v-row>
        <v-row>
            {{ value }}
        </v-row>
        
    </v-container>
</template>

<script>
import Parent from './TestSelectParent'


export default {
    components: {
    Parent,
},
    data: () => ({
        items: [
				{ text: 'text1', value: 1 },
				{ text: 'text2', value: 2 },
				{ text: 'text3', value: 3 },
				{ text: 'text4', value: 4 },
				{ text: 'text5', value: 5 },
        ],
        value:{ text: 'text1', value: 1 },
    }),
    computed: {
		testComputed: {
            get () {
                return this.value
            },
            set (value) {
                console.log('success')
                this.value = value
                console.log(value)
                console.log('これでおじば終わり')
            }
        },
	},
	methods: {
    changeValue(object) {
            //console.log('これはおじばのメソッドになります。')
			//console.log(object)
        },
    pushItems() {
        const key = this.items.length + 1
        const value = `text${key}`
        this.items.push({text:value,value:key})
    },
    },
}
</script>