<template>
  <div v-if="app" class="p-4 border-gray-100 h-screen" style="border-left-style: solid; border-left-width: 0;">
    <h1 class="font-medium text-xl text-slate-900">
      App Settings
    </h1>

    <div class="mt-4 pb-4">
      <div>
        <div class="space-y-12 sm:space-y-16">
          <div>
            <div class="mt-10 space-y-8 border-b border-gray-900/10 pb-12 sm:space-y-0 sm:divide-y sm:divide-gray-900/10 sm:border-t sm:pb-0">
              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">App name</label>
                <div class="mt-2 sm:col-span-2 sm:mt-0">
                  <input v-model="app.name" type="text" name="app-name" id="app-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:max-w-lg sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="country" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Languages</label>
                <div class="mt-2 sm:col-span-2 sm:mt-0 sm:max-w-lg">
                  <el-select v-model="app.languages" multiple filterable placeholder="Select languages"
                             class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-64">
                    <el-option
                        v-for="language in languages"
                        :key="language.code"
                        :label="language.name"
                        :value="language.code">
                    </el-option>
                  </el-select>
                </div>
              </div>

              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">App ID</label>
                <div class="mt-2 flex rounded-md shadow-sm sm:max-w-lg">
                  <div class="relative flex flex-grow items-stretch focus-within:z-10">
                    <input v-model="app.hash" disabled type="text" name="apiKey" id="apiKey" class="block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
                  </div>
                  <button @click="copy(app.hash)" type="button" class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    <ClipboardIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                    Copy
                  </button>
                </div>
              </div>

              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">API Key</label>
                <div class="mt-2 flex rounded-md shadow-sm sm:max-w-lg">
                  <div class="relative flex flex-grow items-stretch focus-within:z-10">
                    <input v-model="app.api_key" disabled type="text" name="apiKey" id="apiKey" class="block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
                  </div>
                  <button @click="copy(app.api_key)" type="button" class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    <ClipboardIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                    Copy
                  </button>
                </div>
              </div>

              <div class="pt-4 pb-4">
                <div class="cursor-pointer items-baseline flex" @click="expandWebPush = !expandWebPush">
                  <ChevronDownIcon ref="chevron-web" class="h-4 w-4 block" :class="expandWebPush ? 'rotate-180': ''" />

                  <div class="block ml-2">
                    <h2 class="text-base font-semibold leading-7 text-gray-900">Web push</h2>
                    <p class="max-w-2xl text-sm leading-6 text-gray-600">Change your web push settings</p>
                  </div>
                </div>

                <div v-if="expandWebPush" class="mt-4 space-y-8 border-t border-gray-900/10 pb-12 sm:space-y-0 sm:divide-y sm:divide-gray-900/10 sm:border-t sm:pb-0">
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Website url</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <input v-model="app.website_url" type="text" name="app-name" id="app-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:max-w-lg sm:text-sm sm:leading-6" />
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Widget color</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0 flex sm:max-w-lg">
                      <input v-model="currentApp.widget_color" type="color" name="color" id="color" class="block w-8 h-9 rounded-md bg-transparent mr-2" />
                      <input v-model="currentApp.widget_color" type="text" name="project-name" id="project-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Public key</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0 sm:max-w-lg">
                      <textarea v-model="currentApp.vapid_public_key" :disabled="!editPublicKey" id="about" name="about" rows="3" class="block w-full max-w-2xl rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                      <span class="text-sm text-gray-400">Editing your public key may result in losing your subscribers. <span class="cursor-pointer underline text-gray-400 text-sm" @click="editPublicKey = !editPublicKey">{{ editPublicKey ? 'Stop editing' : 'Edit public key' }}</span></span>
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Private Key</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0 relative sm:max-w-lg">
                      <textarea v-model="currentApp.vapid_private_key"
                                :class="{'blur-sm': isBlurred}"
                                id="about"
                                name="about"
                                rows="3"
                                :disabled="!editPrivateKey"
                                class="block w-full max-w-2xl rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                      <button @click="toggleBlur" v-if="isBlurred" class="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/3 rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
                        Show private key
                      </button>
                      <span class="text-sm text-gray-400">Editing your private key may result in losing your subscribers. <span class="cursor-pointer underline text-gray-400 text-sm" @click="editPrivateKey = !editPrivateKey">{{ editPrivateKey ? 'Stop editing' : 'Edit private key' }}</span></span>
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Integration</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0 sm:max-w-lg">
                      <div class="mb-3">
                        <label for="tabs" class="sr-only">Select a tab</label>
                        <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                        <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-primary-500 focus:ring-primary-500 text-sm"
                                v-model="selectedTab" @change="onTabChange">
                          <option v-for="tab in tabs" :key="tab.name" :value="tab">{{ tab.name }}</option>
                        </select>
                      </div>
                      <div class="relative w-full mb-3">
                        <span class="block font-medium text-lg">{{ currentTab.title }}</span>
                        <span class="block pt-2 text-sm">{{ currentTab.instructions }}</span>
                        <div class="relative w-full">
                          <div v-if="currentTab.installCode" class="bg-primary-50 text-white rounded-lg mt-2">
                        <span @click="copy(currentTab.installCode)" class="cursor-pointer absolute top-3 right-3 rounded-lg border-2 px-4 py-2 border-primary-400 bg-primary-50/50 text-primary-500 text-xs font-medium" style="-webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);">
                          Copy
                        </span>
                            <code class="text-sm sm:text-base inline-flex text-left items-center space-x-4 p-4 pl-6">
                          <span class="flex gap-4">
                            <span class="shrink-0 text-gray-800">
                                $
                            </span>
                            <span class="flex-1">
                              <span v-html="currentTab.installCodeFormatted"></span>
                            </span>
                          </span>
                            </code>
                          </div>
                        </div>
                      </div>
                      <div class="relative w-full">
                        <div class="rounded-xl bg-primary-50 p-4">
                  <span @click="copy(decodeHtml(currentTab.code))" class="cursor-pointer absolute top-3 right-3 rounded-lg border-2 px-4 py-2 border-primary-400 bg-primary-50/50 text-primary-500 text-xs font-medium" style="-webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);">
                    Copy
                  </span>
                          <pre class="overflow-scroll">
                    <code v-html="code" :class="currentTab.language" style="overflow-x: hidden!important;"></code>
                  </pre>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="pt-4 pb-4">
                <div class="cursor-pointer items-baseline flex" @click="expandAndroid = !expandAndroid">
                  <ChevronDownIcon ref="chevron-web" class="h-4 w-4 block" :class="expandAndroid ? 'rotate-180': ''" />

                  <div class="block ml-2">
                    <h2 class="text-base font-semibold leading-7 text-gray-900">Android</h2>
                    <p class="max-w-2xl text-sm leading-6 text-gray-600">Change your Android push settings</p>
                  </div>
                </div>

                <div v-if="expandAndroid" class="mt-4 space-y-8 border-t border-gray-900/10 pb-12 sm:space-y-0 sm:divide-y sm:divide-gray-900/10 sm:border-t sm:pb-0">
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Firebase service account</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <FileDrop v-model="app.firebase_service_account_file" v-bind:id="'file-input'" v-bind:fileType="'file'"
                                v-bind:requirements="'JSON file only'" v-bind:uploadUrl="`/api/v1/apps/${app.id}/firebase`" class="sm:max-w-lg"/>
                    </div>
                  </div>
                </div>
              </div>

              <div class="pt-4 pb-4">
                <div class="cursor-pointer items-baseline flex" @click="expandIos = !expandIos">
                  <ChevronDownIcon ref="chevron-web" class="h-4 w-4 block" :class="expandIos ? 'rotate-180': ''" />

                  <div class="block ml-2">
                    <h2 class="text-base font-semibold leading-7 text-gray-900">iOS</h2>
                    <p class="max-w-2xl text-sm leading-6 text-gray-600">Change your iOS push settings</p>
                  </div>
                </div>

                <div v-if="expandIos" class="mt-4 space-y-8 border-t border-gray-900/10 pb-12 sm:space-y-0 sm:divide-y sm:divide-gray-900/10 sm:border-t sm:pb-0">
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">p8 key file</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <FileDrop v-model="app.apple_key_file" v-bind:id="'p8-file-input'" v-bind:fileType="'file'"
                                v-bind:requirements="'p8 file only'" v-bind:uploadUrl="`/api/v1/apps/${app.id}/apple`" class="sm:max-w-lg"/>
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Key ID</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <input v-model="app.apple_key_id" type="text" name="appleKeyId" id="appleKeyId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 sm:max-w-lg" required="">
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Team ID</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <input v-model="app.apple_team_id" type="text" name="appleTeamId" id="appleTeamId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 sm:max-w-lg" required="">
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                    <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Apple Bundle ID</label>
                    <div class="mt-2 sm:col-span-2 sm:mt-0">
                      <input v-model="app.apple_bundle_id" type="text" name="appleTeamId" id="appleTeamId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 sm:max-w-lg" required="">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 flex items-center justify-end gap-x-6">
          <button @click="updateApp" class="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import {ChevronDownIcon, ClipboardIcon} from "@heroicons/vue/20/solid";
