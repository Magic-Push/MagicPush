<template>
  <div class="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-10 w-auto" src="/images/magicpushlogo.png" alt="Your Company" />
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Get started with MagicPush</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
        <div class="space-y-6">
          <div>
            <label for="name" class="block text-sm font-medium leading-6 text-gray-900">First & last name</label>
            <div class="mt-2">
              <input v-model="fullName" id="name" name="name" type="text" autocomplete="name" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
            <div class="mt-2">
              <input v-model="email" id="email" name="email" type="email" autocomplete="email" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
            <div class="mt-2">
              <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div>
            <button @click="postSignUp" type="submit" class="flex w-full justify-center rounded-md bg-primary-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">Sign up</button>
          </div>
        </div>
      </div>

      <p class="mt-10 text-center text-sm text-gray-500">
        Already a member?
        {{ ' ' }}
        <a href="/auth/login" class="font-semibold leading-6 text-primary-600 hover:text-primary-500">Login instead</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupPage",
  data() {
    return {
      fullName: null,
      email: null,
      password: null
    }
  },
  methods: {
    postSignUp() {
      let self = this;

      let signupData = {
        name: this.fullName,
        email: this.email,
        password: this.password
      }
      this.$store.dispatch("postSignup", signupData)
          .then(() => {
            if (self.$route.query.buylifetime !== undefined && self.$route.query.buylifetime === "true") {
              self.$store.dispatch('purchaseDeal')
                  .then((response) => {
                    window.location.href = response.data.url
                  })
                  .catch((error) => {
                    console.log(error);
                  });
            } else {
              console.log("nextUrl", self.$route.query.nextUrl);
              self.$router.push(self.$route.query.nextUrl || "/dashboard")
            }
          }).catch((err) => {
            alert(err);
          });
    }
  }
}
</script>

<style scoped>
.signup {
  margin-top: 5rem;
  margin-left: auto;
  margin-right: auto;
}
</style>