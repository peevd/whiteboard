<template>
  <img
    :src="btnSrc"
    @mouseenter="mouseEnter"
    @mousedown="mouseDown"
    @mouseup="mouseUp"
    @mouseleave="mouseUp">
</template>

<script>
import GoogleBtnNormal from '@/assets/googleBtn/btn_google_signin_light_normal_web.png';
import GoogleBtnFocus from '@/assets/googleBtn/btn_google_signin_light_focus_web.png';
import GoogleBtnPressed from '@/assets/googleBtn/btn_google_signin_light_pressed_web.png';

export default {
  name: 'GoogleSignInBtn',
  data() {
    return {
      btnSrc: GoogleBtnNormal,
    };
  },
  methods: {
    mouseEnter() {
      this.btnSrc = GoogleBtnFocus;
    },
    mouseDown() {
      this.btnSrc = GoogleBtnPressed;
    },
    mouseUp() {
      this.btnSrc = GoogleBtnNormal;
    },
    mouseLeave() {
      this.btnSrc = GoogleBtnNormal;
    },
  },
};
</script>

