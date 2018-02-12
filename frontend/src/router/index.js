import Vue from 'vue'
import Router from 'vue-router'
import Adduser from '@/components/add-user'
import Addevent from '@/components/add-event'

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/add-user', component: Adduser, name: 'Adduser'},
    {path: '/add-event', component: Addevent, name: 'Addevent'}
  ],
  mode: 'history'
})
