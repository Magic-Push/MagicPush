<template>
  <div class="p-4 border-gray-100 h-screen" style="border-left-style: solid; border-left-width: 0;">
    <h1 class="font-normal text-2xl text-slate-900">Billing</h1>
    <span class="font-normal text-slate-500">Manage your payment methods and subscription</span>

    <div class="payment-methods mt-4">
      <h2 class="font-medium text-lg text-slate-800">Payment methods</h2>
      <div class="grid grid-cols-3 gap-4 mt-4">
        <div class="bg-slate-50 rounded-lg shadow-md p-4">
          <div class="justify-between items-center">
            <div class="image"></div>
            <h1 class="font-medium text-lg text-slate-800 w-full">Visa **** 1234</h1>
            <span class="text-xs text-slate-400 w-full">Expires: 12/2023</span>
          </div>
        </div>
      </div>

      <button class="mt-4 bg-primary-500 hover:bg-primary-600 focus:ring-4 focus:outline-none focus:ring-primary-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center text-white" @click="showAddPaymentMethod">
        Add payment method
      </button>
    </div>

    <div class="subscription mt-4">
      <h2 class="font-medium text-lg text-slate-800">Subscription</h2>
      <div class="bg-slate-50 rounded-lg shadow-md p-4 mt-4">
        <div class="justify-between items-center">
          <h1 class="font-medium text-lg text-slate-800 w-full">Premium</h1>
          <span class="text-xs text-slate-400 w-full">Expires: 12/2023</span>
        </div>
        <div class="justify-between items-baseline">
          <button class="bg-transparent text-slate-600">
            Manage subscription
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BillingPage",
  methods: {
    showAddPaymentMethod() {
      console.log("Show add payment method");
    }
  }
}
</script>

<style scoped>

</style>