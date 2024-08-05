<template>
  <div class="border-gray-100" style="border-left-style: solid; border-left-width: 0px;">
    <div class="flex flex-col h-screen p-4">
      <div class="flex w-full flex items-center">
        <div class="pb-4">
          <h1 class="font-medium text-xl text-slate-900">
            Notifications
          </h1>
        </div>

        <div class="absolute right-4 top-4 flex items-center">
          <button @click="createNotification"
                  class="rounded-md w-full bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
            New notification
          </button>
        </div>
      </div>

      <div class="flex-1 w-full container">
        <div v-if="getNotifications !== null && getNotifications.notifications.length > 0">
          <ul role="list" class="divide-y divide-gray-100">
            <li v-for="notification in getNotifications.notifications" :key="notification.id" class="flex items-center justify-between gap-x-6 py-5">
              <div @click="openNotification(notification)" class="min-w-0 cursor-pointer">
                <div class="flex items-start gap-x-3">
                  <p class="text-sm font-semibold leading-6 text-gray-900">
                    {{ notification.name }}
                  </p>
                  <p :class="[statuses[notification.sent ? notification.delivery_percentage > 90 ? 'Delivered' : 'Sending' : notification.delivered ? 'Delivered' : 'Draft'], 'rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset']">
                    {{ notification.sent ? notification.delivery_percentage > 0 ? notification.delivery_percentage < 100 ? 'Delivered: ' : 'Delivered' : 'Sending' : 'Draft' }}
                    {{ notification.delivery_percentage > 0 && notification.delivery_percentage < 100 ? notification.delivery_percentage.toFixed(2) + '%' : ''}}
                  </p>
                </div>
                <div class="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
                  <p class="whitespace-nowrap">
                    <span class="font-medium">
                      {{ notification.default_title }}
                    </span>
                    {{ notification.default_message }}
                  </p>
                  <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 fill-current">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  <p class="truncate">
                    Created at <time :datetime="notification.created_at">{{ notification.created_at }}</time>
                  </p>
                </div>
              </div>
              <div class="flex flex-none items-center gap-x-4">
                <Menu as="div" class="relative flex-none">
                  <MenuButton class="-m-2.5 block p-2.5 text-gray-500 hover:text-gray-900">
                    <span class="sr-only">Open options</span>
                    <EllipsisVerticalIcon class="h-5 w-5" aria-hidden="true" />
                  </MenuButton>
                  <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <MenuItems class="absolute right-0 z-10 mt-2 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                      <MenuItem v-if="!notification.sent" v-slot="{ active }">
                        <span @click="sendNotification(notification)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                          Send now
                        </span>
                      </MenuItem>
                      <MenuItem v-if="!notification.sent" v-slot="{ active }">
                        <span @click="openNotification(notification)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                          Edit
                        </span>
                      </MenuItem>
                      <MenuItem v-slot="{ active }">
                        <span @click="duplicateNotification(notification)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                          Duplicate
                        </span>
                      </MenuItem>
                    </MenuItems>
                  </transition>
                </Menu>
              </div>
            </li>
          </ul>
          <nav class="flex items-center justify-between border-t border-gray-200 bg-white py-3" aria-label="Pagination">
            <div class="hidden sm:block">
              <p class="text-sm text-gray-700">
                Showing <span class="font-medium">{{ page === 1 ? '1' : getNotifications.notifications.length * (page - 1) }}</span> to <span class="font-medium">{{ getNotifications.notifications.length * page }}</span> of <span class="font-medium">{{ getNotifications.total }}</span> results
              </p>
            </div>
            <div class="flex flex-1 justify-between sm:justify-end">
              <button @click="previous" :disabled="page === 1" class="relative inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0 cursor-pointer disabled:opacity-60">
                Previous
              </button>
              <button @click="next" :disabled="getNotifications.total <= getNotifications.notifications.length * page" class="relative ml-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0 cursor-pointer disabled:opacity-60">
                Next
              </button>
            </div>
          </nav>
        </div>
        <div v-else class="text-center mx-auto" style="margin-top: 20%;">
          <span class="text-lg font-semibold text-gray-700 block">Send your first notification</span>
          <span class="text-sm font-sans text-gray-400 block mt-2 mb-6">Easily send your first notifications</span>
          <button @click="createNotification"
                  class="rounded-md bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
            New notification
          </button>
        </div>
      </div>
    </div>

    <CreateNotificationModal2 v-bind:open="showModal" v-bind:selectedNotification="selectedNotification"
                              v-bind:showScheduler="false" v-on:onClose="closeModal" />
  </div>
</template>

<script>
import { EllipsisVerticalIcon } from '@heroicons/vue/20/solid'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import CreateFlowModal from "@/modals/CreateFlowModal.vue";
import CreateNotificationModal2 from "@/modals/CreateNotificationModal2.vue";

export default {
  name: "NotificationsPage",
  components: {CreateNotificationModal2, EllipsisVerticalIcon, Menu, MenuButton, MenuItem, MenuItems},
  data() {
    return {
      statuses: {
        Delivered: 'text-green-600 bg-green-50 ring-green-500/10',
        Draft: 'text-gray-600 bg-gray-50 ring-gray-500/10',
        Sending: 'text-yellow-600 bg-yellow-50 ring-yellow-500/10',
      },
      flows: [],
      showModal: false,
      selectedFlow: null,
      page: 1,
      selectedNotification: null,
    }
  },
  mounted() {
    let self = this;
    this.$store.dispatch('getNotifications', { page: this.page })
        .then((res) => {

        })
        .catch((err) => {
          console.error(err);
        });
  },
  computed: {
    getNotifications() {
      return this.$store.state.notificationsData;
    },
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  watch: {
    currentApp: {
      handler: function (newVal, oldVal) {
        if (newVal) {
          this.loadNotifications();
        }
      },
      deep: true
    }
  },
  methods: {
    loadNotifications() {
      this.$store.dispatch('getNotifications', { page: this.page })
          .then((res) => {

          })
          .catch((err) => {
            console.error(err);
          });
    },
    closeModal() {
      this.showModal = false;
      this.selectedFlow = null;

      this.loadNotifications();
    },
    createNotification() {
      this.selectedNotification = null;
      this.showModal = true;
    },
    openNotification(notification) {
      this.selectedNotification = notification;
      this.showModal = true;
    },
    sendNotification(notification) {
      let self = this;

      notification['sent'] = true;
      this.$store.dispatch('updateNotification', notification)
          .then((res) => {
            self.loadNotifications();
          })
          .catch((err) => {
            console.error(err);
          });
    },
    duplicateNotification(notification) {
      this.selectedNotification = notification;
      this.selectedNotification['id'] = null;
      this.showModal = true;
    },
    previous() {
      this.page -= 1;
      this.loadNotifications();
    },
    next() {
      this.page += 1;
      this.loadNotifications();
    }
  }
}
</script>

<style scoped>

</style>