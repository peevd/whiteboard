<template>
  <img
    :src="btnSrc"
    @mouseenter="mouseEnter"
    @mousedown="mouseDown"
    @mouseup="mouseUp"
    @mouseleave="mouseUp">
</template>

<script>
import FacebookBtnNormal from '@/assets/facebookBtn/btn_facebook_normal.png';
import FacebookBtnFocus from '@/assets/facebookBtn/btn_facebook_focus.png';
import FacebookBtnPressed from '@/assets/facebookBtn/btn_facebook_pressed.png';

export default {
  name: 'FacebookSignInBtn',
  data() {
    return {
      btnSrc: FacebookBtnNormal,
    };
  },
  methods: {
    mouseEnter() {
      this.btnSrc = FacebookBtnFocus;
    },
    mouseDown() {
      this.btnSrc = FacebookBtnPressed;
    },
    mouseUp() {
      this.btnSrc = FacebookBtnNormal;
    },
    mouseLeave() {
      this.btnSrc = FacebookBtnNormal;
    },
  },
};
</script>
