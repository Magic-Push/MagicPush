import axios from 'axios';
import { createStore } from 'vuex';
import router from '../routes/routes';

const store = createStore({
    state() {
        return {
            apps: null,
            selectedApp: null,
            scheduleData: [],
            flowsData: [],
            notificationsData: null,
            user: {},
            has_free_tier: true,
            has_payment_method: true,
            auth: {
                token: localStorage.getItem('jwt') || '',
                status: '',
                user: null,
                loginDetails: {},
                loggedIn: localStorage.getItem('jwt') !== null,
            },
            host: process.env.VUE_APP_SERVER_URL,
            languages: [
                {name: "Afrikaans", code: "af"},
                {name: "Albanian - shqip", code: "sq"},
                {name: "Amharic - አማርኛ", code: "am"},
                {name: "Arabic - العربية", code: "ar"},
                {name: "Aragonese - aragonés", code: "an"},
                {name: "Armenian - հայերեն", code: "hy"},
                {name: "Asturian - asturianu", code: "ast"},
                {name: "Azerbaijani - azərbaycan dili", code: "az"},
                {name: "Basque - euskara", code: "eu"},
                {name: "Belarusian - беларуская", code: "be"},
                {name: "Bengali - বাংলা", code: "bn"},
                {name: "Bosnian - bosanski", code: "bs"},
                {name: "Breton - brezhoneg", code: "br"},
                {name: "Bulgarian - български", code: "bg"},
                {name: "Catalan - català", code: "ca"},
                {name: "Central Kurdish - کوردی (دەستنوسی عەرەبی)", code: "ckb"},
                {name: "Chinese - 中文", code: "zh"},
                {name: "Chinese (Hong Kong) - 中文（香港）", code: "zh-HK"},
                {name: "Chinese (Simplified) - 中文（简体）", code: "zh-CN"},
                {name: "Chinese (Traditional) - 中文（繁體）", code: "zh-TW"},
                {name: "Corsican", code: "co"},
                {name: "Croatian - hrvatski", code: "hr"},
                {name: "Czech - čeština", code: "cs"},
                {name: "Danish - dansk", code: "da"},
                {name: "Dutch - Nederlands", code: "nl"},
                {name: "English", code: "en"},
                {name: "English (Australia)", code: "en-AU"},
                {name: "English (Canada)", code: "en-CA"},
                {name: "English (India)", code: "en-IN"},
                {name: "English (New Zealand)", code: "en-NZ"},
                {name: "English (South Africa)", code: "en-ZA"},
                {name: "English (United Kingdom)", code: "en-GB"},
                {name: "English (United States)", code: "en-US"},
                {name: "Esperanto - esperanto", code: "eo"},
                {name: "Estonian - eesti", code: "et"},
                {name: "Faroese - føroyskt", code: "fo"},
                {name: "Filipino", code: "fil"},
                {name: "Finnish - suomi", code: "fi"},
                {name: "French - français", code: "fr"},
                {name: "French (Canada) - français (Canada)", code: "fr-CA"},
                {name: "French (France) - français (France)", code: "fr-FR"},
                {name: "French (Switzerland) - français (Suisse)", code: "fr-CH"},
                {name: "Galician - galego", code: "gl"},
                {name: "Georgian - ქართული", code: "ka"},
                {name: "German - Deutsch", code: "de"},
                {name: "German (Austria) - Deutsch (Österreich)", code: "de-AT"},
                {name: "German (Germany) - Deutsch (Deutschland)", code: "de-DE"},
                {name: "German (Liechtenstein) - Deutsch (Liechtenstein)", code: "de-LI"},
                {name: "German (Switzerland) - Deutsch (Schweiz)", code: "de-CH"},
                {name: "Greek - Ελληνικά", code: "el"},
                {name: "Guarani", code: "gn"},
                {name: "Gujarati - ગુજરાતી", code: "gu"},
                {name: "Hausa", code: "ha"},
                {name: "Hawaiian - ʻŌlelo Hawaiʻi", code: "haw"},
                {name: "Hebrew - עברית", code: "he"},
                {name: "Hindi - हिन्दी", code: "hi"},
                {name: "Hungarian - magyar", code: "hu"},
                {name: "Icelandic - íslenska", code: "is"},
                {name: "Indonesian - Indonesia", code: "id"},
                {name: "Interlingua", code: "ia"},
                {name: "Irish - Gaeilge", code: "ga"},
                {name: "Italian - italiano", code: "it"},
                {name: "Italian (Italy) - italiano (Italia)", code: "it-IT"},
                {name: "Italian (Switzerland) - italiano (Svizzera)", code: "it-CH"},
                {name: "Japanese - 日本語", code: "ja"},
                {name: "Kannada - ಕನ್ನಡ", code: "kn"},
                {name: "Kazakh - қазақ тілі", code: "kk"},
                {name: "Khmer - ខ្មែរ", code: "km"},
                {name: "Korean - 한국어", code: "ko"},
                {name: "Kurdish - Kurdî", code: "ku"},
                {name: "Kyrgyz - кыргызча", code: "ky"},
                {name: "Lao - ລາວ", code: "lo"},
                {name: "Latin", code: "la"},
                {name: "Latvian - latviešu", code: "lv"},
                {name: "Lingala - lingála", code: "ln"},
                {name: "Lithuanian - lietuvių", code: "lt"},
                {name: "Macedonian - македонски", code: "mk"},
                {name: "Malay - Bahasa Melayu", code: "ms"},
                {name: "Malayalam - മലയാളം", code: "ml"},
                {name: "Maltese - Malti", code: "mt"},
                {name: "Marathi - मराठी", code: "mr"},
                {name: "Mongolian - монгол", code: "mn"},
                {name: "Nepali - नेपाली", code: "ne"},
                {name: "Norwegian - norsk", code: "no"},
                {name: "Norwegian Bokmål - norsk bokmål", code: "nb"},
                {name: "Norwegian Nynorsk - nynorsk", code: "nn"},
                {name: "Occitan", code: "oc"},
                {name: "Oriya - ଓଡ଼ିଆ", code: "or"},
                {name: "Oromo - Oromoo", code: "om"},
                {name: "Pashto - پښتو", code: "ps"},
                {name: "Persian - فارسی", code: "fa"},
                {name: "Polish - polski", code: "pl"},
                {name: "Portuguese - português", code: "pt"},
                {name: "Portuguese (Brazil) - português (Brasil)", code: "pt-BR"},
                {name: "Portuguese (Portugal) - português (Portugal)", code: "pt-PT"},
                {name: "Punjabi - ਪੰਜਾਬੀ", code: "pa"},
                {name: "Quechua", code: "qu"},
                {name: "Romanian - română", code: "ro"},
                {name: "Romanian (Moldova) - română (Moldova)", code: "mo"},
                {name: "Romansh - rumantsch", code: "rm"},
                {name: "Russian - русский", code: "ru"},
                {name: "Scottish Gaelic", code: "gd"},
                {name: "Serbian - српски", code: "sr"},
                {name: "Serbo - Croatian", code: "sh"},
                {name: "Shona - chiShona", code: "sn"},
                {name: "Sindhi", code: "sd"},
                {name: "Sinhala - සිංහල", code: "si"},
                {name: "Slovak - slovenčina", code: "sk"},
                {name: "Slovenian - slovenščina", code: "sl"},
                {name: "Somali - Soomaali", code: "so"},
                {name: "Southern Sotho", code: "st"},
                {name: "Spanish - español", code: "es"},
                {name: "Spanish (Argentina) - español (Argentina)", code: "es-AR"},
                {name: "Spanish (Latin America) - español (Latinoamérica)", code: "es-419"},
                {name: "Spanish (Mexico) - español (México)", code: "es-MX"},
                {name: "Spanish (Spain) - español (España)", code: "es-ES"},
                {name: "Spanish (United States) - español (Estados Unidos)", code: "es-US"},
                {name: "Sundanese", code: "su"},
                {name: "Swahili - Kiswahili", code: "sw"},
                {name: "Swedish - svenska", code: "sv"},
                {name: "Tajik - тоҷикӣ", code: "tg"},
                {name: "Tamil - தமிழ்", code: "ta"},
                {name: "Tatar", code: "tt"},
                {name: "Telugu - తెలుగు", code: "te"},
                {name: "Thai - ไทย", code: "th"},
                {name: "Tigrinya - ትግርኛ", code: "ti"},
                {name: "Tongan - lea fakatonga", code: "to"},
                {name: "Turkish - Türkçe", code: "tr"},
                {name: "Turkmen", code: "tk"},
                {name: "Twi", code: "tw"},
                {name: "Ukrainian - українська", code: "uk"},
                {name: "Urdu - اردو", code: "ur"},
                {name: "Uyghur", code: "ug"},
                {name: "Uzbek - o‘zbek", code: "uz"},
                {name: "Vietnamese - Tiếng Việt", code: "vi"},
                {name: "Walloon - wa", code: "wa"},
                {name: "Welsh - Cymraeg", code: "cy"},
                {name: "Western Frisian", code: "fy"},
                {name: "Xhosa", code: "xh"},
                {name: "Yiddish", code: "yi"},
                {name: "Yoruba - Èdè Yorùbá", code: "yo"},
                {name: "Zulu - isiZulu", code: "zu"}
            ]
        }
    },
    getters: {
        isLoggedIn(state) {
            return state.auth.loggedIn;
        },
        jwtToken(state) {
            return state.auth.token;
        },
        isOnboarded(state) {
            if (state.apps === undefined)
                return undefined;
            return state.apps.length > 0;
        },
        currentApp(state){
            return state.selectedApp;
        },
        languages(state) {
            return state.languages;
        },
        getFlows(state) {
            return state.flowsData;
        }
    },
    actions: {
        userShouldHaveBeenLoggedOut({commit}) {
            commit('setUserLoggedInStatus', false);
            commit('removeJwt');
            router.push('/auth/login')
        },
        postLogin({commit}, loginData) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/login', loginData)
                    .then(function (response) {
                        commit('setJwt', response.data.token);
                        commit('setUserLoggedInStatus', true);
                        resolve(response);
                    })
                    .catch(function (error) {
                        commit('authError');
                        console.log(error);
                        reject(error);
                    })
            });
        },
        postSignup({commit}, signUpData) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/signup', signUpData)
                    .then(function (response) {
                        commit('setJwt', response.data.token);
                        commit('setUserLoggedInStatus', true);
                        resolve(response);
                    })
                    .catch(function (error) {
                        commit('authError');
                        console.log(error);
                        reject(error);
                    })
            });
        },
        postRequestResetPassword({commit}, requestData) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/request-reset', requestData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        postPasswordReset({commit}, requestData) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/users/reset/${requestData['token']}`, requestData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getUserDetails({commit}) {
            return new Promise((resolve, reject) => {
                axios.get('/api/v1/users')
                    .then(function (response) {
                        commit('setUserDetails', response.data);
                        commit('setUserLoggedInStatus', true);
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getBilling({commit}) {
            return new Promise((resolve, reject) => {
                axios.get('/api/v1/users/billing')
                    .then(function (response) {
                        commit('setHasFreeTier', response.data.has_free_tier);
                        commit('setHasPaymentMethod', response.data.has_payment_method);
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        setupBilling({commit}) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/billing')
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getBillingPortal({commit}) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/billing-portal')
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        purchaseDeal({commit}) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/users/purchase-deal')
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        updateUserDetails({commit}, userData) {
            return new Promise((resolve, reject) => {
                axios.put('/api/v1/users', userData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getApps({commit}) {
            return new Promise((resolve, reject) => {
                axios.get('/api/v1/apps')
                    .then(function (response) {
                        commit('setApps', response.data.apps);
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getApp({commit}, appId) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/apps/${appId}`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        createApp({commit}, appData) {
            return new Promise((resolve, reject) => {
                axios.post('/api/v1/apps', appData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        updateApp({commit}, appData) {
            return new Promise((resolve, reject) => {
                axios.put(`/api/v1/apps/${appData.id}`, appData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        generateApiKey({state, commit}) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/apps/${state.selectedApp.id}/generate-token`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getInfo({state, commit}, paramsObj) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/statistics/${state.selectedApp.id}/info`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getSubscriberStats({state, commit}) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/statistics/${state.selectedApp.id}/subscribers`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getAdminInfo({state, commit}, paramsObj) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/admin/info`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getAdminSubscriberStats({state, commit}) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/admin/subscribers`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getAdminMessagesStats({state, commit}) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/admin/messages`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getNotifications({state, commit}, paramsObj) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/notifications/${state.selectedApp.id}`, {params: paramsObj})
                    .then(function (response) {
                        commit('setNotificationsData', response.data);
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        createNotification({state, commit}, notificationData) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/notifications/${state.selectedApp.id}`, notificationData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        updateNotification({state, commit}, notificationData) {
            return new Promise((resolve, reject) => {
                axios.put(`/api/v1/notifications/${state.selectedApp.id}/${notificationData.id}`, notificationData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        uploadImage({state, commit}, formData) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/notifications/${state.selectedApp.id}/image`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(function (response) {
                    resolve(response);
                })
                .catch(function (error) {
                    console.log(error);
                    reject(error);
                })
            });
        },
        getScheduledNotifications({state, commit}, paramsObj) {
            // console.log("selected app id: " + this.state.selectedApp.id)
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/scheduler/${state.selectedApp.id}`, {params: paramsObj})
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getFlows({state, commit}) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/flows/${state.selectedApp.id}`)
                    .then(function (response) {
                        commit('setFlowsData', response.data);
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getFlow({state, commit}, flowId) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/flows/${state.selectedApp.id}/${flowId}`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        createFlow({state, commit}, flowData) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/flows/${state.selectedApp.id}`, flowData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        updateFlow({state, commit}, flowData) {
            return new Promise((resolve, reject) => {
                axios.put(`/api/v1/flows/${state.selectedApp.id}/${flowData.id}`, flowData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        deleteFlow({state, commit}, flowData) {
            return new Promise((resolve, reject) => {
                axios.delete(`/api/v1/flows/${state.selectedApp.id}/${flowData.id}`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getAppFromLib({state, commit}, appHash) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/sdk/app-by-hash/${appHash}`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        getAppUser({state, commit}, userData) {
            return new Promise((resolve, reject) => {
                axios.get(`/api/v1/sdk/app-user/${userData['appHash']}/${userData['userHash']}`)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        createAppUser({state, commit}, userData) {
            return new Promise((resolve, reject) => {
                axios.post(`/api/v1/sdk/app-user/${userData['appHash']}`, userData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        },
        updateAppUser({state, commit}, userData) {
            return new Promise((resolve, reject) => {
                axios.put(`/api/v1/sdk/app-user/${userData['appHash']}/${userData['userHash']}`, userData)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                        reject(error);
                    })
            });
        }
    },
    mutations: {
        setSelectedApp(state, app) {
            state.selectedApp = app;
            state.scheduleData = [];
            state.flowsData = [];
        },
        setJwt(state, token) {
            console.log('jwt', token);
            localStorage.setItem('jwt', token);
            axios.defaults.headers.common = {
                'Authorization': `Bearer ${token}`
            }
            state.auth.token = token;
        },
        removeJwt() {
            localStorage.removeItem('jwt')
        },
        setUserDetails(state, user) {
            state.auth.user = user;
        },
        setHasFreeTier(state, hasFreeTier) {
            state.has_free_tier = hasFreeTier;
        },
        setHasPaymentMethod(state, hasPaymentMethod) {
            state.has_payment_method = hasPaymentMethod;
        },
        setUserLoggedInStatus(state, status) {
            state.auth.loggedIn = status;
        },
        authError(state) {
            state.auth.loggedIn = false;
        },
        setApps(state, apps) {
            state.apps = apps;
        },
        setScheduleData(state, data) {
            state.scheduleData = data;
        },
        setFlowsData(state, data) {
            state.flowsData = data;
        },
        setNotificationsData(state, data) {
            state.notificationsData = data;
        }
    }
})

export default store