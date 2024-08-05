<template>
  <div v-if="app">
    <div class="login w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
      <div class="bg-gray-50 p-8">
        <div class="flex items-start justify-between space-x-6">
          <div class="space-y-1">
            <h1 class="text-base font-semibold leading-6 text-gray-900">
              Setup notifications
            </h1>
            <p class="text-sm text-gray-500">
              Follow the easy steps to integrate notifications in your app.
            </p>
          </div>
        </div>
      </div>
      <div class="p-8 space-y-4">
        <div class="mb-2">
          <label for="languages" class="block text-sm font-medium text-gray-900">Select languages</label>
          <div class="mt-2">
            <el-select v-model="selectedLanguages" multiple filterable placeholder="Select languages"
                       class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full">
              <el-option
                  v-for="language in languages"
                  :key="language.code"
                  :label="language.name"
                  :value="language.code">
              </el-option>
            </el-select>
          </div>
        </div>
        <div v-if="app.has_web">
          <h2 class="text-base font-semibold leading-6 text-gray-900 mb-2">Web Setup</h2>
          <div class="mb-3">
            <label for="color" class="block text-lg font-medium leading-6 text-gray-900">1. Choose widget color</label>
            <div class="mt-2 flex">
              <input v-model="color" type="color" name="color" id="color" class="block w-8 h-9 rounded-md bg-transparent mr-2" />
              <input v-model="color" type="text" name="project-name" id="project-name" class="flex-grow block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
          <div class="mb-3">
            <label for="website" class="block text-lg font-medium leading-6 text-gray-900">2. Enter your website URL</label>
            <div class="mt-2">
              <input v-model="website_url" type="text" name="website" id="website" placeholder="https://example.com" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
          <div class="mb-3">
            <label for="website">
              <span class="block text-lg font-medium leading-6 text-gray-900">3. Download the service worker</span>
              <span class="block text-sm leading-6 text-gray-400">Save it on an accessible location on the same domain name.</span>
            </label>
            <div class="mt-2">
              <button @click="downloadServiceWorker" type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
                <ArrowDownCircleIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
                Download
              </button>
            </div>
          </div>
          <div class="mb-3">
            <label for="website">
              <span class="block text-lg font-medium leading-6 text-gray-900">4. Download the manifest</span>
              <span class="block text-sm leading-6 text-gray-400">Save it in the root of your website.</span>
            </label>
            <div class="mt-2">
              <button @click="downloadManifest" type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
                <ArrowDownCircleIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
                Download
              </button>
            </div>
          </div>
          <div class="mb-3">
            <label for="code">
              <span class="block text-lg font-medium leading-6 text-gray-900">5. Add manifest to the head</span>
              <span class="block text-sm leading-6 text-gray-400">Add the manifest.json location to the head of the html page.</span>
            </label>
            <div class="mt-2">
              <div class="relative w-full">
                <div class="rounded-xl bg-primary-50 p-4">
                  <span @click="copy(decodeHtml(manifestCode))" class="cursor-pointer absolute top-3 right-3 rounded-lg border-2 px-4 py-2 border-primary-400 bg-primary-50/50 text-primary-500 text-xs font-medium" style="-webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);">
                    Copy
                  </span>
                  <div class="nice-scrollbars overflow-x-scroll w-full">
                    <code v-html="manifestCodeHighlighted" class="whitespace-nowrap">
                    </code>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label for="code">
              <span class="block text-lg font-medium leading-6 text-gray-900">6. Add the JS widget</span>
              <span class="block text-sm leading-6 text-gray-400">Select how you want to integrate MagicPush.</span>
            </label>
            <div class="mt-2">
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
        <div v-if="app.has_android">
          <h2 class="text-base font-semibold leading-6 text-gray-900">Android Setup</h2>
          <div>
            <label for="dropzone-file" class="block mb-2 text-sm font-medium text-gray-900">Firebase Service Account. <a class="text-primary-400 underline" href="https://docs.getmagicpush.com/firebase-setup" target="_blank">See docs</a></label>
            <FileDrop v-model="firebaseServiceAccountFile" v-bind:id="'file-input'" v-bind:fileType="'file'"
                      v-bind:requirements="'JSON file only'" v-bind:uploadUrl="`/api/v1/apps/${app.id}/firebase`"/>
          </div>
        </div>
        <div v-if="app.has_ios">
          <h2 class="text-base font-semibold leading-6 text-gray-900">iOS Setup</h2>
          <div>
            <label for="dropzone-file" class="block mb-2 text-sm font-medium text-gray-900">p8 file</label>
            <FileDrop v-model="appleKeyFile" v-bind:id="'p8-file-input'" v-bind:fileType="'file'"
                      v-bind:requirements="'p8 file only'" v-bind:uploadUrl="`/api/v1/apps/${app.id}/apple`"/>
          </div>
          <div>
            <label for="appleKeyId" class="block text-sm font-medium leading-6 text-gray-900">Apple Key Id</label>
            <div class="mt-2">
              <input v-model="appleKeyId" type="text" name="appleKeyId" id="appleKeyId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" required="">
            </div>
          </div>
          <div>
            <label for="appleTeamId" class="block text-sm font-medium leading-6 text-gray-900">Apple Team Id</label>
            <div class="mt-2">
              <input v-model="appleTeamId" type="text" name="appleTeamId" id="appleTeamId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" required="">
            </div>
          </div>
          <div>
            <label for="appleBundleId" class="block text-sm font-medium leading-6 text-gray-900">Apple Bundle Id</label>
            <div class="mt-2">
              <input v-model="appleBundleId" type="text" name="appleBundleId" id="appleBundleId" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" required="">
            </div>
          </div>
        </div>
        <button @click="updateApp" type="submit" class="rounded-md w-full bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
          Finish setup
        </button>
        <button @click="$router.push({ path: '/dashboard', query: { app: app.id }})" type="button" class="rounded-md w-full bg-gray-100 px-6 py-2 text-sm font-semibold text-gray-600 shadow-sm hover:bg-gray-200">
          Skip
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import hljs from 'highlight.js';
import 'highlight.js/styles/default.css';
import { ArrowDownCircleIcon } from "@heroicons/vue/24/solid";
import DropzoneFileUpload from "@/components/DropzoneFileUpload";
import FileDrop from "@/components/FileDrop.vue";

