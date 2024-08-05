<template>
  <TransitionRoot :show="open" as="template" @after-leave="query = ''" appear>
    <Dialog class="relative z-50" @close="$emit('onClose')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-25 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-20 w-screen overflow-y-auto p-4 sm:p-6 md:p-20">
        <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100" leave="ease-in duration-200" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95">
          <DialogPanel class="mx-auto max-w-xl transform divide-y divide-gray-100 overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 transition-all" style="margin-top: 15%;">
            <Combobox @update:modelValue="onSelect">
              <div class="relative" v-if="showSearch">
                <MagnifyingGlassIcon class="pointer-events-none absolute left-4 top-3.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                <ComboboxInput class="h-12 w-full border-0 bg-transparent pl-11 pr-4 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm" placeholder="Search..." @change="query = $event.target.value" @blur="query = ''" />
              </div>

              <ComboboxOptions v-if="filteredItems.length > 0" static class="max-h-96 transform-gpu scroll-py-3 overflow-y-auto p-3">
                <ComboboxOption v-for="item in filteredItems" :key="item.id" :value="item" as="template" v-slot="{ active }">
                  <li :class="['flex cursor-pointer select-none rounded-xl p-3', active && 'bg-gray-100']">
                    <div :class="['flex h-10 w-10 flex-none items-center justify-center rounded-lg', item.color]">
                      <component :is="item.icon" class="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    <div class="ml-4 flex-auto">
                      <p :class="['text-sm font-medium', active ? 'text-gray-900' : 'text-gray-700']">
                        {{ item.name }}
                      </p>
                      <p :class="['text-sm', active ? 'text-gray-700' : 'text-gray-500']">
                        {{ item.description }}
                      </p>
                    </div>
                  </li>
                </ComboboxOption>
              </ComboboxOptions>
            </Combobox>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import {
  Combobox,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption,
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import { PaperAirplaneIcon, ClockIcon, FunnelIcon, MagnifyingGlassIcon, ArrowPathRoundedSquareIcon, XCircleIcon } from '@heroicons/vue/20/solid'

export default {
  name: "AddEventModal",
  components: {
    Combobox,
    ComboboxInput,
    ComboboxOptions,
    ComboboxOption,
    Dialog,
    DialogPanel,
    TransitionChild,
    TransitionRoot,
    PaperAirplaneIcon,
    ClockIcon,
    FunnelIcon,
    MagnifyingGlassIcon,
    ArrowPathRoundedSquareIcon,
    XCircleIcon,
  },
  props: ['open'],
  data() {
    return {
      showSearch: false,
      query: '',
      items: [
        {
          id: 1,
          name: 'Notification',
          description: 'Send a notification to the user',
          color: 'bg-primary-500',
          icon: 'PaperAirplaneIcon',
        },
        {
          id: 2,
          name: 'Delay',
          description: 'Wait for a specified amount of time',
          color: 'bg-blue-500',
          icon: 'ClockIcon',
        },
        {
          id: 3,
          name: 'Yes/No condition',
          description: 'Check user variables',
          color: 'bg-yellow-400',
          icon: 'FunnelIcon',
        },
        {
          id: 4,
          name: 'Loop back',
          description: 'Loop back to a previous event',
          color: 'bg-green-500',
          icon: 'ArrowPathRoundedSquareIcon',
        },
        {
          id: 5,
          name: 'End',
          description: 'End the flow',
          color: 'bg-red-500',
          icon: 'XCircleIcon',
        }
      ],
      filteredItems: []
    }
  },
  mounted() {
    this.filteredItems = this.items;
  },
  methods: {
    onSelect(item) {
      this.$emit('onSelect', item);
    },
  },
  watch: {
    query(newVal) {
      // Filter items based on query

    },
  }
}
</script>

<style scoped>

</style>