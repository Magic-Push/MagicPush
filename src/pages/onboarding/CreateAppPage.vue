<template>
  <div>
    <div class="login w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
      <div class="bg-gray-50 p-8">
        <div class="flex items-start justify-between space-x-6">
          <div class="space-y-1">
            <h1 class="text-base font-semibold leading-6 text-gray-900">
              {{ apps === null || apps.length === 0 ? 'Create your first app' : 'Add a new app' }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ apps === null || apps.length === 0 ? 'Let\'s get started by creating your first app.' : 'Add a new app to your account.'}}
            </p>
          </div>
        </div>
      </div>
      <div class="p-8 space-y-4 md:space-y-6">
<!--        <h1 class="text-base font-semibold leading-6 text-gray-900">-->
<!--          Create your first app-->
<!--        </h1>-->
        <div class="space-y-4">
          <div>
            <label for="project-name" class="block text-sm font-medium leading-6 text-gray-900">Name</label>
            <div class="mt-2">
              <input v-model="name" type="text" name="project-name" id="project-name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
          <div>
            <label for="name" class="block mb-2 text-sm font-medium text-gray-900">Available on</label>
            <div class="flex items-center">
              <div class="flex items-center h-5">
                <input v-model="web" id="web" aria-describedby="web" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600">
              </div>
              <div class="ml-3 text">
                <label for="web" class="text-gray-600">Web</label>
              </div>
            </div>

            <div class="flex items-center">
              <div class="flex items-center h-5">
                <input v-model="android" id="android" aria-describedby="android" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600">
              </div>
              <div class="ml-3 text">
                <label for="android" class="text-gray-600">Android</label>
              </div>
            </div>

            <div class="flex items-center">
              <div class="flex items-center h-5">
                <input v-model="ios" id="ios" aria-describedby="ios" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600">
              </div>
              <div class="ml-3 text">
                <label for="ios" class="text-gray-600">iOS</label>
              </div>
            </div>
          </div>
          <button @click="createAppClicked" type="submit" class="rounded-md w-full bg-primary-600 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500">
            Create App
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CreateAppPage",
  data() {
    return {
      name: null,
      web: false,
      android: false,
      ios: false
    }
  },
  computed: {
    apps() {
      return this.$store.state.apps;
    }
  },
  methods: {
    createAppClicked() {
      let self = this;

      if (this.web === true || this.android === true || this.ios === true) {
        let appData = {
          name: this.name,
          has_web: this.web,
          has_android: this.android,
          has_ios: this.ios
        }
        this.$store.dispatch("createApp", appData)
            .then((response) => {
              self.$router.push({ name: "Setup Notifications", params: { id: response.data.id } })
            })
            .catch((err) => {
              alert(err);
            });
      } else {
        alert("Please select at least one platform");
      }
    }
  }
}
</script>

<style scoped>
.login {
  margin-top: 5rem;
  margin-left: auto;
  margin-right: auto;
}
</style>