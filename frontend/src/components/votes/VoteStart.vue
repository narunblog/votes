<template>
  <v-app>
    <v-container fluid>
      <h1>voteStart</h1>
      <v-btn color="primary" v-on:click.stop="dialog = true"><v-icon>mdi-plus</v-icon>作成</v-btn>
      <VoteStartDialog ref="voteStartDialog" :dialog="dialog" v-on:onClickClose="dialog=false" v-on:onClickSave="dialog=false">
      </VoteStartDialog>
    </v-container>
  </v-app>
</template>


<script>
import VoteStartDialog from '../dialogs/VoteStartDialog.vue'


export default {
  name: 'VoteStart',
  components: {
    VoteStartDialog,
  },
  data() {
    return {
      dialog:false,
    }
  },
  methods: {},
};
</script>