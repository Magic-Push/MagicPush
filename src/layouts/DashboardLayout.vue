<template>
  <div class="main" v-if="allApps !== null">
    <div class="relative">
      <SideBar v-on:createProject="createProject"/>
      <div class="sm:ml-64" v-if="selectedApp !== null">
        <router-view :key="$route.fullPath"></router-view>
      </div>
      <SetupBillingModal v-bind:open="showBillingModal" v-on:onClose="showBillingModal = false"/>
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar";
import SetupBillingModal from "@/modals/SetupBillingModal.vue";
export default {
  name: "DashboardLayout",
  components: {SetupBillingModal, SideBar},
  data() {
    return {
      hasFreeTier: false,
      showBillingPanel: false,
      showBillingModal: false
    }
  },
  mounted() {
    let self = this;
    if (this.currentUser === null) {
      this.$store.dispatch('getUserDetails')
          .then((response) => {
            if (self.$route.query.buylifetime !== undefined && self.$route.query.buylifetime === "true") {
              self.$store.dispatch('purchaseDeal')
                  .then((response) => {
                    window.location.href = response.data.url
                  })
                  .catch((error) => {
                    console.log(error);
                  });
            }
          })
          .catch((error) => {
            console.log(error);
          });
    } else {
      if (self.$route.query.buylifetime !== undefined && self.$route.query.buylifetime === "true") {
        self.$store.dispatch('purchaseDeal')
            .then((response) => {
              window.location.href = response.data.url
            })
            .catch((error) => {
              console.log(error);
            });
      }
    }
    if (this.$store.state.apps === null) {
      this.$store.dispatch('getApps')
          .then((response) => {
            if (response.data.apps.length === 0) {
              self.$router.push({path: "/onboarding/create"});
            }
          })
          .catch((error) => {
            console.log(error);
          });
    }
    this.$store.dispatch('getBilling')
        .then((response) => {
          if (response.data.has_purchased_deal === false && response.data.has_payment_method === false) {
            self.showBillingModal = true;
          }
        })
        .catch((error) => {
          console.log(error);
        });

    this.$magicpush.initialize({
      appId: 'd2316d92-a119-4fa4-bce0-1a0755699a94',
      swUrl: '/js/MagicPushSW.js',
      showButton: true,
      autoShowModal: true,
    });

    this.$magicpush.addListener((data) => {
      console.log("MagicPush listener: ");
      console.log(data);
    });
  },
  methods: {
    createProject() {
      // this.$router.push({path: "/app/editor"});
    }
  },
  computed: {
    selectedApp() {
      return this.$store.state.selectedApp;
    },
    allApps() {
      return this.$store.state.apps;
    },
    currentUser() {
      return this.$store.state.auth.user;
    }
  }
}
</script>

<style scoped>

</style>