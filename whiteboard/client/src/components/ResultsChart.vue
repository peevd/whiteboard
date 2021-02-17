<script>
import { Doughnut, mixins } from 'vue-chartjs';

const { reactiveProp } = mixins;

export default {
  name: 'ResultsChart',
  extends: Doughnut,
  mixins: [reactiveProp],
  props: {
    options: {
      type: Object,
      default() {
        return {
          legend: {
            display: false,
          },
          responsive: false,
        };
      },
    },
    width: {
      type: Number,
      default: 300,
    },
    height: {
      type: Number,
      default: 300,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>

<style scoped>
div > canvas {
  margin: auto;
}
</style>
