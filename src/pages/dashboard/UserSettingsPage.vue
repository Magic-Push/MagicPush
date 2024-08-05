<template>
  <div v-if="user" class="p-4 border-gray-100 h-screen" style="border-left-style: solid; border-left-width: 0;">
    <h1 class="font-medium text-xl text-slate-900">
      User Settings
    </h1>

    <div class="mt-4 pb-4">
      <div>
        <div class="space-y-12 sm:space-y-16">
          <div>
            <div class="mt-10 space-y-8 border-b border-gray-900/10 pb-12 sm:space-y-0 sm:divide-y sm:divide-gray-900/10 sm:border-t sm:pb-0">
              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Name</label>
                <div class="mt-2 sm:col-span-2 sm:mt-0">
                  <input v-model="user.name" type="text" name="name" id="name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:max-w-xs sm:text-sm sm:leading-6" />
                </div>
              </div>
              <div class="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 sm:py-6">
                <label for="app-name" class="block text-sm font-medium leading-6 text-gray-900 sm:pt-1.5">Email</label>
                <div class="mt-2 sm:col-span-2 sm:mt-0">
                  <input v-model="user.email" type="email" name="email" id="email" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:max-w-xs sm:text-sm sm:leading-6" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 flex items-center justify-end gap-x-6">
          <button @click="updateUser" class="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserSettings",
  data() {
    return {
      user: null,
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user
    }
  },
  mounted() {
    if (this.currentUser) {
      this.user = this.currentUser
    } else {
      let self = this;
      this.$store.watch(() => this.$store.getters.currentUser, (newVal) => {
        self.user = newVal
      })
    }
  },
  methods: {
    updateUser() {
      this.$store.dispatch('updateUserDetails', this.user)
          .then((response) => {
            alert('User updated successfully');
          })
          .catch((error) => {
            console.log(error);
          });
    }
  }
}
</script>

<style scoped>

</style>