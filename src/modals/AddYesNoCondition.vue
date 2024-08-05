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
                          <DialogTitle class="text-base font-semibold leading-6 text-gray-900">New Yes/No condition.</DialogTitle>
                          <p class="text-sm text-gray-500">Add a new Yes/No split branch to the flow.</p>
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

                    <div class="space-y-6 py-6 sm:space-y-0 sm:divide-y sm:divide-gray-200 sm:py-0">
                      <!-- Key -->
                      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                        <div>
                          <label for="key" class="block text-sm font-medium leading-6 text-gray-900 sm:mt-1.5">Key</label>
                        </div>
                        <div class="sm:col-span-2">
                          <div class="relative ring-1 ring-gray-300 rounded-md shadow-sm z-10">
                            <input v-if="key === 'New key'" type="text" name="newKey" id="newKey" ref="newKey"
                                   class="absolute w-1/2 rounded-md border-0 py-1 m-0.5 mr-5 text-gray-900 ring-0 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                                   placeholder="new key name..."
                                   style="text-transform: lowercase;"
                                   required="">
                            <select v-model="key" id="key" name="key"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-0 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-0 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6">
                              <option v-for="mKey in appUserKeys" :key="mKey.name" :value="mKey.name">{{ mKey.name }}</option>
                            </select>
                          </div>
                          <div v-if="key === 'New key'" class="relative ring-1 ring-gray-300 rounded-md shadow-sm mt-2">
                            <select v-model="keyType" id="key" name="key"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-0 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-0 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6">
                              <option v-for="type in keyTypes" :key="type" :value="type">{{ type }}</option>
                            </select>
                          </div>
                        </div>
                      </div>

                      <!-- Operator -->
                      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                        <div>
                          <label for="operator" class="block text-sm font-medium leading-6 text-gray-900 sm:mt-1.5">Operator</label>
                        </div>
                        <div class="sm:col-span-2">
                          <select v-model="operator" id="operator" name="operator"
                                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6">
                            <option value="==" selected>Equals</option>
                            <option value="!=">Not equals</option>
                            <option value=">">Greater than</option>
                            <option value=">=">Greater than or equals</option>
                            <option value="<">Less than</option>
                            <option value="<=">Less than or equals</option>
                            <option value="is_null">Is NULL</option>
                            <option value="is_not_null">Is not NULL</option>
                            <option value="is_between">Is between</option>
                            <option value="is_not_between">Is not between</option>
                          </select>
                        </div>
                      </div>

                      <!-- Value -->
                      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                        <div>
                          <label for="value" class="block text -sm font-medium leading-6 text-gray-900 sm:mt-1.5">Value</label>
                        </div>
                        <div class="sm:col-span-2">
                          <select v-if="keyType === 'date'" v-model="valueType" id="key" name="key"
                                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 disabled:bg-gray-50">
                            <option v-for="type in valueTypes" :key="type" :value="type">{{ type }}</option>
                          </select>
                          <template v-if="keyType === 'boolean'">
                            <select v-model="value" id="value" name="value"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 disabled:bg-gray-50">
                              <option value="True">True</option>
                              <option value="False">False</option>
                            </select>
                          </template>
                          <template v-else>
                            <input v-model="value" :disabled="operator === 'is_not_null' || operator === 'is_null'" :type="keyType === 'date' && valueType === 'date' ? 'date' : keyType === 'number' ? 'number' : 'text' " name="value" id="value"
                                   class="block w-full rounded-md border-0 py-1.5 mt-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 disabled:bg-gray-50" />
                          </template>
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
                      {{ selectedFlowEvent ? 'Update' : 'Add' }}
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
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';

export default {
  name: "AddYesNoCondition",
  components: {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    XMarkIcon,
  },
  data() {
    return {
      appUserKeys: [],
      keyTypes: ['text', 'number', 'date', 'boolean'],
      key: null,
      keyType: 'text',
      operator: '==',
      value: null,
      valueType: 'date',
      valueTypes: ['date', 'difference(days, hours, minutes, seconds)']
    }
  },
  props: ['open', 'flowId', 'parentId', 'eventId', 'selectedFlowEvent'],
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  mounted() {
    if (this.currentApp) {
      console.log('Current App:', this.currentApp); // Added log
      this.currentApp.default_keys.forEach((key) => {
        console.log('Pushing default key:', key); // Added log
        this.appUserKeys.push(key);
      });
      this.currentApp.keys.forEach((keyObj) => {
        console.log('Pushing key:', keyObj); // Added log
        this.appUserKeys.push(keyObj);
      });
      this.appUserKeys.push({'name': 'New key', 'type': 'text'});
    } else {
      let self = this;
      const watcher = this.$store.watch(
          (state) => state.currentApp,
          (newVal, oldVal) => {
            if (newVal) {
              console.log('New Current App:', newVal); // Added log
              newVal.default_keys.forEach((key) => {
                console.log('Pushing default key:', key); // Added log
                self.appUserKeys.push(key);
              });
              newVal.keys.forEach((keyObj) => {
                console.log('Pushing key:', keyObj); // Added log
                self.appUserKeys.push(keyObj);
              });
              self.appUserKeys.push({'name': 'New key', 'type': 'text'});
              watcher();
            }
          }
      );
    }

    if (this.selectedFlowEvent) {
      let statement = this.selectedFlowEvent['statement'];
      let key = statement.split(' ')[0];
      let operator = statement.split(' ')[1];
      let value = statement.split(' ')[2];

      this.key = key;
      this.operator = operator;
      this.value = value;
    }
  },
  methods: {
    addEvent() {
      var key = "";
      var statement = "";

      if (this.key === 'New key') {
        key = this.$refs.newKey.value;
      } else {
        key = this.key;
      }

      if (this.operator === 'is_null') {
        statement = `${key} is None`;
      } else if (this.operator === 'is_not_null') {
        statement = `${key} is not None`;
      } else {
        statement = `${key} ${this.operator} ${this.value}`;
      }

      let flowData = {
        id: this.flowId,
        events: [
          {
            type: 'Yes/No condition',
            statement: statement,
            key: { key: key, type: this.keyType },
          }
        ],
      }
      if (this.parentId) {
        flowData['events'][0]['parent_id'] = this.parentId;
      }
      if (this.selectedFlowEvent) {
        flowData['events'][0]['id'] = this.selectedFlowEvent.id;
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
  },
  watch: {
    selectedFlowEvent(newVal) {
      if (newVal) {
        let statement = newVal['statement'];
        let key = statement.split(' ')[0];
        let operator = statement.split(' ')[1];
        let value = statement.split(' ')[2];

        this.key = key;
        this.operator = operator;
        this.value = value;
      }
    },
    key(newVal) {
      if (newVal === 'New key') {
        setTimeout(() => {
          this.$refs.newKey.focus();
        }, 50);
      }
      this.keyType = this.appUserKeys.find((key) => key.name === newVal).type;
      this.valueType = 'date';
    }
  }
}
</script>

<style scoped>

</style>