// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
// import GAuth from 'vue-google-oauth';
import VueAxios from 'vue-axios';
import VueAuthenticate from 'vue-authenticate';
import axios from 'axios';
import VueToastr2 from 'vue-toastr-2';
import VueStripeCheckout from 'vue-stripe-checkout';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import '@/assets/scss/bootstrap.cust.scss';
import 'bootstrap/dist/js/bootstrap.bundle';
import 'vue-toastr-2/dist/vue-toastr-2.min.css';

// FA icons
import { faUserCircle, faPlusCircle, faEdit, faTrash, faEraser,
  faSlash, faSquare, faPencilAlt, faFont, faDrawPolygon, faArrowsAlt,
  faEyeDropper, faCircle, faPalette, faPaperPlane,
  faComments, faUndo, faRedo, faTimes, faCheck, faSave,
  faBold, faItalic, faStrikethrough, faUnderline, faCode, faParagraph,
  faHeading, faListUl, faListOl, faQuoteRight } from '@fortawesome/free-solid-svg-icons';

import { vector, user, undo, redo, task, shapeSize, pencil, paintPaletteStroke,
  paintPaletteFill, network, close, move, pencilSize, eyeDropper, list, group,
  floppyDisk, eraser, chat, addButton, text, polygon, mic, micMuted, spinner,
  settings, zoomIn, zoomOut, phone, fullscreen, trashBin, checkboxEmpty,
  checkboxChecked, next, prev, student } from '@/assets/icons';

// Custom icons

import App from '@/App';
import router from '@/router';
import store from '@/store';
import config from '@/config.json';

import Icon from '@/components/Icon';

store.dispatch(
  'addIcons',
  {
    addButton,
    chat,
    checkboxChecked,
    checkboxEmpty,
    close,
    eraser,
    eyeDropper,
    floppyDisk,
    fullscreen,
    group,
    list,
    mic,
    micMuted,
    move,
    network,
    next,
    paintPaletteFill,
    paintPaletteStroke,
    pencil,
    pencilSize,
    phone,
    polygon,
    prev,
    redo,
    settings,
    shapeSize,
    spinner,
    student,
    task,
    text,
    trashBin,
    undo,
    user,
    vector,
    zoomIn,
    zoomOut,
  },
);

// todo: remove font-awesome entirely
library.add(faUserCircle, faPlusCircle, faEdit, faTrash, faPencilAlt,
  faEraser, faSquare, faSlash, faFont, faDrawPolygon, faArrowsAlt,
  faEyeDropper, faCircle, faPalette, faPaperPlane, faComments, faUndo,
  faRedo, faTimes, faCheck, faSave, faBold, faItalic, faStrikethrough,
  faUnderline, faCode, faParagraph, faHeading, faListUl, faListOl, faQuoteRight);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('custom-icon', Icon);

Vue.config.productionTip = false;

let apiUrl = `${config.hostname}${config.apiPath}`;

if (apiUrl.endsWith('/')) {
  apiUrl = apiUrl.slice(0, -1);
}

window.toastr = require('toastr');

Vue.use(VueToastr2);

Vue.use(VueAxios, axios);
Vue.use(VueAuthenticate, {
  baseUrl: `${apiUrl}`,
  storageType: null,

  providers: {
    google: {
      clientId: config.google.clientId,
      redirectUrl: `${apiUrl}/auth/google`,
    },
  },
});

// todo: set publishable key
Vue.use(VueStripeCheckout, config.stripePK);

if (store.state.token !== '') {
  Vue.axios.defaults.headers.common.Authorization = store.state.token;
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App />',
});

