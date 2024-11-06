import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import DatabaseView from '@/views/DatabaseView.vue'
import PredictiveView from '@/views/PredictiveView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import LogOutView from '@/views/LogOutView.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import LogInView from '@/views/LogInView.vue'
import SettingView from '@/views/SettingView.vue'
import ContactView from '@/views/ContactView.vue'
import DocumentView from '@/views/DocumentView.vue'

import { useAuthStore } from '../stores/useAuthStore';
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/database',
    name: 'database',
    component: DatabaseView
  },
  {
    path: '/predictive',
    name: 'predictive',
    component: PredictiveView
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogOutView
  },
  {
    path: '/registration',
    name: 'registration',
    component: RegistrationView
  },
  {
    path: '/login',
    name: 'login',
    component: LogInView
  },
  {
    path: '/setting',
    name: 'setting',
    component: SettingView
  },
  {
    path: '/document',
    name: 'document',
    component: DocumentView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView
  },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: NotFoundView,
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Routing Protection:
// If user log out and trying to go back in the browser:
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // List of routes that require login
  const protectedRoutes = ["dashboard", "database", "predictive", "setting"];

  // Check if the route requires login
  if (protectedRoutes.includes(to.name) && !authStore.isLogin) {
    // If the user is not logged in, redirect to the home or login page
    next({ name: 'logout' });
  } else {
    // Otherwise, allow access
    next();
  }
});

export default router