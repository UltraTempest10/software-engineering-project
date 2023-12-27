import { createRouter, createWebHashHistory } from 'vue-router'
import FramePlayer from '../views/FramePlayer.vue'
import DataView from '../views/DataView.vue'
import AlarmView from '../views/AlarmView.vue'
import Home from '../views/Home.vue'
import PrivacyPolicy from '../components/PrivacyPolicy.vue'
import Error from '../views/Error.vue'
// import Login from '../views/Login.vue'

const routes = [
  {
    path:'/',
    redirect:"/Home"
  },
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  // {
  //   path: '/Login',
  //   name: 'Login',
  //   component: Login
  // },
  {
    path: '/PrivacyPolicy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy
  },
  {
    path: '/FramePlayer',
    name: 'FramePlayer',
    component: FramePlayer
  },
  {
    path: '/DataView',
    name: 'DataView',
    component: DataView
  },
  {
    path: '/AlarmView',
    name: 'AlarmView',
    component: AlarmView
  },
  {    
    path: '/404',
    name: '404',    
    component: Error,    
    hidden: true
  }, 
  // * at the end of the path
  {     
    path: '/:catchAll(.*)',
    redirect: '/404',
    hidden: true
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
