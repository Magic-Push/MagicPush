import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index.js'

import AuthLayout from '@/layouts/AuthLayout.vue';
import DashboardLayout from "@/layouts/DashboardLayout";

import DashboardPage from "@/pages/dashboard/DashboardPage";
import BillingPage from "@/pages/dashboard/BillingPage";
import UserSettingsPage from "@/pages/dashboard/UserSettingsPage";
import LoginPage from "@/pages/auth/LoginPage";
import SignupPage from "@/pages/auth/SignupPage";
import PasswordForgetPage from "@/pages/auth/PasswordForgetPage";
import SchedulerPage from "@/pages/dashboard/SchedulerPage.vue";
import FlowsPage from "@/pages/dashboard/FlowsPage";
import FlowBuilderPage from "@/pages/dashboard/FlowBuilderPage";
import OnboardingLayout from "@/layouts/OnboardingLayout";
import CreateAppPage from "@/pages/onboarding/CreateAppPage";
import SetupNotificationsPage from "@/pages/onboarding/SetupNotificationsPage";
import AppSettingsPage from "@/pages/dashboard/AppSettingsPage";
import ButtonPage from "@/pages/library/ButtonPage";
import ModalPage from "@/pages/library/ModalPage";
import LibLayout from "@/layouts/LibLayout";
import NotificationsPage from "@/pages/dashboard/NotificationsPage.vue";
import ResetPasswordPage from "@/pages/auth/ResetPasswordPage.vue";
import AdminDashboardPage from "@/pages/dashboard/AdminDashboardPage.vue";

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/dashboard',
    name: 'Dashboard layout',
    meta: { requiresAuth: true, requiresOnboarding: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: DashboardPage
      },
      {
        path: 'billing',
        name: 'Billing',
        component: BillingPage
      },
      {
        path: 'app-settings',
        name: 'App Settings',
        component: AppSettingsPage
      },
      {
        path: 'user-settings',
        name: 'User Settings',
        component: UserSettingsPage
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: NotificationsPage
      },
      {
        path: 'scheduler',
        name: 'Scheduler',
        component: SchedulerPage
      },
      {
        path: 'flows',
        name: 'Flows',
        component: FlowsPage
      },
      {
        path: 'builder/:id',
        name: 'Flow Builder',
        component: FlowBuilderPage
      },
      {
        path: 'admin',
        name: 'Admin',
        component: AdminDashboardPage,
      }
    ]
  },
  {
    path: '/auth',
    component: AuthLayout,
    redirect: '/auth/login',
    name: 'Authentication',
    meta: { hideOnAuth: true },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: LoginPage
      },
      {
        path: 'signup',
        name: 'Signup',
        component: SignupPage
      },
      {
        path: 'forget',
        name: 'Password Forget',
        component: PasswordForgetPage
      },
      {
        path: 'reset/:token',
        name: 'Password Reset',
        component: ResetPasswordPage,
      }
    ]
  },
  {
    path: '/onboarding',
    component: OnboardingLayout,
    redirect: '/onboarding/create',
    name: 'Onboarding',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'create',
        name: 'Create App',
        component: CreateAppPage
      },
      {
        path: 'setup/:id',
        name: 'Setup Notifications',
        component: SetupNotificationsPage
      }
    ]
  },
  {
    path: '/lib',
    component: LibLayout,
    redirect: '/lib/button',
    name: 'Lib',
    children: [
      {
        path: 'button/:appId',
        name: 'Button',
        component: ButtonPage
      },
      {
        path: 'modal/:appId',
        name: 'Modal',
        component: ModalPage
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    //Logic to prevent user accessing pages with meta requiresAuth true
    console.log("requiresAuth");
    console.log(store.getters.isLoggedIn);
    if (store.getters.isLoggedIn === true) {
      if (to.matched.some(record => record.meta.requiresOnboarding)) {
        next();
      } else {
        console.log("isLoggedIn");
        next();
      }
    } else if (store.getters.isLoggedIn === undefined) {
      //TODO add timeout to this and the others
      const watcher = store.watch(() => store.getters.isLoggedIn, isLoggedIn => {
        watcher(); // stop watching
        if (isLoggedIn) {
          if (to.matched.some(record => record.meta.requiresOnboarding)) {
            next();
          } else {
            console.log("isLoggedIn");
            next();
          }
        } else {
          console.log("go to login!");
          next({path: 'auth/login', query: {nextUrl: to.fullPath}});
        }
      });
    } else {
      console.log("go to login");
      next({path: 'auth/login', query: {nextUrl: to.fullPath}})
    }
  } else if (to.matched.some(record => record.meta.hideOnAuth)) {
    if (store.getters.isLoggedIn === true) {
      if (to.query.buylifetime !== undefined && to.query.buylifetime === "true") {
        // get billing url from env
        // window.location.href = process.env.BILLING_URL_DEAL;
        next({ path: 'dashboard', query: { buylifetime: 'true' }});
      } else {
        next('dashboard');
      }
    } else if (store.getters.isLoggedIn === undefined) {
      const watcher = store.watch(() => store.getters.isLoggedIn, isLoggedIn => {
        watcher(); // stop watching
        if (isLoggedIn) {
          if (to.query.buylifetime !== undefined && to.query.buylifetime === "true") {
            // get billing url from env
            // window.location.href = process.env.BILLING_URL_DEAL;
            next({ path: 'dashboard', query: { buylifetime: 'true' }});
          } else {
            next('dashboard');
          }
        } else {
          next();
        }
      });
    } else {
      next();
    }
  } else next();
});

router.afterEach(() => {

});

export default router;
