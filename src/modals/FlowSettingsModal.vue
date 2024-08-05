<template>
  <TransitionRoot as="template" :show="open">
    <Dialog class="relative z-10" @close="$emit('onClose')">
      <div class="fixed inset-0" />

      <div class="fixed inset-0 overflow-hidden">
        <div class="absolute inset-0 overflow-hidden">
          <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10 sm:pl-16">
            <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
              <DialogPanel class="pointer-events-auto w-screen max-w-xl">
                <div class="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
                  <div class="flex-1">
                    <!-- Header -->
                    <div class="bg-gray-50 px-4 py-6 sm:px-6">
                      <div class="flex items-start justify-between space-x-3">
                        <div class="space-y-1">
                          <DialogTitle class="text-base font-semibold leading-6 text-gray-900">Flow settings.</DialogTitle>
                          <p class="text-sm text-gray-500">Add a delay to the flow.</p>
                        </div>
                        <div class="flex h-7 items-center">
                          <button type="button" class="relative text-gray-400 hover:text-gray-500" @click="$emit('onClose')">
                            <span class="absolute -inset-2.5" />
                            <span class="sr-only">Close panel</span>
                            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Divider container -->
                    <div class="space-y-6 py-6 sm:space-y-0 sm:divide-y sm:divide-gray-200 sm:py-0">
                      <!-- Project name -->
                      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                        <div>
                          <label for="project-name" class="block text-sm font-medium leading-6 text-gray-900 sm:mt-1.5">Duration</label>
                        </div>
                        <div class="sm:col-span-2 flex justify-between">
                          <input v-model="duration" type="text" name="project-name" id="project-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                          <select v-model="unit" id="repeat" name="repeat"
                                  class="ml-4 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                            <option value="seconds">Seconds</option>
                            <option value="minutes">Minutes</option>
                            <option value="hours">Hours</option>
                            <option value="days">Days</option>
                            <option value="weeks">Weeks</option>
                            <option value="months">Months</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Action buttons -->
                  <div class="flex-shrink-0 border-gray-200 bg-gray-100 justify-between p-4">
                    <button @click="$emit('onClose')" style="width: 27%; margin-right: 3%;"
                            class="text-gray-600 bg-gray-300 hover:bg-gray-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-block">
                      Cancel
                    </button>
                    <button @click="addEvent" style="width: 70%"
                            class="text-white bg-primary-600 hover:bg-primary-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-block">
                      Add
                    </button>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import { XMarkIcon } from '@heroicons/vue/24/outline';
import { LinkIcon, PlusIcon, QuestionMarkCircleIcon, } from '@heroicons/vue/20/solid';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';

export default {
  name: "AddDelayModal",
  components: {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    XMarkIcon
  },
  props: ['open', 'flowId', 'parentId', 'eventId'],
  data() {
    return {
      duration: 0,
      unit: 'seconds'
    }
  },
  methods: {
    addEvent() {
      let flowData = {
        id: this.flowId,
        events: [
          {
            type: 'Delay',
            delay: this.duration,
            delay_unit: this.unit
          }
        ],
      }
      if (this.parentId) {
        flowData['events'][0]['parent_id'] = this.parentId;
      }

      let self = this;
      this.$store.dispatch('updateFlow', flowData)
          .then((res) => {
            self.$emit('onUpdate', res.data);
            self.$emit('onClose');
          })
          .catch((err) => {
            alert('Error adding delay, please try again');
          });
    }
  }
}
</script>

<style scoped>

</style>