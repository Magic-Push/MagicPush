<template>
  <div class="border-gray-100" style="border-left-style: solid; border-left-width: 0px;">
    <div class="flex flex-col h-screen p-4">
      <div class="flex w-full flex items-center">
        <div class="pb-4">
          <h1 class="font-medium text-xl text-slate-900">
            Flows
          </h1>
        </div>

        <div class="absolute right-4 top-4 flex items-center" v-if="enabled">
          <button @click="createFlow"
                  class="rounded-md w-full bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
            New flow
          </button>
        </div>
      </div>

      <div class="flex-1 w-full container" v-if="enabled">
        <ul v-if="getFlows.length > 0" role="list" class="divide-y divide-gray-100">
          <li v-for="flow in getFlows" :key="flow.id" class="flex items-center justify-between gap-x-6 py-5">
            <div @click="openFlow(flow)" class="min-w-0 cursor-pointer">
              <div class="flex items-start gap-x-3">
                <p class="text-sm font-semibold leading-6 text-gray-900">{{ flow.name }}</p>
                <p :class="[statuses[flow.enabled ? 'Enabled' : 'Disabled'], 'rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset']">
                  {{ flow.enabled ? 'Enabled' : 'Disabled' }}
                </p>
              </div>
              <div class="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
                <p class="whitespace-nowrap">
                  For event {{ flow.event }}
                </p>
                <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 fill-current">
                  <circle cx="1" cy="1" r="1" />
                </svg>
                <p class="truncate">
                  Created at <time :datetime="flow.created_at">{{ flow.created_at }}</time>
                </p>
              </div>
            </div>
            <div class="flex flex-none items-center gap-x-4">
              <button @click="openFlow(flow)" class="cursor-pointer hidden rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:block">
                Open flow editor
              </button>
              <Menu as="div" class="relative flex-none">
                <MenuButton class="-m-2.5 block p-2.5 text-gray-500 hover:text-gray-900">
                  <span class="sr-only">Open options</span>
                  <EllipsisVerticalIcon class="h-5 w-5" aria-hidden="true" />
                </MenuButton>
                <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                  <MenuItems class="absolute right-0 z-10 mt-2 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                    <MenuItem v-slot="{ active }">
                      <button class="w-full text-left" @click="enableFlow(flow)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                        {{ flow.enabled ? 'Disable' : 'Enable' }}
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <button class="w-full text-left" @click="editFlow(flow)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                        Edit
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <button class="w-full text-left" @click="deleteFlow(flow)" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                        Delete
                      </button>
                    </MenuItem>
                  </MenuItems>
                </transition>
              </Menu>
            </div>
          </li>
        </ul>
        <div v-else class="text-center mx-auto" style="margin-top: 20%;">
          <span class="text-lg font-semibold text-gray-700 block">Create your first flow</span>
          <span class="text-sm font-sans text-gray-400 block mt-2 mb-6">Start with automating your push notifications</span>
          <button @click="createFlow"
                  class="rounded-md bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
            New flow
          </button>
        </div>
      </div>
      <div class="flex-1 w-full container" v-else>
        <div class="overflow-hidden bg-white py-24 sm:py-32">
          <div class="mx-auto max-w-7xl px-6 lg:px-8">
            <div class="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 sm:gap-y-20 lg:mx-0 lg:max-w-none lg:grid-cols-2">
              <div class="lg:ml-auto lg:pl-4 lg:pt-4">
                <div class="lg:max-w-lg">
                  <h2 class="text-base font-medium leading-7 text-primary-500">Coming soon</h2>
                  <p class="mt-2 text-3xl font-semibold tracking-tight text-gray-800 sm:text-4xl">MagicPush Flows</p>
                  <p class="mt-6 text-lg leading-8 text-gray-500">
                    A powerful way to automate & personalize your push notifications. Create flows that trigger based on events. Add delays, true/false conditions, A/B tests and more.
                  </p>
                  <button @click="$magicpush.toggleModal()" class="rounded-md bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 mt-6">
                    Get Notified
                  </button>
                </div>
              </div>
              <div class="flex items-start justify-end lg:order-first">
                <img src="/images/flows.png" alt="Product screenshot" class="w-[48rem] max-w-none rounded-xl ring-1 ring-gray-400/10 sm:w-[57rem]" width="2432" height="1442" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CreateFlowModal v-bind:open="showModal" v-bind:selectedFlow="selectedFlow" v-on:onClose="closeModal" />
  </div>
</template>

<script>
import CreateFlowModal from "@/modals/CreateFlowModal.vue";
import { EllipsisVerticalIcon } from '@heroicons/vue/20/solid';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';

export default {
  name: "FlowsPage",
  components: {CreateFlowModal, EllipsisVerticalIcon, Menu, MenuButton, MenuItem, MenuItems},
  data() {
    return {
      statuses: {
        Enabled: 'text-green-700 bg-green-50 ring-green-600/20',
        Disabled: 'text-gray-600 bg-gray-50 ring-gray-500/10'
      },
      flows: [],
      showModal: false,
      selectedFlow: null,
      enabled: true
    }
  },
  mounted() {
    this.loadFlows();
  },
  computed: {
    getFlows() {
      return this.$store.state.flowsData;
    },
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  watch: {
    currentApp: {
      handler: function (newVal, oldVal) {
        if (newVal) {
          this.loadFlows();
        }
      },
      deep: true
    }
  },
  methods: {
    loadFlows() {
      this.$store.dispatch('getFlows')
          .then((res) => {

          })
          .catch((err) => {
            console.error(err);
          });
    },
    closeModal() {
      this.showModal = false;
      this.selectedFlow = null;

      this.loadFlows();
    },
    createFlow() {
      this.showModal = true;
    },
    openFlow(flow) {
      this.$router.push('/builder/' + flow.id);
    },
    enableFlow(flow) {
      flow['enabled'] = !flow['enabled'];

      let self = this;
      this.$store.dispatch('updateFlow', flow)
          .then((res) => {
            self.loadFlows();
          })
          .catch((err) => {
            console.error(err);
          });
    },
    editFlow(flow) {
      this.selectedFlow = flow;
      this.showModal = true;
    },
    deleteFlow(flow) {
      let self = this;
      this.$store.dispatch('deleteFlow', flow)
          .then((res) => {
            self.loadFlows();
          })
          .catch((err) => {
            console.error(err);
          });
    }
  }
}
</script>

<style scoped>

</style>