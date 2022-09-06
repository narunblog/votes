<template>
    <v-container>
        <v-row>
            <v-textarea
                label="Parent"
                v-model="fieldComputed"
            />
        </v-row>

        <v-row>
            <Child
                v-bind:child-field.sync="fieldComputed"
            />
        </v-row>
    </v-container>
</template>

<script>
import Child from './Child'

export default {
    components: {
        Child
    },
    data: () => ({
        field: ""
    }),
    computed: {
        fieldComputed: {
            get () {
                return this.field
            },
            set (value) {
                this.field =value
            }
        }
    }
}
</script>