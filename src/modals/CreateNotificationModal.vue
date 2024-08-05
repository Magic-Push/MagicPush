<template>
  <div v-if="show" class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <span class="font-normal text-2xl text-slate-900 w-full p-3">
          {{ selectedNotification === null ? 'Create Notification' : 'Update Notification' }}
        </span>
        <div class="rounded-lg hover:bg-gray-200 w-6 h-6 m-3 cursor-pointer" @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="black" viewBox="0 0 24 24" stroke-width="1.5" stroke="black"
               class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/>
          </svg>
        </div>
      </header>

      <section class="modal-body">
        <div class="flex flex-col space-y-4 p-3">
          <div class="flex flex-col space-y-2">
            <label for="name" class="block mb-2 text-sm font-medium text-gray-900">Name</label>
            <input v-model="name" type="text" name="name" id="name"
                   class="block w-full rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600"
                   placeholder="Notification name" required="">
          </div>
          <div class="flex flex-col space-y-2">
            <label for="scheduled_at" class="block mb-2 text-sm font-medium text-gray-900">Schedule at</label>
            <div class="columns-2">
              <input v-model="scheduled_at" type="date" name="scheduled_at" id="scheduled_at"
                     class="block w-full rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600"
                     placeholder="Select a date" required="">
              <input v-model="scheduled_at_time" type="time" name="scheduled_at_time" id="scheduled_at_time"
                     class="block w-full rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600"
                     placeholder="Select a time" required="">
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <div class="flex items-start items-baseline">
              <div class="h-5">
                <input v-model="repeat" id="repeat" aria-describedby="repeat" type="checkbox"
                       class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300">
              </div>
              <div class="ml-3 text-sm">
                <label for="repeat" class="text-gray-500">Repeat notification</label>
              </div>
              <div class="ml-3">
                <select :disabled="!repeat" v-model="repeat_interval" id="repeat" name="repeat"
                        class="rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <label class="block mb-2 text-sm font-medium text-gray-900">Translations</label>
            <div class="flex flex-col space-y-2" v-for="translation in translations" :key="translation.language">
              <span class="text-lg font-medium text-gray-600 pt-3 pb-3">{{ getLanguageName(translation.language) }}</span>
              <div class="flex flex-col space-y-2">
                <label for="title" class="block mb-2 text-sm font-medium text-gray-900">Title</label>
                <input v-model="translation.title" type="text" name="title" id="title"
                       class="rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600"
                       placeholder="Notification title" required="">
              </div>
              <div class="flex flex-col space-y-2">
                <label for="message" class="block mb-2 text-sm font-medium text-gray-900">Message</label>
                <textarea v-model="translation.message" name="message" id="message"
                          class="rounded-lg border-0 p-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600"
                          placeholder="Notification message" required=""></textarea>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer class="modal-footer">
        <button @click="createNotification" style="width: 30%;"
                class="m-1 text-gray-600 bg-gray-300 hover:bg-gray-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
          Save draft
        </button>
        <button @click="createNotification" style="width: 70%"
                class="m-1 text-white bg-primary-600 hover:bg-primary-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
          Create & publish
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: "CreateNotificationModal",
  props: ["show", "selectedNotification"],
  data() {
    return {
      name: null,
      scheduled_at: null,
      scheduled_at_time: null,
      repeat: false,
      repeat_interval: "monthly",
      translations: [],
    }
  },
  mounted() {
    // populate translations with the languages that are supported
    let self = this;
    if (this.selectedNotification) {
      let scheduledAtDate = new Date(this.selectedNotification.scheduled_at);
      this.name = this.selectedNotification.name;
      this.scheduled_at = scheduledAtDate.toISOString().split('T')[0];
      this.scheduled_at_time = scheduledAtDate.toISOString().split('T')[1].split('.')[0];
      this.repeat = this.selectedNotification.repeat;
      this.repeat_interval = this.selectedNotification.repeat_interval;
      this.translations = this.selectedNotification.translations;
    } else {
      if (this.currentApp) {
        this.currentApp.languages.forEach((language) => {
          self.translations.push({
            language: language,
            title: null,
            message: null,
          });
        })
      } else {
        const watcher = this.$store.watch(
            (state) => state.currentApp,
            (currentApp) => {
              if (currentApp !== null) {
                currentApp.languages.forEach((language) => {
                  self.translations.push({
                    language: language,
                    title: null,
                    message: null,
                  });
                })
                watcher();
              }
            }
        );
      }
    }
  },
  watch: {
    selectedNotification(newVal) {
      if (newVal !== null) {
        let scheduledAtDate = new Date(newVal.scheduled_at);
        this.name = newVal.name;
        this.scheduled_at = scheduledAtDate.toISOString().split('T')[0];
        this.scheduled_at_time = scheduledAtDate.toISOString().split('T')[1].split('.')[0];
        this.repeat = newVal.repeat;
        this.repeat_interval = newVal.repeat_interval;
        this.translations = newVal.translations;
      } else {
        this.name = null;
        this.scheduled_at = null;
        this.scheduled_at_time = null;
        this.repeat = false;
        this.repeat_interval = "monthly";
      }
    }
  },
  computed: {
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  methods: {
    createNotification() {
      let notification = {
        name: this.name,
        scheduled_at: this.scheduled_at + "T" + this.scheduled_at_time,
        repeat: this.repeat,
        repeat_interval: this.repeat_interval,
        translations: this.translations
      };

      this.$store.dispatch('createScheduledNotification', notification)
          .then((response) => {
            this.$emit('close');
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