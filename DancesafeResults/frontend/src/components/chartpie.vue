<template>
  <div class = 'chart'>
    <!-- import font awesome for legend icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">

    <!--
      Both the :data and :config properties are deeply reactive so any changes
      to these will cause the chart to update.
    -->
    <chart-pie :data = 'demoChart' :config = 'chartConfig'></chart-pie>
  </div>
</template>

<script>
import { ChartPie } from 'vue-d2b'
import axios from 'axios'

export default {
  data: () => ({
    // Describe the pie-chart data for more information on this checkout
    // the d2bjs.org docs.
    chartData: [
      {label: 'arc 1', value: 1},
      {label: 'arc 2', value: 31},
      {label: 'arc 3', value: 80},
      {label: 'arc 4', value: 8}
    ],
    demoChart: '',
    piepiepie: [],
    // The chart config property is a callback function that is executed
    // any time the chart undergoes an update. The function receives the
    // d2b chart generator as an argument and can be configured as described
    // as described by the d2bjs.org docs.
    chartConfig (chart) {
      chart.donutRatio(0.5)
    }
  }),
  methods: {
    fetchChart () {
      const path = `http://192.168.4.1:9090/api/demo_chart`
      axios.get(path)
        .then(response => {
          this.demoChart = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created: function () {
    this.demoChart = this.fetchChart()
  },
  components: {
    ChartPie
  }
}
</script>

<style scoped>
  /*
    The chart dimensions is bound by the outer container in this case '.chart'.
  */
  .chart{
    height: 500px;
  }
</style>
