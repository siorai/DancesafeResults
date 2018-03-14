import Vue from 'vue'
import Router from 'vue-router'
import Adduser from '@/components/add-user'
import Addevent from '@/components/add-event'
import Newsurvey from '@/components/new-survey'
import chart from '@/components/chartpie'

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/add-user', component: Adduser, name: 'Adduser'},
    {path: '/add-event', component: Addevent, name: 'Addevent'},
    {path: '/new-survey', component: Newsurvey, name: 'Newsurvey'},
    {path: '/pie-chart', component: chart, name: 'Chartpie'}
  ],
  mode: 'history'
})
