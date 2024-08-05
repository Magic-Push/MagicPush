<template>
  <div ref="modal" v-if="app">
    <div v-if="modalType === 'notifications'" class="notifications-modal bg-white">
      <div class="block px-4 py-2 font-semibold text-primary-900 rounded-t-lg bg-primary-50">
        Notifications
      </div>
      <div class="notifications divide-y divide-gray-100" style="height: 350px; overflow-y: scroll;">
<!--        <ul role="list" class="flex-1 pl-2 pr-2">-->
<!--          <li v-for="item in notifications" :key="item.id" class="py-2">-->
<!--            <div @click="notificationClicked" class="p-2 flex items-center cursor-pointer" :class="item.status === 'new' ? 'bg-gray-100 rounded-lg' : ''">-->
<!--              <div v-if="item.image" class="w-10 h-10 mr-2 rounded bg-gray-400"></div>-->
<!--              <div>-->
<!--                <div class="flex items-center gap-x-3">-->
<!--                  <h3 class="flex-auto truncate text-sm font-semibold leading-6 text-gray-900">{{ item.title }}</h3>-->
<!--                  <time :datetime="item.created_at" class="flex-none right-0 text-xs text-gray-500">{{parseDate(item.created_at)}}</time>-->
<!--                </div>-->
<!--                <p class="mt-1 truncate text-sm text-gray-500">-->
<!--                  {{item.message}}-->
<!--                </p>-->
<!--              </div>-->
<!--            </div>-->
<!--          </li>-->
<!--        </ul>-->
        <a v-for="item in notifications" :key="item.id" href="#" :class="item.status === 'new' ? 'opacity-100' : 'opacity-50'" class="flex px-4 py-3 hover:bg-gray-100">
          <div class="flex-shrink-0">
<!--            <img class="rounded-full w-11 h-11" src="/docs/images/people/profile-picture-5.jpg" alt="Robert image">-->
<!--            <div class="absolute flex items-center justify-cester w-5 h-5 ms-6 -mt-5 bg-purple-500 border border-white rounded-full dark:border-gray-800">-->
<!--              <svg class="w-2 h-2 text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 14">-->
<!--                <path d="M11 0H2a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm8.585 1.189a.994.994 0 0 0-.9-.138l-2.965.983a1 1 0 0 0-.685.949v8a1 1 0 0 0 .675.946l2.965 1.02a1.013 1.013 0 0 0 1.032-.242A1 1 0 0 0 20 12V2a1 1 0 0 0-.415-.811Z"/>-->
<!--              </svg>-->
<!--            </div>-->
          </div>
          <div class="w-full">
            <div class="text-gray-500 text-sm mb-1.5"><span class="font-semibold text-gray-900 dark:text-white">{{ item.title }}</span> {{item.message}}</div>
            <div class="text-xs text-primary-600">3 hours ago</div>
          </div>
        </a>
      </div>
      <a href="https://getmagicpush.com" target="_blank" class="w-full block text-center text-sm items-baseline bg-primary-50 p-1">
        <img class=" h-4 inline-block" src="/images/magicpushlogo.png" alt="" />
        <span class="pl-1 inline-block font-medium text-primary-700">Magic</span>
        <span class="inline-block font-light text-primary-700">Push</span>
      </a>
    </div>
    <div v-else-if="modalType === 'notifications-v2'" class="notifications-v2-modal">
      <div v-for="item in notifications" :key="item.id" aria-live="assertive" class="pointer-events-none inset-0 flex items-end px-2 py-2 sm:items-start sm:p-6">
        <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
          <!-- Notification panels, dynamically insert this into the live region when it needs to be displayed -->
          <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="show" class="pointer-events-auto w-full max-w-sm rounded-lg bg-white shadow-md ring-1 ring-black ring-opacity-5">
              <div class="p-4">
                <div class="flex items-start">
