import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import vuetify from "./plugins/vuetify";
Vue.config.productionTip = false;
import { firestorePlugin } from 'vuefire'

Vue.use(firestorePlugin)

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
