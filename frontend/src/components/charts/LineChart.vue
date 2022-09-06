<!-- Chartjsを使ってコンポーネント化する場合は<template>タグを使用しない -->
<!--参考サイト:https://vue-chartjs.org/ja/guide/#vue-%E3%82%B7%E3%83%B3%E3%82%B0%E3%83%AB%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88 -->

<script>
import { Line,mixins } from 'vue-chartjs'
const { reactiveProp } = mixins;

export default {
	extends: Line,
	mixins: [reactiveProp],
  props: ["options"],
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>

<style>
</style>