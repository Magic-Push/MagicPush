<template>
  <button data-drawer-target="default-sidebar" data-drawer-toggle="default-sidebar" aria-controls="default-sidebar" type="button" class="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200">
    <span class="sr-only">Open sidebar</span>
    <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
      <path clip-rule="evenodd" fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
    </svg>
  </button>

  <aside id="default-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0 bg-background" aria-label="Sidebar">
    <!-- Flex container -->
    <div class="flex flex-col h-full">
      <!-- Main content wrapper -->
      <div class="flex-grow overflow-y-auto">
        <div class="px-3 py-4">
          <AppDropdown v-on:appSelected="appSelected"/>
          <ul class="space-y-2 font-medium">
            <li>
              <div v-for="menuItem in items" v-bind:key="menuItem.path" @click="menuItemClick(menuItem)"
                   class="flex mb-1 items-center p-3 text-slate-600 rounded-lg hover:bg-slate-50 group cursor-pointer font-sans"
                   :class="menuItem.selected === true ? 'bg-slate-50' : ''">
                <component :is="menuItem.icon"  class="w-6 h-6 group-hover:text-primary-500" :class="menuItem.selected === true ? 'text-primary-500' : menuItem.enabled ? 'text-gray-400' : 'text-gray-400 opacity-80'"></component>
                <span class="ms-3 text-sm group-hover:text-primary-500" :class="menuItem.selected === true ? 'text-primary-500' : menuItem.enabled ? 'text-slate-600' : 'text-slate-600 opacity-80'">
                {{ menuItem.name }}
              </span>
                <span v-if="!menuItem.enabled" class="bg-primary-500 text-white text-xs font-normal px-2.5 py-0.5 rounded-lg dark:bg-gray-600 dark:text-gray-300 ml-1 opacity-80">coming soon</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <!-- Sticky footer -->
      <div class="px-3 py-4 w-full text-center space-x-2">
        <span @click="logout" class="text-gray-400 text-xs cursor-pointer">Logout</span>
        <a href="https://magicpush.alphadoc.io/" target="_blank" class="text-gray-400 text-xs cursor-pointer">Docs</a>
        <a href="#" target="_blank" class="text-gray-400 text-xs cursor-pointer">Terms</a>
        <a href="mailto:support@playstudioapps.com" class="text-gray-400 text-xs cursor-pointer">Support</a>
      </div>
    </div>
  </aside>
</template>

<script>
import AppDropdown from "@/components/AppDropdown";
import { UserCircleIcon, CogIcon, CreditCardIcon, BarsArrowDownIcon, CalendarIcon, ChatBubbleOvalLeftIcon, HomeIcon, ChartBarIcon } from "@heroicons/vue/24/outline";

export default {
  name: "SideBar",
  components: {
    AppDropdown,
  },
  data() {
    return {
      items: [
        {
          path: '/dashboard',
          icon: HomeIcon,
          color: 'bg-amber-400',
          name: 'Home',
          selected: true,
          enabled: true
        },
        {
          path: '/notifications',
          icon: ChatBubbleOvalLeftIcon,
          color: 'bg-amber-400',
          name: 'Notifications',
          selected: false,
          enabled: true
        },
        {
          path: '/scheduler',
          icon: CalendarIcon,
          color: 'bg-amber-400',
          name: 'Scheduler',
          selected: false,
          enabled: true
        },
        {
          path: '/flows',
          icon: BarsArrowDownIcon,
          color: 'bg-amber-400',
          name: 'Flows',
          selected: false,
          enabled: true
        },
        {
          path: '/billing',
          icon: CreditCardIcon,
          color: 'bg-blue-400',
          name: 'Billing',
          selected: false,
          enabled: true
        },
        {
          path: '/app-settings',
          icon: CogIcon,
          color: 'bg-rose-300',
          name: 'App Settings',
          selected: false,
          enabled: true
        },
        {
          path: '/user-settings',
          icon: UserCircleIcon,
          color: 'bg-rose-300',
          name: 'User Settings',
          selected: false,
          enabled: true
        }
      ]
    }
  },
  mounted() {
    this.items.forEach((item) => {
      if (this.$route.path === item.path) {
        item.selected = true;
      } else {
        item.selected = false;
      }
    });

    if (this.currentUser) {
      if (this.currentUser.is_admin) {
        this.items.push({
          path: '/admin',
          icon: ChartBarIcon,
          color: 'bg-amber-400',
          name: 'Admin panel',
          selected: false,
          enabled: true
        })
      }
    } else {
      let self = this;
      let watcher = this.$watch(() => this.$store.state.auth.user, (newVal, oldVal) => {
        if (newVal) {
          if (newVal.is_admin) {
            this.items.push({
              path: '/admin',
              icon: ChartBarIcon,
              color: 'bg-amber-400',
              name: 'Admin panel',
              selected: false,
              enabled: true
            })
          }
          watcher();
        }
      });
    }
  },
  methods: {
    createProject() {
      this.$emit("createProject");
    },
    menuItemClick(item) {
      this.items.forEach((item) => {
        item.selected = false;
      });
      let menuItem = this.items.find((i) => i.path === item.path);

      if (menuItem.path !== '/billing') {
        menuItem.selected = true;

        this.$router.push({ path: menuItem.path, query: { app: this.currentApp.id }});
      } else {
        this.$store.dispatch('getBillingPortal')
            .then((res) => {
              window.location.href = res.data.url;
            })
            .catch((err) => {
              console.log(err);
            });
      }
    },
    appSelected(app) {
      this.$emit("appSelected", app);
    },
    logout() {
      this.$store.dispatch("userShouldHaveBeenLoggedOut");
    }
  },
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    },
    checkoutUrl() {
      return this.$store.state.checkout_url;
    },
    billingUrl() {
      return this.$store.state.billing_url;
    },
    currentUser() {
      return this.$store.state.auth.user;
    }
  }
}
</script>

<style scoped>

</style>