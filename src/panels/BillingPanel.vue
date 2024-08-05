<template>
  <div class="bg-yellow-100 items-baseline">
    <div class="text-left">
      <h1 class="text-base font-semibold leading-6 text-gray-900">
        Please add your billing details
      </h1>
      <span class="text-sm leading-6 text-gray-600">
        First 1k subscribers are free. Add your billing details to prevent any service interruptions in the future.
      </span>
    </div>

    <button @click="setupBilling" type="button" class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">
      Setup Billing
    </button>
  </div>
</template>

<script>
export default {
  name: "BillingPanel",
  computed: {
    checkoutUrl() {
      return this.$store.state.checkout_url;
    },
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    setupBilling() {
      window.location.href = this.checkoutUrl + '?checkout[email]=' + this.currentUser.email + '&checkout[name]=' + this.currentUser.name;
    }
  }
}
</script>

<style scoped>

</style>