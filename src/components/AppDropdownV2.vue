<template>
  <Listbox as="div" v-model="selectedApp">
    <div class="relative mb-5">
      <ListboxButton class="relative w-full cursor-default rounded-md bg-white py-2 pl-3.5 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
        <span class="block truncate">{{ selectedApp ? selectedApp.name : 'Loading...' }}</span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div class="absolute z-10 mt-1 w-full bg-white rounded-md">
          <div class="app-list max-h-60 overflow-auto rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <ListboxOptions class="py-1 text-base sm:text-sm">
              <ListboxOption as="template" v-for="app in allApps" :key="app.id" :value="app.name" v-slot="{ active, selected }">
                <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                  <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ app.name }}</span>
                </li>
              </ListboxOption>
            </ListboxOptions>
          </div>
          <a @click="createApp" href="#" class="flex items-center p-3 text-sm font-medium text-primary-600 border-t border-gray-200 rounded-b-md bg-gray-50 hover:bg-gray-100 hover:underline">
            <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7 7V5"/>
            </svg>
            Create new app
          </a>
        </div>
      </transition>
    </div>
  </Listbox>
</template>

<script>
import { ChevronUpDownIcon } from '@heroicons/vue/20/solid';
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue';

export default {
  name: "AppDropdownV2",
  components: { ChevronUpDownIcon, Listbox, ListboxButton, ListboxOption, ListboxOptions },
  data() {
    return {
      selectedApp: null
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
  watch: {
    selectedApp: {
      handler: function (newVal) {
        this.$emit('appSelected', newVal);
      }
    }
  },
  mounted() {
    if (this.allApps !== null) {
      this.selectedApp = this.allApps[0];
    } else {
      // create watcher to watch for changes in apps
      let self = this;

      const watcher = this.$store.watch(
          (state) => state.apps,
          (newVal, oldVal) => {
            self.selectedApp = newVal[0];
            watcher();
          }
      );
    }
  },
  methods: {
    createApp() {
      this.$router.push("/onboarding/create");
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