<template>
  <div class="relative mb-5">
    <button @click="dropDownVisible = !dropDownVisible" class="rounded-md w-full bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 text-center inline-flex items-center" type="button">
      {{ selectedApp ? selectedApp.name : "Loading..."  }}
      <svg class="absolute w-2.5 h-2.5 me-4 right-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
      </svg>
    </button>

    <!-- Dropdown menu -->
    <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="dropDownVisible" class="z-10 bg-white rounded-lg shadow w-full absolute">
        <ul class="app-list py-2 overflow-y-auto text-gray-700 max-h-60" aria-labelledby="dropdownUsersButton">
          <li v-for="app in allApps" :key="app.id">
            <a href="#" class="flex items-center px-4 py-2 hover:bg-gray-100" :class="app.id === selectedApp.id ? 'bg-gray-100' : ''" @click="clickApp(app)">
              {{ app.name }}
            </a>
          </li>
        </ul>
        <a @click="createApp" href="#" class="flex items-center p-3 text-sm font-medium text-primary-600 border-t border-gray-200 rounded-b-lg bg-gray-50 hover:bg-gray-100  hover:underline">
          <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7 7V5"/>
          </svg>
          Create new app
        </a>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "AppDropdown",
  data() {
    return {
      selectedApp: null,
      dropDownVisible: false
    }
  },
  computed: {
    allApps() {
      return this.$store.state.apps;
    },
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  mounted() {
    if (this.allApps !== null) {
      if (this.$route.query.app !== undefined) {
        this.selectedApp = this.allApps.find(app => app.id === parseInt(this.$route.query.app));
      } else {
        this.selectedApp = this.allApps[0];
      }
    } else {
      // create watcher to watch for changes in apps
      let self = this;

      const watcher = this.$store.watch(
        (state) => state.apps,
        (newVal, oldVal) => {
          if (newVal) {
            if (self.$route.query.app !== undefined) {
              self.selectedApp = newVal.find(app => app.id === parseInt(self.$route.query.app));
            } else {
              self.selectedApp = newVal[0];
            }
            watcher();
          }
        }
      );
    }
  },
  watch: {
    selectedApp(newVal) {
      if (newVal !== undefined) {
        this.$store.commit('setSelectedApp', newVal);
        this.addParamsToLocation({ app: newVal.id });

        if (this.selectedApp.has_web === true && this.selectedApp.website_url === null) {
          this.$router.push({ name: 'Setup Notifications', params: { id: this.selectedApp.id } });
        }

        if (this.selectedApp.has_android === true && this.selectedApp.firebase_service_account_file === null) {
          this.$router.push({ name: 'Setup Notifications', params: { id: this.selectedApp.id } });
        }

        if (this.selectedApp.has_ios === true && this.selectedApp.apple_key_file === null) {
          this.$router.push({ name: 'Setup Notifications', params: { id: this.selectedApp.id } });
        }
      }
    }
  },
  methods: {
    clickApp(app) {
      this.selectedApp = app;
      this.dropDownVisible = false;
    },
    createApp() {
      this.$router.push("/onboarding/create");
    },
    focusOutMenu() {
      this.dropDownVisible = false;
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
    }
  }
}
</script>

<style scoped>

.app-list::-webkit-scrollbar {
  width: 6px;               /* width of the entire scrollbar */
  padding: 1px;
}

.app-list::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

.app-list::-webkit-scrollbar-thumb {
  background-color: #eeeeee;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid transparent;  /* creates padding around scroll thumb */
}
</style>