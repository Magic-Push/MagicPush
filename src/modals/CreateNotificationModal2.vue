<template>
  <TransitionRoot as="template" :show="open">
    <Dialog class="relative z-10" @close="$emit('onClose')">
      <div class="fixed inset-0" />

      <div class="fixed inset-0 overflow-hidden">
        <div class="absolute inset-0 overflow-hidden">
          <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10 sm:pl-16">
            <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
              <DialogPanel class="pointer-events-auto w-screen max-w-xl">
                <div class="flex h-full flex-col overflow-hidden bg-white shadow-xl">
                  <div class="flex-1 overflow-y-scroll">
                    <!-- Header -->
                    <div class="bg-gray-50 px-4 py-6 sm:px-6">
                      <div class="flex items-start justify-between space-x-3">
                        <div class="space-y-1">
                          <DialogTitle class="text-base font-semibold leading-6 text-gray-900">
                            {{ showScheduler === true ? 'Schedule notification' : flowId !== undefined ? 'Create notification' : 'Send notification' }}
                          </DialogTitle>
                          <p class="text-sm text-gray-500">
                            {{ showScheduler === true ? 'Schedule a notification to be sent at a specific date & time' : flowId !== undefined ? 'Create a new notification' : 'Send a notification' }}
                          </p>
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

                    <div class="flex flex-1 flex-col justify-between">
                      <div class="divide-y divide-gray-200 px-4 sm:px-6">
                        <div class="space-y-6 pb-5 pt-6">
                          <div>
                            <label for="project-name" class="block text-sm font-medium leading-6 text-gray-900">Name</label>
                            <div class="mt-2">
                              <input v-model="name" type="text" name="project-name" id="project-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
                            </div>
                          </div>
                          <div v-if="showScheduler">
                            <label for="scheduled_at" class="block">
                              <span class="block text-sm font-medium leading-6 text-gray-900">Scheduled at</span>
                              <span class="block text-xs leading-6 text-gray-400">Notification will be send in the user's local time</span>
                            </label>
                            <div class="mt-2">
                              <div class="columns-2">
                                <input v-model="scheduled_at" type="date" name="scheduled_at" id="scheduled_at"
                                       class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 disabled:bg-gray-50"
                                       placeholder="Select a date" required="">
                                <input v-model="scheduled_at_time" type="time" name="scheduled_at_time" id="scheduled_at_time"
                                       class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 disabled:bg-gray-50"
                                       placeholder="Select a time" required="">
                              </div>
                              <div class="flex items-baseline mt-4">
                                <div class="h-4">
                                  <input v-model="repeat" id="repeat" aria-describedby="repeat" type="checkbox"
                                         class="w-4 h-4 border border-gray-300 rounded bg-gray-50 checked:bg-primary-500 focus:ring-3 focus:ring-primary-300">
                                </div>
                                <div class="ml-3 text-sm">
                                  <label for="repeat" class="text-gray-500">Repeat notification</label>
                                </div>
                                <div class="ml-3">
                                  <select :disabled="!repeat" v-model="repeat_interval" id="repeat" name="repeat"
                                          class="rounded-lg border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600">
                                    <option value="daily">Daily</option>
                                    <option value="weekly">Weekly</option>
                                    <option value="monthly">Monthly</option>
                                    <option value="yearly">Yearly</option>
                                  </select>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div>
                            <span class="block text-sm font-medium leading-6 text-gray-900">Translations</span>
                            <div class="flex flex-col space-y-2 mt-4" v-for="translation in translations" :key="translation.language">
                              <div class="rounded-lg bg-gray-50 p-2 text-gray-600 w-full text-xs font-medium cursor-pointer" @click="expandLanguage(translation.language)">
                                {{ getLanguageName(translation.language) }}
                                {{ translation.language === 'en' ? '(Default)' : '' }}
                                <span class="text-right">
                                  <ChevronDownIcon :ref="'chevron-' + translation.language" class="h-4 w-4 inline-block text-right" :class="translation.language === 'en' ? 'rotate-180': ''" />
                                </span>
                              </div>
                              <div :ref="'language-' + translation.language" :style="translation.language === 'en' ? 'display: block;' : 'display: none;'">
                                <div class="flex flex-col space-y-2 px-2">
                                  <label for="title" class="block mb-1 text-sm font-medium text-gray-900">Title</label>
                                  <input v-model="translation.title" type="text" name="title" id="title"
                                         class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                                         placeholder="Notification title" required="">
                                </div>
                                <div class="flex flex-col space-y-2 px-2 mt-2">
                                  <label for="message" class="block mb-1 text-sm font-medium text-gray-900">Message</label>
                                  <textarea v-model="translation.message" name="message" id="message"
                                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                                            placeholder="Notification message" required=""></textarea>
                                </div>
                                <div class="flex flex-col space-y-2 px-2 mt-2">
                                  <label for="image" class="block mb-1 text-sm font-medium text-gray-900">Image</label>
                                  <FileDrop v-model="translation.image" v-bind:id="translation.language"
                                            v-bind:fileType="'image'" v-bind:uploadUrl="`/api/v1/notifications/${currentApp.id}/image`"/>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div>
                            <label for="project-name" class="block text-sm font-medium leading-6 text-gray-900">Action</label>
                            <div class="mt-2">
                              <input v-model="action" type="text" name="project-name" id="project-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Action buttons -->
                  <div class="flex-shrink-0 border-gray-200 bg-gray-100 justify-between p-4">
                    <button @click="saveDraft" style="width: 27%; margin-right: 3%;"
                            class="text-gray-600 bg-gray-300 hover:bg-gray-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-block">
                      Save draft
                    </button>
                    <button @click="publishNotification" style="width: 70%"
                            class="text-white bg-primary-600 hover:bg-primary-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-block">
                      Save & Publish
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
import FileDrop from "@/components/FileDrop.vue";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';

