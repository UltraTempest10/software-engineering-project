import { createRouter, createWebHashHistory } from 'vue-router'
import FramePlayer from '../views/FramePlayer.vue'
import DataView from '../views/DataView.vue'

const routes = [
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
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