export default {
  name: "SetupNotificationsPage",
  components: {FileDrop, ArrowDownCircleIcon},
  data() {
    return {
      app: null,
      firebaseServiceAccountFile: null,
      appleKeyFile: null,
      appleKeyId: null,
      appleTeamId: null,
      appleBundleId: null,
      selectedLanguages: null,
      color: "#8b5cf6",
      website_url: "https://",
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
    }
  },
  mounted() {
    let self = this;

    this.selectedTab = this.tabs.find(tab => tab.current);
    this.$store.dispatch("getApps")
        .then((res) => {
          res.data.apps.forEach((app) => {
            if (app.id === parseInt(self.$route.params.id)) {
              self.app = app;
              self.selectedLanguages = app.languages;

              self.tabs.find(tab => tab.name === 'JavaScript').code = `
&lt;script src="https://getmagicpush.com/js/main.min.js"&gt;&lt;/script&gt;\n
&lt;script type="application/javascript"&gt;
&nbsp;&nbsp;&nbsp;&nbsp;new MagicPush("${app.hash}", "/js/MagicPushSW.js", true, true);
&lt;/script&gt;`
              self.tabs.find(tab => tab.name === 'Vue.js').code = `
import { createApp } from 'vue'
import MagicPushVuePlugin from "magicpush-vue";
createApp(App).use(MagicPushVuePlugin).mount('#app');
this.$magicpush.initialize({
  appId: '${app.hash}',
  swUrl: '/js/MagicPushSW.js',
  showButton: true,
  autoShowModal: true,
})

this.$magicpush.addListener((event) => {
  console.log(event);
});`;
              self.tabs.find(tab => tab.name === 'Node').code = `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "${app.hash}",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
})

MagicPush.addListener((event) => {
    console.log(event)
});`;
              self.tabs.find(tab => tab.name === 'React').code = `
import MagicPush from "magicpush-npm";
MagicPush.init({
    appId: "${app.hash}",
    swUrl: "/js/MagicPushSW.js",
    showButton: true,
    autoShowModal: true
});

MagicPush.addListener((event) => {
    console.log(event)
});`
            }
          });
        })
        .catch((err) => {

        });
  },
  computed: {
    jwtToken() {
      return this.$store.getters.jwtToken;
    },
    host() {
      return this.$store.state.host;
    },
    languages() {
      return this.$store.getters.languages;
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
  methods: {
    updateApp() {
      let self = this;

      let appData = {
        id: this.app.id,
        languages: this.selectedLanguages,
        appleKeyId: this.appleKeyId,
        appleTeamId: this.appleTeamId,
        appleBundleId: this.appleBundleId,
        widget_color: this.color,
        website_url: this.website_url,
      }
      this.$store.dispatch("updateApp", appData)
          .then((res) => {
            console.log("nextUrl", self.$route.query.nextUrl);
            self.$store.commit("setSelectedApp", res.data);
            self.$router.push({ path: self.$route.query.nextUrl || "/dashboard", query: { app: self.app.id } })
          })
          .catch((err) => {
            alert(err);
          });
    },
    uploaded(file) {
      this.imageFile = file;
      this.$emit("uploaded");
    },
    checkFile(file) {
      // if (
      //     file.type !== "image/jpeg" &&
      //     file.type !== "image/png" &&
      //     file.type !== "image/gif"
      // ) {
      //   this.$refs.imageDropzone.dropzone.removeFile(file);
        alert(
            `Filetype '${file.type}' not supported. Please upload images in .jpeg or .png format.`
        );
      // } else if (file.size > 5000000) {
      //   this.$refs.imageDropzone.dropzone.removeFile(file);
      //   alert(
      //       `Image is too big. Image is ${Math.round(
      //           file.size / 1000
      //       )}kb, should be max. 5MB`
      //   );
      // }
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
.login {
  margin-top: 5rem;
  margin-left: auto;
  margin-right: auto;
}

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