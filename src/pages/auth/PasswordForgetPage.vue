<template>
  <!--
    This example requires updating your template:

    ```
    <html class="h-full bg-gray-50">
    <body class="h-full">
    ```
  -->
  <div class="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-10 w-auto" src="/images/magicpushlogo.png" alt="Your Company" />
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Request password reset</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
        <div class="space-y-6" >
          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
            <div class="mt-2">
              <input v-model="email" id="email" name="email" type="email" autocomplete="email" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div>
            <button @click="postForget" type="submit" class="flex w-full justify-center rounded-md bg-primary-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">Request reset</button>
          </div>
        </div>
      </div>

      <p class="mt-10 text-center text-sm text-gray-500">
        Remember it again?
        {{ ' ' }}
        <a href="/auth/login" class="font-semibold leading-6 text-primary-600 hover:text-primary-500">Login</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "PasswordForgetPage",
  data() {
    return {
      email: null
    }
  },
  methods: {
    postForget() {
      this.$store.dispatch('postRequestResetPassword', {
        email: this.email
      })
          .then((res) => {
            alert('Password reset link sent to your email');
          })
          .catch((err) => {
            alert('Error sending password reset link');
          })
    }
  }
}
</script>

<style scoped>
.forget {
  margin-top: 5rem;
  margin-left: auto;
  margin-right: auto;
}
</style>