import hljs from "highlight.js";
import FileDrop from "@/components/FileDrop.vue";

export default {
  name: "UserSettings",
  components: {FileDrop, ChevronDownIcon, ClipboardIcon },
  computed: {
    languages() {
      return this.$store.getters.languages;
    },
    currentApp() {
      return this.$store.getters.currentApp;
    },
    manifestCodeHighlighted() {
      return hljs.highlightAuto(this.decodeHtml(this.manifestCode)).value;
    },
    code() {
      let code = this.tabs.find(tab => tab.current).code;
      return hljs.highlightAuto(this.decodeHtml(code)).value;
    },
    currentTab() {
      return this.tabs.find(tab => tab.current);
    }
  },
  watch: {
    currentApp: {
      handler(newVal) {
        if (newVal != null) {
          this.app = newVal;
          this.updateCodeTabs();
        }
      },
      immediate: true
    }
  },
  data() {
    return {
      app: null,
      isBlurred: true,
      editPublicKey: false,
      editPrivateKey: false,
      manifestCode: `
&lt;link rel="manifest" href="/manifest.json"&gt;
      `,
      tabs: [
        {
          name: 'JavaScript',
          language: 'html',
          title: 'JS integration',
          instructions: 'Copy paste the code inside your html page to get started.',
          installCode: null,
          installCodeFormatted: null,
          code: `
&lt;script src="https://getmagicpush.com/js/main.min.js"&gt;&lt;/script&gt;\n
&lt;script type="application/javascript"&gt;
&nbsp;&nbsp;&nbsp;&nbsp;new MagicPush("APP ID", "/js/MagicPushSW.js", true, true);
&lt;/script&gt;
          `,
          current: true
        },
        {
          name: 'Node',
          language: 'language-javascript',
          title: 'NPM integrations',
          instructions: 'Use our NPM package to integrate MagicPush.',
          installCode: 'npm i magicpush-npm',
          installCodeFormatted: `
          <span class="text-gray-800">
            npm i
          </span>
          <span class="text-yellow-500">
              magicpush-npm
          </span>
          `,
          code: `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "APP ID",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
})

# listen to event push-subscribed or push-unsubscribed containing user_id
MagicPush.addListener((event) => {
    console.log(event)
});

MagicPush.toggleModal();`,
          current: false
        },
        {
          name: 'Vue.js',
          language: 'language-javascript',
          title: 'MagicPush Vue plugin',
          instructions: 'Integrate MagicPush directly into your Vue.js application.',
          installCode: 'npm i magicpush-vue',
          installCodeFormatted: `
          <span class="text-gray-800">
            npm i
          </span>
          <span class="text-yellow-500">
              magicpush-vue
          </span>
          `,
          code: `
import { createApp } from 'vue'
import MagicPushVuePlugin from "magicpush-vue";
createApp(App).use(MagicPushVuePlugin).mount('#app');
this.$magicpush.initialize({
  appId: 'APP ID',
  swUrl: '/js/MagicPushSW.js',
  showButton: true,
  autoShowModal: true,
})

# listen to event push-subscribed or push-unsubscribed containing user_id
this.$magicpush.addListener((event) => {
  console.log(event);
});`,
          current: false
        },
        {
          name: 'React',
          language: 'language-javascript',
          title: 'React integration',
          instructions: 'To use MagicPush in your React application, install the npm package.',
          installCode: 'npm i magicpush-npm',
          installCodeFormatted: `
          <span class="text-gray-800">
            npm i
          </span>
          <span class="text-yellow-500">
              magicpush-npm
          </span>
          `,
          code: `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "APP ID",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
});

# listen to event push-subscribed or push-unsubscribed containing user_id
MagicPush.addListener((event) => {
    console.log(event)
});
          `,
          current: false
        }
      ],
      selectedTab: null,
      expandWebPush: false,
      expandAndroid: false,
      expandIos: false
    }
  },
  mounted() {
    if (this.currentApp) {
      this.app = this.currentApp
      this.updateCodeTabs();
    } else {
      let self = this;
      this.$store.watch(() => this.$store.getters.currentApp, (newVal) => {
        self.app = newVal;
        self.updateCodeTabs();
      })
    }
    this.selectedTab = this.tabs.find(tab => tab.current);
  },
  methods: {
    toggleBlur() {
      this.isBlurred = !this.isBlurred;
    },
    generateApiKey() {
      let self = this;
      this.$store.dispatch('generateApiKey')
          .then((res) => {
            console.log(res);
            self.app.apiKey = res.data.token;
          })
          .catch((err) => {
            console.error(err);
          });
    },
    copy(str) {
      navigator.clipboard.writeText(str)
          .then(() => {
            alert('Copied to clipboard');
          })
          .catch((err) => {
            alert('Failed to copy to clipboard')
          });
    },
    updateApp() {
      this.$store.dispatch('updateApp', this.app)
          .then((res) => {
            console.log(res);
          })
          .catch((err) => {
            console.error(err);
          });
    },
    updateCodeTabs() {
      this.tabs.find(tab => tab.name === 'JavaScript').code = `
&lt;script src="https://getmagicpush.com/js/main.min.js"&gt;&lt;/script&gt;\n
&lt;script type="application/javascript"&gt;
&nbsp;&nbsp;&nbsp;&nbsp;new MagicPush("${this.app.hash}", "/js/MagicPushSW.js", true, true);
&lt;/script&gt;`
      this.tabs.find(tab => tab.name === 'Vue.js').code = `
import { createApp } from 'vue'
import MagicPushVuePlugin from "magicpush-vue";
createApp(App).use(MagicPushVuePlugin).mount('#app');
this.$magicpush.initialize({
  appId: '${this.app.hash}',
  swUrl: '/js/MagicPushSW.js',
  showButton: true,
  autoShowModal: true,
})

this.$magicpush.addListener((event) => {
  console.log(event);
});`;
      this.tabs.find(tab => tab.name === 'Node').code = `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "${this.app.hash}",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
})

MagicPush.addListener((event) => {
    console.log(event)
});`;
      this.tabs.find(tab => tab.name === 'React').code = `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "${this.app.hash}",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
});

MagicPush.addListener((event) => {
    console.log(event)
});`
    },
    downloadServiceWorker() {
      let data = "importScripts('https://getmagicpush.com/js/sw.min.js');"
      let dataStr = "data:text/javascript;charset=utf-8," + encodeURIComponent(data);
      this.downloadObjectAsJson(dataStr, "MagicPushSW.js");
    },
    downloadManifest() {
      let manifest = {
        "name": this.app.name,
        "display": "standalone",
        "id": "/?source=pwa",
        "start_url": "/?source=pwa",
        "icons": []
      }
      let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(manifest));
      this.downloadObjectAsJson(dataStr, "manifest.json");
    },
    downloadObjectAsJson(dataStr, exportName){
      var downloadAnchorNode = document.createElement('a');
      downloadAnchorNode.setAttribute("href",     dataStr);
      downloadAnchorNode.setAttribute("download", exportName);
      document.body.appendChild(downloadAnchorNode); // required for firefox
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    },
    decodeHtml(html) {
      var txt = document.createElement("textarea");
      txt.innerHTML = html;
      return txt.value;
    },
    onTabChange() {
      this.clickTab(this.selectedTab);
    },
    clickTab(tab) {
      this.tabs.forEach((tab) => {
        tab.current = false
      });
      tab.current = true;
    },
  }
}
</script>

<style scoped>
pre, code {
  background-color: transparent !important; /* Ensures no background color on the container */
}
/* Specific highlight styles */
.hljs {
  background-color: transparent !important; /* Override default Highlight.js background */
}
.hljs-keyword, .hljs-string, .hljs-title, .hljs-name {
  background-color: #ffffcc; /* Apply background only to text elements you choose */
  padding: 0.1em 0.2em; /* Optional: Adds padding around the text for better visibility */
}

pre::-webkit-scrollbar {
  width: 2px;               /* width of the entire scrollbar */
  height: 6px;
  padding: 1px;
}

pre::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

pre::-webkit-scrollbar-thumb {
  background-color: #c4b5fd;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 1px solid transparent;  /* creates padding around scroll thumb */
}

.nice-scrollbars::-webkit-scrollbar {
  width: 2px;               /* width of the entire scrollbar */
  height: 6px;
  padding: 1px;
}

.nice-scrollbars::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

.nice-scrollbars::-webkit-scrollbar-thumb {
  background-color: #c4b5fd;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 1px solid transparent;  /* creates padding around scroll thumb */
}
</style>