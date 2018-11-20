// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import axios from 'axios'
import('vuetify/dist/vuetify.min.css')
import('./assets/css/materiel.fonts.css')
import('./assets/css/fonts/2fcrYFNaTjcS6g4U3t-Y5ZjZjT5FdEJ140U2DJYC3mY.woff2')
import('./assets/css/fonts/0eC6fl06luXEYWpBSJvXCBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/Fl4y0QdOxyyTHEGMXX8kcRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/-L14Jk06m6pUHB-5mXQQnRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/I3S1wsgSg9YCurV6PUkTORJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/NYDWBdD4gIq26G5XYbHsFBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/Pru33qjShpZSmG3z6VYwnRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/Hgo13k-tfSpn0qi1SFdUfVtXRa8TVwTICgirnJhmVJw.woff2')
import('./assets/css/fonts/ek4gzZ-GeXAPcSbHtCeQI_esZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/mErvLBYg_cXG3rLvUsKT_fesZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/-2n2p-_Y08sg57CNWQfKNvesZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/u0TOpm082MNkS5K0Q4rhqvesZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/NdF9MtnOpLzo-noMoG0miPesZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/Fcx7Wwv8OzT71A3E1XOAjvesZW2xOQ-xsNqO47m55DA.woff2')
import('./assets/css/fonts/CWB0XYA8bzo0kSThX0UTuA.woff2')
import('./assets/css/fonts/ZLqKeelYbATG60EpZBSDyxJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/oHi30kwQWvpCWqAhzHcCSBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/rGvHdJnr2l75qb0YND9NyBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/mx9Uck6uB63VIKFYnEMXrRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/mbmhprMH69Zi6eEPBYVFhRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/oOeFwZNlrTefzLYmlVV1UBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/RxZJdnzeo3R5zSexge8UUVtXRa8TVwTICgirnJhmVJw.woff2')
import('./assets/css/fonts/77FXFjRbGzN4aCrSFhlh3hJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/isZ-wbCXNKAbnjo6_TwHThJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/UX6i4JxQDm3fVTc1CPuwqhJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/jSN2CGVDbcVyCnfJfjSdfBJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/PwZc-YbIL414wB9rB1IAPRJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/97uahxiqZRoncBaCEI3aWxJtnKITppOI_IvcXXDNrsc.woff2')
import('./assets/css/fonts/d-6IYplOFocCacKzxwXSOFtXRa8TVwTICgirnJhmVJw.woff2')
import('./assets/css/font-awesome.css')
import('./assets/css/fonts/fontawesome-webfont.eot')
import('./assets/css/fonts/fontawesome-webfont.eot?#iefix')
import('./assets/css/fonts/fontawesome-webfont.woff2')
import('./assets/css/fonts/fontawesome-webfont.woff')
import('./assets/css/fonts/fontawesome-webfont.ttf')
import('./assets/css/fonts/fontawesome-webfont.svg')

Vue.use(router)
Vue.use(Vuetify)
Vue.use(axios)

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
}).$mount('#app')