<!--                  <div class="flex-shrink-0 pt-0.5">-->
<!--                    <img class="h-10 w-10 rounded-full" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2.2&w=160&h=160&q=80" alt="" />-->
<!--                  </div>-->
                  <div class=" w-0 flex-1">
                    <p class="text-sm font-medium text-gray-900">{{item.title}}</p>
                    <p class="mt-1 text-sm text-gray-500">{{item.message}}</p>
                  </div>
                  <div class="ml-4 flex flex-shrink-0">
                    <button type="button" @click="show = false" class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                      <span class="sr-only">Close</span>
                      <XMarkIcon class="h-5 w-5" aria-hidden="true" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
    <div v-else-if="modalType === 'request'" class="request-modal">
      <div class="inset-0 z-10">
        <div class="min-h-full text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden bg-white px-4 text-left transition-all pt-6 pl-6 pr-6">
            <div class="sm:flex sm:items-start">
              <div class="text-left sm:ml-4 sm:mt-0 sm:text-left">
                <span class="text-base font-semibold leading-6 text-gray-900">
                  Receive notifications
                </span>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Start receiving notifications from {{ app ? app.name : '' }}.
                  </p>
                </div>
              </div>
            </div>
            <div class="mt-5 flex justify-between w-full">
              <button type="button" :style="`background-color: ${app.widget_color};`" class="rounded-md w-full px-3 py-2 text-sm font-semibold text-white shadow-sm hover:opacity-80" @click="accept">Accept</button>
              <button type="button" class="rounded-md ml-3 w-full bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" @click="cancel" ref="cancelButtonRef">Refuse</button>
            </div>
            <div class="w-full block text-center text-xs items-baseline p-3">
              <a href="https://getmagicpush.com" target="_blank" >
                <span class="inline-block font-light text-gray-700 pr-1">Powered by</span>
                <img class=" h-3.5 inline-block" src="/images/magicpushlogo.png" alt="" />
                <span class="pl-1 inline-block font-medium text-primary-700">Magic</span>
                <span class="inline-block font-light text-primary-700">Push</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="modalType === 'install-pwa'" class="request-modal">
      <div class="inset-0 z-10">
        <div class="min-h-full text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden bg-white px-4 text-left transition-all pt-6 pl-6 pr-6">
            <div class="sm:flex sm:items-start">
              <div class="text-left sm:mt-0 sm:text-left">
                <span class="text-base font-semibold leading-6 text-gray-900">
                  Add {{app ? app.name : ''}} to your homescreen
                </span>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    To receive notifications please add {{ app ? app.name : '' }} to your homescreen.
                  </p>
                  <div class="pt-2 pb-2 flex items-baseline">
                    <span class="inline-block rounded-full bg-gray-200 text-gray-700 text-lg w-10 h-10 text-center content-center">
                      1
                    </span>
                    <div class="flex-1">
                      <span class="inline-block text-gray-500 text-sm ml-1">
                        Tap the
                      </span>
                      <img class="inline-block w-10 h-10 bg-white shadow-sm rounded-sm ml-1 mr-1" :src="isSafari ? '/images/ios-safari-sharing-api-button.svg' : '/images/ios-chrome-more-button.svg'">
                      <span class="inline-block text-gray-500 text-sm">
                        {{ isSafari ? 'button below.' : 'button in the upper right corner.' }}
                      </span>
                    </div>
                  </div>
                  <div class="pt-2 pb-2 flex flex items-baseline">
                    <span class="inline-block rounded-full bg-gray-200 text-gray-700 text-lg w-10 h-10 text-center content-center">
                      2
                    </span>
                    <div class="flex-1">
                      <span class="inline-block text-gray-500 text-sm ml-1">
                        Click on
                      </span>
                      <img class="inline-block h-8 bg-white shadow-sm rounded-sm ml-1" src="/images/ios-safari-add-to-home-screen-button.svg">
                      <span class="inline-block text-gray-500 text-sm ml-1">
                        from the menu that pops up. You may need to scroll down.
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-5 flex justify-between w-full">
              <button type="button" :style="`background-color: ${app.widget_color};`" class="rounded-md w-full px-3 py-2 text-sm font-semibold text-white shadow-sm hover:opacity-80" @click="pwaDone">Done</button>
              <button type="button" class="rounded-md ml-3 w-full bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" @click="cancel" ref="cancelButtonRef">Cancel</button>
            </div>
            <div class="w-full block text-center text-xs items-baseline p-3">
              <a href="https://getmagicpush.com" target="_blank" >
                <span class="inline-block font-light text-gray-700 pr-1">Powered by</span>
                <img class=" h-3.5 inline-block" src="/images/magicpushlogo.png" alt="" />
                <span class="pl-1 inline-block font-medium text-primary-700">Magic</span>
                <span class="inline-block font-light text-primary-700">Push</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="modalType === 'connect'" class="connect-modal">

    </div>
    <div v-else-if="modalType === 'settings'" class="settings-modal">
      <div class="inset-0 z-10">
        <div class="min-h-full text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden bg-white px-4 text-left transition-all pt-6 pl-6 pr-6">
            <div class="sm:flex sm:items-start">
              <div class="text-left sm:ml-4 sm:mt-0 sm:text-left">
                <span class="text-base font-semibold leading-6 text-gray-900">
                  Notification settings
                </span>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    What kind of notifications do you want to receive? Click <span class="font-semibold cursor-pointer" @click="unsubscribe">here</span> if you wish to unsubscribe.
                  </p>
                </div>
                <div class="mt-2" v-if="app && appUser">
                  <SwitchGroup v-for="group in app.notification_groups" :key="group" as="div" class="flex items-center pt-2 pb-2">
                    <Switch @click="clickSwitch(group)" :checked="isChecked(group)" :style="isChecked(group) ? `background-color: ${app.widget_color};` : 'bg-gray-200'" class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2">
                      <span aria-hidden="true" :class="[isChecked(group) ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out']" />
                    </Switch>
                    <SwitchLabel as="span" class="ml-3 w-full">
                      <span class="font-medium text-gray-700">{{ capitalizeFirstLetter(group) }}</span>
                    </SwitchLabel>
                  </SwitchGroup>
                </div>
              </div>
            </div>
            <div class="mt-5 flex justify-between w-full">
              <button type="button" :style="`background-color: ${app.widget_color};`" class="rounded-md w-full px-3 py-2 text-sm font-semibold text-white shadow-sm hover:opacity-80" @click="save">Save</button>
              <button type="button" class="rounded-md ml-3 w-full bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" @click="cancel" ref="cancelButtonRef">Cancel</button>
            </div>
            <div class="w-full block text-center text-xs items-baseline p-3">
              <a href="https://getmagicpush.com" target="_blank" >
                <span class="inline-block font-light text-gray-700 pr-1">Powered by</span>
                <img class=" h-3.5 inline-block" src="/images/magicpushlogo.png" alt="" />
                <span class="pl-1 inline-block font-medium text-primary-700">Magic</span>
                <span class="inline-block font-light text-primary-700">Push</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { XMarkIcon } from '@heroicons/vue/20/solid';
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'

