<template>
  <div class="border-gray-100" style="border-left-style: solid; border-left-width: 0px;">
    <div class="flex flex-col h-screen pt-4 ">
      <div class="flex w-full flex items-center">
        <div class="pb-4 pl-4">
          <h1 class="font-medium text-xl text-slate-900">
            Scheduler
          </h1>
        </div>

        <div class="absolute right-4 top-4 flex items-center">
          <div class="relative flex items-center rounded-md bg-white shadow-sm md:items-stretch">
            <button type="button" @click="previousMonth"
                    class="flex h-9 w-12 items-center justify-center rounded-l-md border-y border-l border-gray-300 pr-1 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:pr-0 md:hover:bg-gray-50">
              <span class="sr-only">Previous month</span>
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd"
                      d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z"
                      clip-rule="evenodd"/>
              </svg>
            </button>
            <button type="button"
                    class="hidden border-y border-gray-300 px-3.5 text-sm font-semibold text-gray-900 hover:bg-gray-50 focus:relative md:block">
              {{ parseDate(currentDate) }}
            </button>
            <span class="relative -mx-px h-5 w-px bg-gray-300 md:hidden"></span>
            <button type="button" @click="nextMonth"
                    class="flex h-9 w-12 items-center justify-center rounded-r-md border-y border-r border-gray-300 pl-1 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:pl-0 md:hover:bg-gray-50">
              <span class="sr-only">Next month</span>
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                      clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
          <button @click="createNotification(null)"
                  class="rounded-md w-full bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 ml-5 items-baseline items-center">
            New notification
          </button>
        </div>
      </div>

      <div class="flex-1 w-full container p-4">
        <CalendarView v-bind:days="days" v-on:notificationClicked="notificationClicked"
                      v-on:createNotification="createNotification"/>
      </div>
    </div>
    <CreateNotificationModal2 v-bind:open="showModal" v-bind:selectedNotification="selectedNotification"
                              v-bind:selectedDate="selectedDate" v-bind:showScheduler="true" v-on:onClose="closeModal" />
  </div>
</template>

<script>
import CalendarView from "@/components/CalendarView";
import CreateNotificationModal2 from "@/modals/CreateNotificationModal2";

export default {
  name: "SchedulePage",
  components: {CalendarView, CreateNotificationModal2},
  data() {
    return {
      showModal: false,
      selectedNotification: null,
      selectedDate: null,
      notifications: [],
      days: [],
      currentDate: new Date(),
    }
  },
  mounted() {
    if (this.$route.query.date) {
      // convert date url safe string to date object
      this.currentDate = new Date(this.$route.query.date);
    }
    this.loadDays();
  },
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  methods: {
    loadDays() {
      let self = this;
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDayOfMonth = (new Date(year, month, 1).getDay() + 6) % 7;
      const daysInMonth = new Date(year, month + 1, 0).getDate();

      const totalCells = 42;
      const previousMonthDays = firstDayOfMonth;
      const nextMonthDays = totalCells - (daysInMonth + previousMonthDays);

      const lastDateOfPrevMonth = new Date(year, month, 0).getDate();
      console.log('lastDateOfPrevMonth: ' + lastDateOfPrevMonth)
      const startDay = lastDateOfPrevMonth - firstDayOfMonth;

      this.days = [];

      for (let i = previousMonthDays; i > 0; i--) {
        this.days.push({
          day: (lastDateOfPrevMonth - i) + 1,
          month: month - 1,
          year: year,
          date: `${year}-${month.toString().padStart(2, '0')}-${((lastDateOfPrevMonth - i) + 1).toString().padStart(2, '0')}`,
          isCurrentMonth: false,
          notifications: []
        });
      }

      for (let i = 1; i <= daysInMonth; i++) {
        this.days.push({
          day: i,
          month: month,
          year: year,
          date: `${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`,
          isCurrentMonth: true,
          notifications: []
        });
      }

      for (let i = 1; i <= nextMonthDays; i++) {
        let date = new Date(year, month + 1, i);
        this.days.push({
          day: i,
          month: date.getMonth(),
          year: date.getFullYear(),
          date: `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`,
          isCurrentMonth: false,
          notifications: []
        });
      }

      this.getScheduledNotifications();
    },
    getScheduledNotifications() {
      let self = this;
      this.$store.dispatch("getScheduledNotifications", { start_date: this.days[0].date, end_date: this.days[this.days.length - 1].date })
          .then((response) => {
            self.notifications = response.data;
            // sort notifications by scheduled date
            self.notifications.sort((a, b) => {
              return new Date(a.scheduled_at) - new Date(b.scheduled_at);
            });
            self.notifications.forEach((notification) => {
              let date = new Date(notification.scheduled_at);
              let mDay = date.getDate();
              let mMonth = date.getMonth();
              let mYear = date.getFullYear();

              let dayObj = self.days.find((day) => day.day === mDay && day.month === mMonth && day.year === mYear);
              if (dayObj) {
                if (dayObj.notifications.find((n) => n.id === notification.id)) return;
                dayObj.notifications.push(notification);
              }
            });
          })
          .catch((err) => {
            console.log("Error", err);
          });
    },
    nextMonth() {
      this.currentDate = new Date(this.currentDate.setMonth(this.currentDate.getMonth() + 1));
      this.addParamsToLocation({date: this.currentDate, app: this.currentApp.id });
      this.loadDays();
    },
    previousMonth() {
      this.currentDate = new Date(this.currentDate.setMonth(this.currentDate.getMonth() - 1));
      this.addParamsToLocation({date: this.currentDate, app: this.currentApp.id });
      this.loadDays();
    },
    addParamsToLocation(params) {
      history.pushState(
          {},
          null,
          this.$route.path +
          '?' +
          Object.keys(params)
              .map(key => {
                return (
                    encodeURIComponent(key) + '=' + encodeURIComponent(params[key])
                )
              })
              .join('&')
      )
    },
    createNotification(date) {
      if (date !== null) {
        console.log(date);
        this.selectedDate = date;
      } else {
        this.selectedDate = null;
      }
      this.selectedNotification = null;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.getScheduledNotifications();
    },
    parseDate(dateStr) {
      let date = new Date(dateStr);

      let formatter = new Intl.DateTimeFormat('en-GB', {
        month: 'short'
      });

      return formatter.format(date);
    },
    notificationClicked(notification) {
      this.selectedNotification = notification;
      this.showModal = true;
    }
  }
}
</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
}

.notification-holder {
  width: 500px;
}

.notification-preview {
  display: block;
  width: 100%;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  background: #ffffff;
  border: solid 1px #d9d9d9;
}
</style>