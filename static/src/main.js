import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import VueRouter from 'vue-router'

import {library} from '@fortawesome/fontawesome-svg-core'
import {faClone, faMinus} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(faClone, faMinus);
Vue.component('font-awesome-icon', FontAwesomeIcon);


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Departments from "./Components/Departments";
import Diagnoses from "./Components/Diagnoses";
import Patients from "./Components/Patients";
import SickLists from "./Components/SickLists";
import Main from "./Components/Main";
import Login from "./Components/Login";
import Consultants from "./Components/Consultants";

Vue.use(VueRouter)
Vue.use(BootstrapVue)


const routes = [
  {path: '/departments', component: Departments},
  {path: '/diagnoses', component: Diagnoses},
  {path: '/patients', component: Patients},
  {path: '/consultants', component: Consultants},
  {path: '/sick_lists', component: SickLists},
  {path: '/main', component: Main},
  {path: '/login', component: Login}
]


const router = new VueRouter({
  routes, // сокращённая запись для `routes: routes`
  mode: 'history'
})


new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
