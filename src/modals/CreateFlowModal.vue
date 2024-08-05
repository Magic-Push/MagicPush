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
                          <DialogTitle class="text-base font-semibold leading-6 text-gray-900">New flow</DialogTitle>
                          <p class="text-sm text-gray-500">Create a new notification flow</p>
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
                    <div class="space-y-6 py-6 px-6">
                      <!-- Project name -->
                      <div>
                        <label for="eventName" class="block mb-2 text-sm font-medium text-gray-900">Name</label>
                        <div class="mt-2" >
                          <input v-model="name" type="text" name="eventName" id="eventName"
                                 class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                                 required="">
                        </div>
                      </div>
                      <div>
                        <label for="selectEvent" class="block mb-2 text-sm font-medium text-gray-900">Event</label>
                        <div class="relative mt-2 ring-1 ring-gray-300 rounded-md shadow-sm">
                          <input v-if="flowEvent === 'new event'" type="text" name="event" id="event" ref="newEvent"
                                 class="absolute w-1/2 rounded-md border-0 py-1 m-0.5 mr-5 text-gray-900 ring-0 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                                 placeholder="New event"
                                 style="text-transform: lowercase;"
                                 required="">
                          <select v-model="flowEvent" type="text" name="selectEvent" id="selectEvent" ref="selectEvent"
                                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                                  required="">
                            <option v-for="app_event in currentApp.events" :key="app_event.id" :value="app_event.name">{{ app_event.name }}</option>
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
                    <button @click="createFlow" style="width: 70%"
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
import {
  Dialog,
  DialogTitle,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import {XMarkIcon, ChevronDownIcon} from "@heroicons/vue/24/outline";

export default {
  name: "CreateFlowModal",
  components: {
    Dialog,
    DialogTitle,
    DialogPanel,
    TransitionChild,
    TransitionRoot,
    XMarkIcon,
  },
  props: ["open", "selectedFlow"],
  data() {
    return {
      name: null,
      flowEvent: null,
      flowEvents: [],
      availableEvents: []
    }
  },
  mounted() {
    // populate translations with the languages that are supported
    if (this.selectedFlow) {
      this.name = this.selectedFlow.name;
      this.flowEvent = this.selectedFlow.event;
    }

    if (this.currentApp) {
      this.availableEvents = this.currentApp.events;
      if (this.availableEvents.find(event => event.id === -1) === undefined) {
        this.availableEvents.push({name: 'new event', id: -1})
      }
    }
  },
  watch: {
    selectedFlow(newVal) {
      if (newVal !== null) {
        this.name = newVal.name;
        this.flowEvent = newVal.event;
      } else {
        this.name = null;
        this.flowEvent = null;
      }
    },
    currentApp(newVal) {
      if (newVal) {
        this.availableEvents = newVal.events;
        if (this.availableEvents.find(event => event.id === -1) === undefined) {
          this.availableEvents.push({name: 'new event', id: -1})
        }
      }
    },
    flowEvent(newVal) {
      if (newVal === 'New event') {
        setTimeout(() => {
          this.$refs.newEvent.focus();
        }, 50);
      }
    }
  },
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  methods: {
    createFlow() {
      let flow = {
        name: this.name,
        event: this.flowEvent === 'new event' ? this.$refs.newEvent.value : this.flowEvent,
      };

      this.$store.dispatch('createFlow', flow)
          .then((response) => {
            this.$emit('onClose');
          })
          .catch((error) => {
            console.log(error);
          });
    },
    updateFlow() {
      let flow = {
        id: this.selectedFlow.id,
        name: this.name,
        event: this.flowEvent === 'new event' ? this.$refs.newEvent.value : this.flowEvent,
      };

      this.$store.dispatch('updateFlow', flow)
          .then((response) => {
            this.$emit('onClose');
          })
          .catch((error) => {
            console.log(error);
          });
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
    clickChevron() {
      document.getElementById('selectEvent').click();
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  z-index: 100;
}

.modal {
  background: #FFFFFF;
  width: 500px;
  height: 100%;
  overflow-x: auto;
  position: fixed;
  right: 0;
  flex-direction: column;
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  color: #4AAE9B;
  justify-content: space-between;
}

.modal-footer {
  position: fixed;
  bottom: 0;
  width: 500px;
  background-color: #eee;
}

.modal-body {
  position: relative;
  padding: 15px;
  margin-bottom: 70px;
}
</style>