<template>
<div>
  <v-row justify="start">
    <v-col cols="12">
      <v-btn color="primary" outlined @click="isShowFilterCard=!isShowFilterCard">
        <v-icon left>
          mdi-filter-variant
        </v-icon>
        フィルタ
      </v-btn>
    </v-col>
    <v-col cols="12" v-if="isShowFilterCard">
      <VoteResultFilterCard @formActionDone="formActionDone"></VoteResultFilterCard>
    </v-col>
  </v-row>
  <v-row justify="center">
    <v-col cols="6">
      <bar-chart v-if="!loading" :chart-data="chartData" :options="options"></bar-chart>
    </v-col>
  </v-row>
</div>
</template>

<script>
import BarChart from '../charts/BarChart.vue'
import { axiosAPI } from '@/mixins/AxiosAPI';
import VoteResultFilterCard from '../cards/VoteResultFilterCard.vue';

  export default {
    components: {
      BarChart,
      VoteResultFilterCard,
    },
    data () {
      return {
        isShowFilterCard:false,
        chartData: {},
        options: {
          legend: {
            display: false,
          },
          scales: {
            xAxes: [{
              stacked: true,
            }],
            yAxes: [{
              stacked: true,
            }],
          },
          tooltips: {
            mode: 'index',
            filter: function (item, data) {
              data = data.datasets[item.datasetIndex].data[item.index];
              return !isNaN(data) && data !== null;
            },
          },
        },
        labels: [],
        datasets: [],
        labelsOfDatasets:[],
        loading:true,
      }
    },
    mounted () {
      this.createChartData()
    },
    methods: {
      fillData() {
        const newData = {
          labels: this.labels,
          datasets: this.datasets,
        }
        this.chartData = Object.assign({}, newData)
      },
      getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      },
      getLabels(data) {
        const items = data
        this.labels.splice(0)
        items.forEach(item => {
          this.labels.push(item.name)
        })
      },
      getDatasets(data) {
        const items = data
        this.labelsOfDatasets.splice(0)
        this.datasets.splice(0)

        items.forEach(item => {
          item.size.forEach(s => {
            if (!this.labelsOfDatasets.includes(s)) {
              this.labelsOfDatasets.push(s)
            }
          })
        })
        let dataset = {}
        this.labelsOfDatasets.forEach(label => {
          dataset = {
            label: label,
            backgroundColor: '#f87979',
            data: [...Array(this.labels.length)]
          }
          this.datasets.push(dataset)
        })
      },
      async getDataOfDatasets(params={}) {
        const endpoint = '/api/votes/order/item/count/'
        await axiosAPI.get(endpoint, { params: params })
          .then(response => {    
            const data = response.data[0]
            data.forEach(d => {
              let size = d.size__size
              let indexOfDatasets = this.labelsOfDatasets.indexOf(size)

              let name = d.item__name
              let indexOfLabels = this.labels.indexOf(name)

              let value = d.quantity__sum
              this.$set(this.datasets[indexOfDatasets].data, indexOfLabels, value)              
            })
        })
      },
      createChartData(params={}) {
        const endpoint = '/api/votes/item/'
        axiosAPI.get(endpoint)
          .then(async(response) => {
            const data = [...response.data]
            this.getLabels(data)
            this.getDatasets(data)
            await this.getDataOfDatasets(params)
            this.fillData()
            this.loading = false
        })
      },
      formActionDone(formData) {
        this.isShowFilterCard = false
        const params = {
          order__vote: formData.vote,
          order__user: formData.user,
          order__order_datetime_after: formData.startDatetime,
          order__order_datetime_before:formData.endDatetime,
        }
        this.createChartData(params)
      }
  },
  }
</script>

<style>
  .small {
    max-width: 600px;
    margin:  150px auto;
  }
</style>


<!--[
            {
              label: 'XS',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(),,this.getRandomInt(),]
            },
            {
              label: 'S',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(),,this.getRandomInt(),]
            },
            {
              label: 'M',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(),,this.getRandomInt(),]
            },
            {
              label: 'L',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(),,this.getRandomInt(),]
            },
            {
              label: 'XL',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(),,this.getRandomInt(),]
            },
            {
              label: '23.0',
              backgroundColor: '#f87979',
              data: [, this.getRandomInt(),,]
            },
            {
              label: '23.5',
              backgroundColor: '#f87979',
              data: [, this.getRandomInt(),,]
            },
            {
              label: '24.0',
              backgroundColor: '#f87979',
              data: [, this.getRandomInt(),,]
            },
            {
              label: '24.5',
              backgroundColor: '#f87979',
              data: [, this.getRandomInt(),,]
            },
            {
              label: '100',
              backgroundColor: '#f87979',
              data: [,,,this.getRandomInt()]
            },
            {
              label: '180',
              backgroundColor: '#f87979',
              data: [,,,this.getRandomInt()]
            },
          ]-->