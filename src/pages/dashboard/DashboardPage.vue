<template>
  <div class="p-4 border-gray-100 h-screen" style="border-left-style: solid; border-left-width: 0;">
    <h1 class="font-medium text-xl text-slate-900">
      Dashboard
    </h1>

    <div class="container mt-4">
      <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div v-for="item in stats" :key="item.name" class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 flex justify-between">
          <div>
            <dt class="truncate text-sm font-medium text-gray-500">{{ item.name }}</dt>
            <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{{ item.stat }}</dd>
          </div>
          <div class="flex items-center px-2.5 py-0.5 text-base font-semibold dark:text-green-500 text-center" :class="item.growth >= 0 ? 'text-green-500' : 'text-red-500'">
            <svg v-if="item.growth === null" fill="currentColor" class="w-6 h-6" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.288 9.463a4.856 4.856 0 0 0-4.336-2.3 4.586 4.586 0 0 0-3.343 1.767c.071.116.148.226.212.347l.879 1.652.134-.254a2.71 2.71 0 0 1 2.206-1.519 2.845 2.845 0 1 1 0 5.686 2.708 2.708 0 0 1-2.205-1.518L13.131 12l-1.193-2.26a4.709 4.709 0 0 0-3.89-2.581 4.845 4.845 0 1 0 0 9.682 4.586 4.586 0 0 0 3.343-1.767c-.071-.116-.148-.226-.212-.347l-.879-1.656-.134.254a2.71 2.71 0 0 1-2.206 1.519 2.855 2.855 0 0 1-2.559-1.369 2.825 2.825 0 0 1 0-2.946 2.862 2.862 0 0 1 2.442-1.374h.121a2.708 2.708 0 0 1 2.205 1.518l.7 1.327 1.193 2.26a4.709 4.709 0 0 0 3.89 2.581h.209a4.846 4.846 0 0 0 4.127-7.378z"/>
            </svg>
            <span v-else>
              {{ item.growth.toFixed(2) }}%
            </span>
            <svg :class="item.growth >= 0 ? '' : 'rotate-180'" class="w-3 h-3 ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13V1m0 0L1 5m4-4 4 4"/>
            </svg>
          </div>
        </div>
      </dl>

      <div class="mt-4 w-full bg-white rounded-lg shadow p-4 md:p-6">
        <div class="flex justify-between mb-5">
          <div>
            <p class="text-sm font-medium text-gray-500">New subscribers</p>
          </div>
        </div>
        <div id="grid-chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts'

export default {
  name: "DashboardPage",
  data() {
    return {
      stats: [
        {
          name: 'Total subscribers',
          stat: '0',
          growth: null
        },
        {
          name: 'Delivery rate',
          stat: '0%',
          growth: null
        },
        {
          name: 'Open rate',
          stat: '0%',
          growth: null
        }
      ],
      options: {

// set grid lines to improve the readability of the chart, learn more here: https://apexcharts.com/docs/grid/
        grid: {
          show: true,
          strokeDashArray: 4,
          padding: {
            left: 2,
            right: 2,
            top: -26
          },
        },
        series: [
          {
            name: "Subscribers",
            data: [],
            // data: [
            //   123, 156, 98, 145, 134, 122, 67, 189, 155, 103,
            //   78, 145, 99, 112, 140, 76, 130, 148, 167, 190,
            //   83, 91, 100, 179, 160, 65, 110, 88, 172, 134
            // ], // dummy data of the number of new subscribers every day the last 30 days
            color: "#8b5cf6",
          },
        ],
        chart: {
          height: "100%",
          maxWidth: "100%",
          type: "area",
          fontFamily: "Inter, sans-serif",
          dropShadow: {
            enabled: false,
          },
          toolbar: {
            show: false,
          },
        },
        tooltip: {
          enabled: true,
          x: {
            show: false,
          },
        },
        legend: {
          show: true
        },
        fill: {
          type: "gradient",
          gradient: {
            opacityFrom: 0.55,
            opacityTo: 0,
            shade: "#8b5cf6",
            gradientToColors: ["#8b5cf6"],
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          width: 6,
        },
        xaxis: {
          categories: [],
          // categories: [
          //   "2021-09-01",
          //   "2021-09-02",
          //   "2021-09-03",
          //   "2021-09-04",
          //   "2021-09-05",
          //   "2021-09-06",
          //   "2021-09-07",
          //   "2021-09-08",
          //   "2021-09-09",
          //   "2021-09-10",
          //   "2021-09-11",
          //   "2021-09-12",
          //   "2021-09-13",
          //   "2021-09-14",
          //   "2021-09-15",
          //   "2021-09-16",
          //   "2021-09-17",
          //   "2021-09-18",
          //   "2021-09-19",
          //   "2021-09-20",
          //   "2021-09-21",
          //   "2021-09-22",
          //   "2021-09-23",
          //   "2021-09-24",
          //   "2021-09-25",
          //   "2021-09-26",
          //   "2021-09-27",
          //   "2021-09-28",
          //   "2021-09-29",
          //   "2021-09-30",
          // ], // dummy data of last 30 days
          labels: {
            show: false,
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
        },
        yaxis: {
          show: false,
        }
      }
    }
  },
  mounted() {
    let self = this;

    this.$store.dispatch('getInfo')
        .then((response) => {
          self.stats[0].stat = response.data.total_subscribers;
          self.stats[0].growth = response.data.total_subscribers_growth_rate;
          self.stats[1].stat = response.data.delivery_rate.toFixed(2) + "%";
          self.stats[1].growth = response.data.delivery_rate_growth_rate;
          self.stats[2].stat = response.data.click_rate.toFixed(2) + "%";
          self.stats[2].growth = response.data.click_rate_growth_rate;
        })
        .catch((error) => {
          console.log(error);
        });

    this.$store.dispatch('getSubscriberStats')
        .then((response) => {
          response.data.results.forEach((result) => {
            const dateKey = Object.keys(result)[0];

            // Add the date to the categories for the x-axis
            self.options.xaxis.categories.push(dateKey);

            // Add the corresponding value to the data for the series
            self.options.series[0].data.push(result[dateKey]);
          });

          const chart = new ApexCharts(document.querySelector("#grid-chart"), self.options);
          chart.render()
        })
        .catch((error) => {
          console.log(error);
        });
  },
  methods: {
  }
}
</script>

<style scoped>
.image {
  width: 100%;
  height: 230px;
  background-size: cover, cover;
  background-repeat: no-repeat;
}
</style>