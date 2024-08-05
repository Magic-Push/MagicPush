import './index.css';
import Axios from 'axios';
import App from './App.vue';
import { createApp } from 'vue';
import store from './store/index';
import 'element-plus/dist/index.css';
import router from './routes/routes';
import * as Sentry from "@sentry/vue";
import ElementPlus from 'element-plus';
import MagicPushVuePlugin from "magicpush-vue";

Axios.defaults.baseURL = process.env.VUE_APP_SERVER_URL;

const token = localStorage.getItem('jwt')
if (token) {
    Axios.defaults.headers.common = {
        'Authorization': `Bearer ${token}`
    }
}

const UNAUTHORIZED = 401;

Axios.interceptors.response.use(
    response => response,
    error => {
        //Log the error to Sentry
        // Sentry.captureException(error)

        const {status} = error.response || {};
        if (status === UNAUTHORIZED) {
            store.dispatch('userShouldHaveBeenLoggedOut');
        }
        return Promise.reject(error);
    }
);

const app = createApp(App,
    {
        // created() {
        //     this.$store.dispatch('getUserDetails')
        // }
    });

Sentry.init({
    app,
    dsn: "https://541aa89c0c2367ec360082b5bf44617a@o362710.ingest.us.sentry.io/4507385312706560",
    integrations: [
        Sentry.browserTracingIntegration(),
        Sentry.replayIntegration(),
    ],
    // Performance Monitoring
    tracesSampleRate: 1.0, //  Capture 100% of the transactions
    // Set 'tracePropagationTargets' to control for which URLs distributed tracing should be enabled
    tracePropagationTargets: ["localhost"],
    // Session Replay
    replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
    replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
});

app.use(store)
app.use(router)
app.use(ElementPlus)
app.use(MagicPushVuePlugin)

app.mount('#app')