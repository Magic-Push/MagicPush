<template>
  <TransitionRoot as="template" :show="open">
    <Dialog class="relative z-50">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-sm sm:p-6">
              <div>
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-100">
                  <CreditCardIcon class="h-6 w-6 text-primary-600" aria-hidden="true" />
                </div>
                <div class="mt-3 text-center sm:mt-5">
                  <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">
                    Add your billing details
                  </DialogTitle>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500" v-if="hasFreeTier">
                      The first 1000 subscribers are completely free of charge! But to prevent future service disruptions, please add your billing details now.
                    </p>
                    <p class="text-sm text-gray-500" v-else>
                      You have outgrown the free tier. We would love to continue serving you, but we need your billing details to do so.
                    </p>
                  </div>
                </div>
              </div>
              <div v-if="hasFreeTier" class="mt-5 sm:mt-6 flex columns-2 justify-between space-x-2">
                <button @click="$emit('onClose')" type="button" class="col-span-1 w-full justify-center rounded-md bg-gray-200 px-3 py-2 text-sm font-semibold text-gray-500 shadow-sm hover:bg-gray-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-400">
                  Dismiss
                </button>
                <button @click="setupBilling" type="button" class="col-span-1 w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
                  Continue
                </button>
              </div>
              <div v-else class="mt-5 sm:mt-6">
                <button @click="setupBilling" type="button" class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
                  Continue
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import { CreditCardIcon } from "@heroicons/vue/24/solid";
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'

export default {
  name: "SetupBillingModal",
  components: {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    CreditCardIcon
  },
  props: ['open'],
  computed: {
    checkoutUrl() {
      return this.$store.state.checkout_url;
    },
    currentUser() {
      return this.$store.state.auth.user;
    },
    hasFreeTier() {
      return this.$store.state.has_free_tier;
    }
  },
  methods: {
    setupBilling() {
      this.$store.dispatch('setupBilling')
          .then((res) => {
            window.location.href = res.data.url;
          })
          .catch((err) => {
            console.log(err);
          });
    }
  }
}
</script>

<style scoped>

</style>