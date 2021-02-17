<template>
  <div
    id="app"
    class="container-fluid">

    <NavBar v-if="isAuthenticated" />

    <UserBanner v-if="isAuthenticated && isHome()" />

    <router-view/>

  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import UserBanner from '@/components/UserBanner';

export default {
  name: 'App',
  components: {
    NavBar,
    UserBanner,
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    isHome() {
      return this.$route.name === 'Home';
    },
  },
};
</script>

<style>
body {
  background: url('./assets/bg_plus.png');
  color: white;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  // padding: 0;
}

#app > nav {
  margin-left: -15px;
  margin-right: -15px;
}

#app > .page-content {
  margin: 0px;
  margin-left: -10px;
  margin-right: -10px;
  padding: 0px;
}

@media (min-width: 576px) {
  #app > .page-content {
    margin: 0px;
    padding: 10px;
  }
}

@media (min-width: 768px) {
  #app > .page-content {
    margin: 0px;
    padding: 10px;
  }
}

@media (min-width: 992px) {
  #app > .page-content {
    margin: 10px;
    padding: 30px;
  }
}

.click-pointer {
  cursor: pointer;
}

.full-height {
  height: 100%;
}

.modal-dialog {
  max-width: 690px;
}

.modal-footer {
  border-top: none !important;
}

.modal-header {
  border-bottom: none !important;
}

.ProseMirror-focused {
  outline: none;
}

.ProseMirror code {
  border-radius: 0.25rem;
  padding: 5px 5px 3px 5px;
  background-color: #dedede;
  color: #555;
}

.ProseMirror pre {
  overflow: auto;
  padding: 20px;
  padding: 20px 20px 20px 20px;
  background-color: #dedede;
  font-size: 100%;
}

.ProseMirror pre > code {
  padding: 0;
  background-color: inherit;
  margin: auto;
}

.ProseMirror ul li > p,
.ProseMirror ol li > p {
  margin-bottom: 0.5rem;
}

.ProseMirror > *:last-child {
  margin-bottom: 0;
}

.profile-pic {
  border-radius: 50%;
  border: 2px black solid;
}

.accordion .card:first-of-type:last-of-type {
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.spin-svg > svg {
  animation-name: ckw;
  animation-duration: 3.5s; /* Things added */
  animation-iteration-count: infinite;
  transform-origin: 50% 50%;
  display: inline-block;
  /* <--- */
}

@keyframes ckw {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn-success {
  background-color: #00cec9 !important;
  border-color: #00cec9 !important;
}

.btn-success:not(.disabled):hover {
  background-color: #02b1ad !important;
  text-decoration: none;
}

.link-success {
  color: #00ab7c !important;
}

.text-success {
  color: #00cec9 !important;
}

.btn-danger {
  background-color: #ff7675 !important;
  border-color: #ff7675 !important;
}

.btn-danger:not(.disabled):hover {
  background-color: #df6665  !important;
}

.bg-danger {
  background-color: #ff7675 !important;
}

.text-danger {
  color: #ff7675 !important;
}

.btn-default {
  background-color: transparent !important;
}

.btn-default:not(.disabled):hover,
.btn-hover:hover {
  background-color: rgba(0, 0, 0, 0.1) !important;
  background-blend-mode: multiply;
}

.bg-default {
  background-color: white !important;
}

.bg-success {
  background-color: #00cec9 !important;
  color: #fff;
}

a.bg-success:hover {
  text-decoration: none;
  background-color: #1297e0 !important;
  color: #fff;
}

.bg-white {
  background-color: #fff !important;
}

.fg-white {
  color: #fff;
}

.bg-blue {
  background-color: #00cec9 !important;
  color: #fff;
}

.vdatetime-popup__header,
.vdatetime-calendar__month__day--selected:hover>span>span,
.vdatetime-calendar__month__day--selected>span>span {
  background-color: #ff7675  !important;
}

.vdatetime-time-picker__item--selected,
.vdatetime-popup__actions__button,
.vdatetime-year-picker__item--selected,
.vdatetime-month-picker__item--selected {
  color: #ff7675  !important;
}

.btn-default.bg-default:hover:not(.disabled) {
  background-color: #eee !important;
}
</style>
