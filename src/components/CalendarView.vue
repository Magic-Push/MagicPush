<template>
  <div class="min-h-full w-full lg:flex lg:h-full lg:flex-col">
    <div class="shadow rounded-lg ring-1 ring-black ring-opacity-5 lg:flex lg:flex-auto lg:flex-col">
      <div class="grid grid-cols-7 rounded-t-lg gap-px border-b border-gray-300 bg-gray-200 text-center text-xs font-semibold leading-6 text-gray-700 lg:flex-none">
        <div class="flex justify-center rounded-tl-lg bg-white py-2">
          <span>M</span>
          <span class="sr-only sm:not-sr-only">on</span>
        </div>
        <div class="flex justify-center bg-white py-2">
          <span>T</span>
          <span class="sr-only sm:not-sr-only">ue</span>
        </div>
        <div class="flex justify-center bg-white py-2">
          <span>W</span>
          <span class="sr-only sm:not-sr-only">ed</span>
        </div>
        <div class="flex justify-center bg-white py-2">
          <span>T</span>
          <span class="sr-only sm:not-sr-only">hu</span>
        </div>
        <div class="flex justify-center bg-white py-2">
          <span>F</span>
          <span class="sr-only sm:not-sr-only">ri</span>
        </div>
        <div class="flex justify-center bg-white py-2">
          <span>S</span>
          <span class="sr-only sm:not-sr-only">at</span>
        </div>
        <div class="flex justify-center rounded-tr-lg bg-white py-2">
          <span>S</span>
          <span class="sr-only sm:not-sr-only">un</span>
        </div>
      </div>
      <div class="flex bg-gray-200 text-xs leading-6 text-gray-700 lg:flex-auto">
        <div class="hidden w-full min-h-full lg:grid lg:grid-cols-7 lg:grid-rows-6 lg:gap-px">
          <!--
            Always include: "relative py-2 px-3"
            Is current month, include: "bg-white"
            Is not current month, include: "bg-gray-50 text-gray-500"
          -->
          <template v-for="day in days" :key="day.date">
            <div class="relative px-3 py-2 cursor-pointer" :class="day.isCurrentMonth ? 'bg-white' : 'bg-gray-50 text-gray-500'">
              <time datetime="2021-12-31">{{ day.day }}</time>
              <ol class="mt-2">
                <li v-for="notification in day.notifications" :key="notification.id" @click="$emit('notificationClicked', notification)">
                  <div class="group flex cursor-pointer">
                    <p class="flex-auto truncate font-medium text-gray-900 group-hover:text-indigo-600">{{ notification.name }}</p>
                    <time datetime="2022-01-03T10:00" class="ml-3 hidden flex-none text-gray-500 group-hover:text-indigo-600 xl:block">
                      {{ getTime(notification.scheduled_at) }}
                    </time>
                  </div>
                </li>
              </ol>
              <div @click="$emit('createNotification', day.date)" class="w-full h-full"></div>
            </div>
          </template>
        </div>
        <div class="isolate grid grow w-full h-full grid-cols-7 grid-rows-6 gap-px lg:hidden">
          <!--
            Always include: "flex flex-col py-2 px-3 hover:bg-gray-100 focus:z-10"
            Is current month, include: "bg-white"
            Is not current month, include: "bg-gray-50"
            Is selected or is today, include: "font-semibold"
            Is selected, include: "text-white"
            Is not selected and is today, include: "text-indigo-600"
            Is not selected and is current month, and is not today, include: "text-gray-900"
            Is not selected, is not current month, and is not today: "text-gray-500"
          -->
          <template v-for="day in days" :key="day.date">
            <button type="button" class="flex flex-col bg-gray-50 px-3 py-2 text-gray-500 hover:bg-gray-100"
                    :class="day.isCurrentMonth ? 'bg-white' : 'bg-gray-50 text-gray-500'"
                    @click="$emit('notificationClicked', notification)">
              <!--
                Always include: "ml-auto"
                Is selected, include: "flex h-6 w-6 items-center justify-center rounded-full"
                Is selected and is today, include: "bg-indigo-600"
                Is selected and is not today, include: "bg-gray-900"
              -->
              <time datetime="2021-12-27" class="ml-auto">{{ day.day }}</time>
              <span class="sr-only">{{ day.notifications.length }} events</span>

              <template v-if="day.notifications.length > 0">
                <span class="-mx-0.5 mt-auto flex flex-wrap-reverse"></span>
                <span v-for="notification in day.notifications" :key="notification.id" class="mx-0.5 mb-1 h-1.5 w-1.5 rounded-full bg-gray-400"></span>
              </template>
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CalendarView",
  props: ["days"],
  methods: {
    getTime(created_at) {
      const date = new Date(created_at);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  }
}
</script>

<style scoped>

</style>