<template>
  <div v-if="app" :style="`background-color: ${app.widget_color};`" class="button w-full h-full" @click="click">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7">
      <path fill-rule="evenodd" d="M5.25 9a6.75 6.75 0 0 1 13.5 0v.75c0 2.123.8 4.057 2.118 5.52a.75.75 0 0 1-.297 1.206c-1.544.57-3.16.99-4.831 1.243a3.75 3.75 0 1 1-7.48 0 24.585 24.585 0 0 1-4.831-1.244.75.75 0 0 1-.298-1.205A8.217 8.217 0 0 0 5.25 9.75V9Zm4.502 8.9a2.25 2.25 0 1 0 4.496 0 25.057 25.057 0 0 1-4.496 0Z" clip-rule="evenodd" />
    </svg>
  </div>
</template>

<script>
export default {
  name: "ButtonPage",
  data() {
    return {
      app: null,
    }
  },
  methods: {
    click() {
      window.parent.postMessage({ message: 'button-clicked' }, '*');
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
  }
}
</script>

<style scoped>
.button {
  cursor: pointer;
  background-color: #7c3aed;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 15px;
  width: 100%;
  height: 100vh;
}
</style>