export default {
  name: "ModalPage",
  components: {XMarkIcon, Switch, SwitchGroup, SwitchLabel},
  data() {
    return {
      modalType: 'request', // 'request', 'connect', 'settings, 'notifications', 'notifications-v2'
      appUser: null,
      show: true,
      open: true,
      statuses: {
        read: 'text-gray-300 bg-gray-100/10',
        new: 'text-green-400 bg-green-400/10',
      },
      notifications: [],
      websiteName: "MagicPush",
      app: null,
      notificationSubscription: null,
      isDeviceIOS: null,
      isRunningStandalone: null,
      isSafari: null,
    }
  },
  watch: {
    modalType(newVal, oldVal) {
      let self = this;
      if (newVal === 'notifications') {
        this.$store.dispatch('getNotifications', this.$route.params.appId)
          .then((response) => {
            self.notifications = response.data;
          })
          .catch((error) => {

          });
      }

      setTimeout(() => {
        if (this.$refs.modal !== undefined) {
          console.log('ModalPage: modal-resize', this.$refs.modal.scrollHeight);
          window.parent.postMessage({message: 'modal-resize', height: this.$refs.modal.scrollHeight + 1}, '*');
        }
      }, 200);
    }
  },
  mounted() {
    let self = this;
    if (this.$route.params.appId !== null) {
      this.$store.dispatch('getAppFromLib', this.$route.params.appId)
        .then((response) => {
          self.app = response.data;
        })
        .catch((error) => {

        });
    }

    window.addEventListener('message', (event) => {
      console.log('ModalPage: message', event.data);
      if (event.data.message === 'app-user-id') {
        let userData = {
          appHash: self.$route.params.appId,
          userHash: event.data.appUserId,
        }
        self.$store.dispatch('getAppUser', userData)
            .then((res) => {
              self.appUser = res.data;

              let body = {
                appHash: self.$route.params.appId,
                userHash: self.appUser.hash,
              }
              if (self.appUser.language !== navigator.language) {
                body['language'] = navigator.language;
              }
              if (self.appUser.web_push_endpoint !== self.notificationSubscription.endpoint) {
                body['web_push_endpoint'] = event.data.subscription.endpoint;
                body['web_push_auth'] = event.data.subscription.keys.auth;
                body['web_push_p256dh'] = event.data.subscription.keys.p256dh;
              }
              this.$store.dispatch('updateAppUser', body)
                  .then((response) => {
                    console.log('ModalPage: updateAppUser', response.data);
                  })
                  .catch((error) => {
                    console.log('ModalPage: updateAppUser', error);
                  });
            })
            .catch((error) => {

            });
      }

      if (event.data.message === 'new-app-user-id') {
        let appUserData = {
          appHash: self.$route.params.appId,
          language: Navigator.language,
        }
        self.$store.dispatch('createAppUser', appUserData)
            .then((res) => {
              self.appUser = res.data;
              window.parent.postMessage({message: 'created-app-user-id', appUserId: res.data.hash}, '*')
            })
            .catch((error) => {

            });
      }

      if (event.data.message === 'has-subscription') {
        self.modalType = 'settings';
        self.notificationSubscription = event.data.subscription;
      }

      if (event.data.message === 'push-subscribed') {
        self.modalType = 'settings';
        self.notificationSubscription = event.data.subscription;

        self.$store.dispatch('updateAppUser', {
          appHash: self.$route.params.appId,
          userHash: self.appUser.hash,
          web_push_endpoint: event.data.subscription.endpoint,
          web_push_auth: event.data.subscription.keys.auth,
          web_push_p256dh: event.data.subscription.keys.p256dh,
        })
          .then((response) => {
            console.log('ModalPage: updateAppUser', response.data);
          })
          .catch((error) => {
            console.log('ModalPage: updateAppUser', error);
          });
      }

      if (event.data.message === 'push-unsubscribed') {
        self.modalType = 'request';
        self.notificationSubscription = null;

        self.$store.dispatch('updateAppUser', {
          appHash: self.$route.params.appId,
          userHash: self.appUser.hash,
          web_push_endpoint: null,
          web_push_auth: null,
          web_push_p256dh: null,
        })
          .then((response) => {
            console.log('ModalPage: updateAppUser', response.data);
          })
          .catch((error) => {
            console.log('ModalPage: updateAppUser', error);
          });
      }

      if (event.data.message === 'is-safari') {
        self.isSafari = event.data.isSafari;
      }

      if (event.data.message === 'is-running-standalone') {
        self.isRunningStandalone = event.data.isRunningStandalone;
      }

      if (event.data.message === 'is-ios') {
        self.isDeviceIOS = event.data.isIOS;
      }
    });

    setTimeout(() => {
      if (this.$refs.modal !== undefined) {
        console.log('ModalPage: modal-resize', this.$refs.modal.scrollHeight);
        window.parent.postMessage({message: 'modal-resize', height: this.$refs.modal.scrollHeight + 1}, '*');
      }
    }, 200);
  },
  methods: {
    notificationClicked() {

    },
    unsubscribe() {
      window.parent.postMessage({ message: 'unsubscribe-push' }, '*');
    },
    accept() {
      if (this.isSafari === true && this.isDeviceIOS === true && this.isRunningStandalone === false) {
        this.modalType = 'install-pwa';
      } else {
        window.parent.postMessage({ message: 'accept-push', publicKey: this.app.vapid_public_key }, '*');
      }
    },
    pwaDone() {
      window.parent.open(this.app.website_url, '_blank');
    },
    save() {
      this.$store.dispatch('updateAppUser', {
        appHash: this.$route.params.appId,
        userHash: this.appUser.hash,
        notification_groups: JSON.stringify(this.appUser.notification_groups),
      })
        .then((response) => {
          console.log('ModalPage: updateAppUser', response.data);
          window.parent.postMessage({ message: 'button-clicked' }, '*');
        })
        .catch((error) => {
          console.log('ModalPage: updateAppUser', error);
        });
    },
    cancel() {
      window.parent.postMessage({ message: 'button-clicked' }, '*');
    },
    isChecked(group) {
      return this.appUser.notification_groups.includes(group);
    },
    clickSwitch(group) {
      if (this.appUser.notification_groups.includes(group)) {
        this.appUser.notification_groups.splice(this.appUser.notification_groups.indexOf(group), 1);
      } else {
        this.appUser.notification_groups.push(group);
      }
      Array.isArray(this.appUser.notification_groups);
    },
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    parseDate(dateStr) {
      let date = new Date(dateStr);

      let formatter = new Intl.DateTimeFormat('en-GB', {
        month: 'short'
      });

      return formatter.format(date);
    }
  }
}
</script>

<style scoped>
.notifications-modal {
  width: 100%;
  /*height: 400px;*/
  max-height: 400px;
}

.notifications-v2-modal {
  width: 100%;
  /*height: 400px;*/
  max-height: 400px;
}

.notifications::-webkit-scrollbar {
  width: 6px;               /* width of the entire scrollbar */
}

.notifications::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

.notifications::-webkit-scrollbar-thumb {
  background-color: #eeeeee;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid transparent;  /* creates padding around scroll thumb */
}

.request-modal {
  width: 100%;
}

.connect-modal {
  width: 100%;
}

.settings-modal {
  width: 100%;
}
</style>