export default {
  name: "CreateNotificationModal2",
  components: {
    FileDrop,
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    XMarkIcon,
    ChevronDownIcon
  },
  props: ['open', 'flowId', 'parentId', 'eventId', 'showScheduler', 'selectedNotification', 'selectedDate',
    'selectedFlowEvent'],
  data() {
    return {
      name: null,
      default_title: null,
      default_message: null,
      default_image: null,
      scheduled_at: null,
      scheduled_at_time: null,
      repeat: false,
      repeat_interval: "monthly",
      translations: [],
      action: null,
      notification: null,
    }
  },
  mounted() {
    // populate translations with the languages that are supported
    let self = this;
    if (this.selectedNotification) {
      this.name = this.selectedNotification.name;

      if (this.scheduled_at) {
        this.scheduled_at = this.scheduled_at.split('T')[0];
        this.scheduled_at_time = this.scheduled_at.split('T')[1].split('.')[0];
      }

      this.repeat = this.selectedNotification.repeat;
      this.repeat_interval = this.selectedNotification.repeat_interval;
      this.action = this.selectedNotification.action;
    }

    if (this.selectedDate) {
      this.scheduled_at = this.selectedDate;
    }

    if (this.selectedFlowEvent) {
      let notification = this.selectedFlowEvent['notification'];

      this.name = notification.name;
      if (notification.scheduled_at) {
        this.scheduled_at = notification.scheduled_at.split('T')[0];
        this.scheduled_at_time = notification.scheduled_at.split('T')[1].split('.')[0];
      }
      this.repeat = notification.repeat;
      this.repeat_interval = notification.repeat_interval;
      this.action = notification.action;

      this.translations.forEach((translation) => {
        console.log(translation.language)
        if (translation.language === 'en') {
          translation.title = notification.default_title;
          translation.message = notification.default_message;
          translation.image = notification.image;
        } else {
          let existingTranslation = notification.translations.find(ts => ts.language === translation.language);

          if (existingTranslation) {
            translation.title = existingTranslation.title;
            translation.message = existingTranslation.message;
            translation.image = existingTranslation.image;
          }
        }
      });

      this.notification = notification;
    }

    if (this.currentApp) {
      this.currentApp.languages.forEach((language) => {
        let title;
        let message;
        let image;
        if (self.selectedNotification) {
          if (language === 'en') {
            title = self.selectedNotification.default_title;
            message = self.selectedNotification.default_message;
            image = self.selectedNotification.image;
          } else {
            let translation = self.selectedNotification.translations.find(translation => translation.language === language);

            if (translation) {
              title = translation.title;
              message = translation.message;
              image = translation.image;
            }
          }
        }

        self.translations.push({
          language: language,
          title: title,
          message: message,
          image: image
        });
      });
      this.action = this.currentApp.website_url;
    } else {
      const watcher = this.$store.watch(
          (state) => state.currentApp,
          (currentApp) => {
            if (currentApp !== null) {
              currentApp.languages.forEach((language) => {
                let title;
                let message;
                let image;
                if (self.selectedNotification) {
                  if (language === 'en') {
                    title = self.selectedNotification.default_title;
                    message = self.selectedNotification.default_message;
                    image = self.selectedNotification.image;
                  } else {
                    let translation = self.selectedNotification.translations.find(translation => translation.language === language);

                    if (translation) {
                      title = translation.title;
                      message = translation.message;
                      image = translation.image;
                    }
                  }
                }

                self.translations.push({
                  language: language,
                  title: title,
                  message: message,
                  image: image
                });
              })
              self.action = currentApp.website_url;
              watcher();
            }
          }
      );
    }
  },
  watch: {
    selectedFlowEvent(newVal) {
      if (newVal) {
        let notification = newVal['notification'];

        this.name = notification.name;
        if (notification.scheduled_at) {
          this.scheduled_at = notification.scheduled_at.split('T')[0];
          this.scheduled_at_time = notification.scheduled_at.split('T')[1].split('.')[0];
        }
        this.repeat = notification.repeat;
        this.repeat_interval = notification.repeat_interval;
        this.action = notification.action;

        this.translations.forEach((translation) => {
          console.log(translation.language)
          if (translation.language === 'en') {
            translation.title = notification.default_title;
            translation.message = notification.default_message;
            translation.image = notification.image;
          } else {
            let existingTranslation = notification.translations.find(ts => ts.language === translation.language);

            if (existingTranslation) {
              translation.title = existingTranslation.title;
              translation.message = existingTranslation.message;
              translation.image = existingTranslation.image;
            }
          }
        });

        this.notification = notification;
      } else {
        this.name = null;
        this.scheduled_at = null;
        this.scheduled_at_time = null;
        this.repeat = false;
        this.repeat_interval = "monthly";
        this.action = null;
        this.translations.forEach((translation) => {
          translation.title = null;
          translation.message = null;
          translation.image = null;
        })

        this.notification = null;
      }
    },
    selectedNotification(newVal) {
      if (newVal !== null) {
        this.name = newVal.name;
        if (newVal.scheduled_at) {
          this.scheduled_at = newVal.scheduled_at.split('T')[0];
          this.scheduled_at_time = newVal.scheduled_at.split('T')[1].split('.')[0];
        }
        this.repeat = newVal.repeat;
        this.repeat_interval = newVal.repeat_interval;
        this.action = newVal.action;

        this.translations.forEach((translation) => {
          console.log(translation.language)
          if (translation.language === 'en') {
            translation.title = newVal.default_title;
            translation.message = newVal.default_message;
            translation.image = newVal.image;
          } else {
            let existingTranslation = this.selectedNotification.translations.find(ts => ts.language === translation.language);

            if (existingTranslation) {
              translation.title = existingTranslation.title;
              translation.message = existingTranslation.message;
              translation.image = existingTranslation.image;
            }
          }
        });

        this.notification = newVal;
      } else {
        this.name = null;
        this.scheduled_at = null;
        this.scheduled_at_time = null;
        this.repeat = false;
        this.repeat_interval = "monthly";
        this.action = null;
        this.translations.forEach((translation) => {
          translation.title = null;
          translation.message = null;
          translation.image = null;
        })

        this.notification = null;
      }
    },
    selectedDate(newVal) {
      if (newVal !== null) {
        this.scheduled_at = newVal;
      }
    }
  },
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  methods: {
    expandLanguage(language) {
      let element = this.$refs['language-' + language][0];
      let chevron = this.$refs['chevron-' + language][0];
      if (element.style.display === 'none') {
        element.style.display = 'block';
        chevron.classList.add('rotate-180');
      } else {
        element.style.display = 'none';
        chevron.classList.remove('rotate-180');
      }
    },
    fileUploaded(language, imageId) {
      console.log(imageId);
      console.log(language);
      let translation = this.translations.find(translation => translation.language === language);
      translation.image = imageId;
    },
    saveDraft() {
      let self = this;

      let notification = {
        name: this.name,
        repeat: this.repeat,
        repeat_interval: this.repeat_interval,
        translations: this.translations,
        action: this.action
      };

      if (this.scheduled_at) {
        notification['scheduled_at'] = this.scheduled_at + "T" + this.scheduled_at_time;
      }

      if (this.notification['id']) {
        notification['id'] = this.notification['id'];
        this.$store.dispatch('updateNotification', notification)
            .then((res) => {
              if (self.flowId) {
                self.updateFlowInStore(res.data.id);
              } else {
                self.$emit('onClose');
              }
            })
            .catch((error) => {
              console.log(error);
            });
      } else {
        this.$store.dispatch('createNotification', notification)
            .then((res) => {
              if (self.flowId) {
                self.updateFlowInStore(res.data.id);
              } else {
                self.$emit('onClose');
              }
            })
            .catch((error) => {
              console.log(error);
            });
      }
    },
    publishNotification() {
      let self = this;

      let notification = {
        name: this.name,
        repeat: this.repeat,
        repeat_interval: this.repeat_interval,
        translations: this.translations,
        sent: this.flowId === undefined,
        live: this.flowId !== undefined,
        action: this.action
      };

      if (this.scheduled_at) {
        notification['scheduled_at'] = this.scheduled_at + "T" + this.scheduled_at_time;
      }

      if (this.notification && this.notification['id']) {
        notification['id'] = this.notification['id'];
        this.$store.dispatch('updateNotification', notification)
            .then((res) => {
              if (self.flowId) {
                self.updateFlowInStore(res.data.id);
              } else {
                self.$emit('onClose');
              }
            })
            .catch((error) => {
              console.log(error);
            });
      } else {
        this.$store.dispatch('createNotification', notification)
            .then((res) => {
              if (self.flowId) {
                self.updateFlowInStore(res.data.id);
              } else {
                self.$emit('onClose');
              }
            })
            .catch((error) => {
              console.log(error);
            });
      }
    },
    getLanguageName(code) {
      return new Intl.DisplayNames([code], {type: 'language'}).of(code);
    },
    getFlag(code) {
      code = new Intl.Locale(code).region;
      const flags = {
        'AD': '🇦🇩', 'AE': '🇦🇪', 'AF': '🇦🇫', 'AG': '🇦🇬', 'AI': '🇦🇮',
        'AL': '🇦🇱', 'AM': '🇦🇲', 'AO': '🇦🇴', 'AQ': '🇦🇶', 'AR': '🇦🇷',
        'AS': '🇦🇸', 'AT': '🇦🇹', 'AU': '🇦🇺', 'AW': '🇦🇼', 'AX': '🇦🇽',
        'AZ': '🇦🇿', 'BA': '🇧🇦', 'BB': '🇧🇧', 'BD': '🇧🇩', 'BE': '🇧🇪',
        'BF': '🇧🇫', 'BG': '🇧🇬', 'BH': '🇧🇭', 'BI': '🇧🇮', 'BJ': '🇧🇯',
        'BL': '🇧🇱', 'BM': '🇧🇲', 'BN': '🇧🇳', 'BO': '🇧🇴', 'BQ': '🇧🇶',
        'BR': '🇧🇷', 'BS': '🇧🇸', 'BT': '🇧🇹', 'BV': '🇧🇻', 'BW': '🇧🇼',
        'BY': '🇧🇾', 'BZ': '🇧🇿', 'CA': '🇨🇦', 'CC': '🇨🇨', 'CD': '🇨🇩',
        'CF': '🇨🇫', 'CG': '🇨🇬', 'CH': '🇨🇭', 'CI': '🇨🇮', 'CK': '🇨🇰',
        'CL': '🇨🇱', 'CM': '🇨🇲', 'CN': '🇨🇳', 'CO': '🇨🇴', 'CR': '🇨🇷',
        'CU': '🇨🇺', 'CV': '🇨🇻', 'CW': '🇨🇼', 'CX': '🇨🇽', 'CY': '🇨🇾',
        'CZ': '🇨🇿', 'DE': '🇩🇪', 'DJ': '🇩🇯', 'DK': '🇩🇰', 'DM': '🇩🇲',
        'DO': '🇩🇴', 'DZ': '🇩🇿', 'EC': '🇪🇨', 'EE': '🇪🇪', 'EG': '🇪🇬',
        'EH': '🇪🇭', 'ER': '🇪🇷', 'ES': '🇪🇸', 'ET': '🇪🇹', 'FI': '🇫🇮',
        'FJ': '🇫🇯', 'FK': '🇫🇰', 'FM': '🇫🇲', 'FO': '🇫🇴', 'FR': '🇫🇷',
        'GA': '🇬🇦', 'GB': '🇬🇧', 'GD': '🇬🇩', 'GE': '🇬🇪', 'GF': '🇬🇫',
        'GG': '🇬🇬', 'GH': '🇬🇭', 'GI': '🇬🇮', 'GL': '🇬🇱', 'GM': '🇬🇲',
        'GN': '🇬🇳', 'GP': '🇬🇵', 'GQ': '🇬🇶', 'GR': '🇬🇷', 'GS': '🇬🇸',
        'GT': '🇬🇹', 'GU': '🇬🇺', 'GW': '🇬🇼', 'GY': '🇬🇾', 'HK': '🇭🇰',
        'HM': '🇭🇲', 'HN': '🇭🇳', 'HR': '🇭🇷', 'HT': '🇭🇹', 'HU': '🇭🇺',
        'ID': '🇮🇩', 'IE': '🇮🇪', 'IL': '🇮🇱', 'IM': '🇮🇲', 'IN': '🇮🇳',
        'IO': '🇮🇴', 'IQ': '🇮🇶', 'IR': '🇮🇷', 'IS': '🇮🇸', 'IT': '🇮🇹',
        'JE': '🇯🇪', 'JM': '🇯🇲', 'JO': '🇯🇴', 'JP': '🇯🇵', 'KE': '🇰🇪',
        'KG': '🇰🇬', 'KH': '🇰🇭', 'KI': '🇰🇮', 'KM': '🇰🇲', 'KN': '🇰🇳',
        'KP': '🇰🇵', 'KR': '🇰🇷', 'KW': '🇰🇼', 'KY': '🇰🇾', 'KZ': '🇰🇿',
        'LA': '🇱🇦', 'LB': '🇱🇧', 'LC': '🇱🇨', 'LI': '🇱🇮', 'LK': '🇱🇰',
        'LR': '🇱🇷', 'LS': '🇱🇸', 'LT': '🇱🇹', 'LU': '🇱🇺', 'LV': '🇱🇻',
        'LY': '🇱🇾', 'MA': '🇲🇦', 'MC': '🇲🇨', 'MD': '🇲🇩', 'ME': '🇲🇪',
        'MF': '🇲🇫', 'MG': '🇲🇬', 'MH': '🇲🇭', 'MK': '🇲🇰', 'ML': '🇲🇱',
        'MM': '🇲🇲', 'MN': '🇲🇳', 'MO': '🇲🇴', 'MP': '🇲🇵', 'MQ': '🇲🇶',
        'MR': '🇲🇷', 'MS': '🇲🇸', 'MT': '🇲🇹', 'MU': '🇲🇺', 'MV': '🇲🇻',
        'MW': '🇲🇼', 'MX': '🇲🇽', 'MY': '🇲🇾', 'MZ': '🇲🇿', 'NA': '🇳🇦',
        'NC': '🇳🇨', 'NE': '🇳🇪', 'NF': '🇳🇫', 'NG': '🇳🇬', 'NI': '🇳🇮',
        'NL': '🇳🇱', 'NO': '🇳🇴', 'NP': '🇳🇵', 'NR': '🇳🇷', 'NU': '🇳🇺',
        'NZ': '🇳🇿', 'OM': '🇴🇲', 'PA': '🇵🇦', 'PE': '🇵🇪', 'PF': '🇵🇫',
        'PG': '🇵🇬', 'PH': '🇵🇭', 'PK': '🇵🇰', 'PL': '🇵🇱', 'PM': '🇵🇲',
        'PN': '🇵🇳', 'PR': '🇵🇷', 'PS': '🇵🇸', 'PT': '🇵🇹', 'PW': '🇵🇼',
        'PY': '🇵🇾', 'QA': '🇶🇦', 'RE': '🇷🇪', 'RO': '🇷🇴', 'RS': '🇷🇸',
        'RU': '🇷🇺', 'RW': '🇷🇼', 'SA': '🇸🇦', 'SB': '🇸🇧', 'SC': '🇸🇨',
        'SD': '🇸🇩', 'SE': '🇸🇪', 'SG': '🇸🇬', 'SH': '🇸🇭', 'SI': '🇸🇮',
        'SJ': '🇸🇯', 'SK': '🇸🇰', 'SL': '🇸🇱', 'SM': '🇸🇲', 'SN': '🇸🇳',
        'SO': '🇸🇴', 'SR': '🇸🇷', 'SS': '🇸🇸', 'ST': '🇸🇹', 'SV': '🇸🇻',
        'SX': '🇸🇽', 'SY': '🇸🇾', 'SZ': '🇸🇿', 'TC': '🇹🇨', 'TD': '🇹🇩',
        'TF': '🇹🇫', 'TG': '🇹🇬', 'TH': '🇹🇭', 'TJ': '🇹🇯', 'TK': '🇹🇰',
        'TL': '🇹🇱', 'TM': '🇹🇲', 'TN': '🇹🇳', 'TO': '🇹🇴', 'TR': '🇹🇷',
        'TT': '🇹🇹', 'TV': '🇹🇻', 'TW': '🇹🇼', 'TZ': '🇹🇿', 'UA': '🇺🇦',
        'UG': '🇺🇬', 'UM': '🇺🇲', 'US': '🇺🇸', 'UY': '🇺🇾', 'UZ': '🇺🇿',
        'VA': '🇻🇦', 'VC': '🇻🇨', 'VE': '🇻🇪', 'VG': '🇻🇬', 'VI': '🇻🇮',
        'VN': '🇻🇳', 'VU': '🇻🇺', 'WF': '🇼🇫', 'WS': '🇼🇸', 'XK': '🇽🇰',
        'YE': '🇾🇪', 'YT': '🇾🇹', 'ZA': '🇿🇦', 'ZM': '🇿🇲', 'ZW': '🇿🇼'
      };
      code = code.toUpperCase();
      return flags[code] || '🏳';
    },
    getLanguageByCountryCode(languageCode) {
      const countryLanguageMap = {
        'AD': 'ca', // Andorra -> Catalan
        'AE': 'ar', // United Arab Emirates -> Arabic
        'AF': 'fa', // Afghanistan -> Dari/Pashto
        'AG': 'en', // Antigua and Barbuda -> English
        'AI': 'en', // Anguilla -> English
        'AL': 'sq', // Albania -> Albanian
        'AM': 'hy', // Armenia -> Armenian
        'AO': 'pt', // Angola -> Portuguese
        'AQ': 'en', // Antarctica -> English (scientific community)
        'AR': 'es', // Argentina -> Spanish
        'AS': 'en', // American Samoa -> English
        'AT': 'de', // Austria -> German
        'AU': 'en', // Australia -> English
        'AW': 'nl', // Aruba -> Dutch
        'AX': 'sv', // Åland Islands -> Swedish
        'AZ': 'az', // Azerbaijan -> Azerbaijani
        'BA': 'bs', // Bosnia and Herzegovina -> Bosnian
        'BB': 'en', // Barbados -> English
        'BD': 'bn', // Bangladesh -> Bengali
        'BE': 'nl', // Belgium -> Dutch
        'BF': 'fr', // Burkina Faso -> French
        'BG': 'bg', // Bulgaria -> Bulgarian
        'BH': 'ar', // Bahrain -> Arabic
        'BI': 'fr', // Burundi -> French
        'BJ': 'fr', // Benin -> French
        'BL': 'fr', // Saint Barthélemy -> French
        'BM': 'en', // Bermuda -> English
        'BN': 'ms', // Brunei -> Malay
        'BO': 'es', // Bolivia -> Spanish
        'BQ': 'nl', // Caribbean Netherlands -> Dutch
        'BR': 'pt', // Brazil -> Portuguese
        'BS': 'en', // Bahamas -> English
        'BT': 'dz', // Bhutan -> Dzongkha
        'BV': 'no', // Bouvet Island -> Norwegian
        'BW': 'en', // Botswana -> English
        'BY': 'be', // Belarus -> Belarusian
        'BZ': 'en', // Belize -> English
        'CA': 'en', // Canada -> English/French
        'CC': 'en', // Cocos (Keeling) Islands -> English
        'CD': 'fr', // Congo (DRC) -> French
        'CF': 'fr', // Central African Republic -> French
        'CG': 'fr', // Congo (Republic) -> French
        'CH': 'de', // Switzerland -> German/French/Italian
        'CI': 'fr', // Côte d’Ivoire -> French
        'CK': 'en', // Cook Islands -> English
        'CL': 'es', // Chile -> Spanish
        'CM': 'fr', // Cameroon -> French/English
        'CN': 'zh', // China -> Mandarin
        'CO': 'es', // Colombia -> Spanish
        'CR': 'es', // Costa Rica -> Spanish
        'CU': 'es', // Cuba -> Spanish
        'CV': 'pt', // Cabo Verde -> Portuguese
        'CW': 'nl', // Curaçao -> Dutch
        'CX': 'en', // Christmas Island -> English
        'CY': 'el', // Cyprus -> Greek
        'CZ': 'cs', // Czech Republic -> Czech
        // ...continuing with the rest of the countries
      };

      return this.filterByValue(countryLanguageMap, languageCode) || 'Unknown';
    },
    filterByValue (object, filterValue) {
      const filteredKeys = Object.keys(object).filter(key => object[key] === filterValue);
      const filteredObject = null;
      filteredKeys.forEach(key => {
        filteredObject[key] = object[key];
      });
      return filteredObject;
    },
    updateFlowInStore(notification_id) {
      let flowData = {
        id: this.flowId,
        events: [
          {
            type: 'Notification',
            notification_id: notification_id
          }
        ],
      }
      if (this.parentId) {
        flowData['events'][0]['parent_id'] = this.parentId;
      }

      if (this.selectedFlowEvent) {
        flowData['events'][0]['id'] = this.selectedFlowEvent.id;
      }
      this.$store.dispatch('updateFlow', flowData)
          .then((res) => {
            this.$emit('onUpdate', res.data);
            this.$emit('onClose');
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