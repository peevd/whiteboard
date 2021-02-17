<template>
  <div
    :style="iconStyle"
    class="d-inline-block"
    v-html="iconSvg" />
</template>

<script>
export default {
  name: 'Icon',
  props: {
    icon: { type: String, default: '' },
    size: { type: String, default: '' },
  },
  data() {
    const defSize = 20;
    const scale = this.size[1] === 'x' ? Number(this.size[0]) : 1;

    return {
      defSize,
      realSize: scale * defSize,
    };
  },
  computed: {
    iconSvg() {
      return this.$store.state.icons[this.icon] || '';
    },
    iconStyle() {
      return {
        width: `${this.realSize}px`,
        height: `${this.realSize}px`,
      };
    },
  },
  watch: {
    size(val) {
      if (val[1] === 'x') {
        this.realSize = Number(val[0]) * this.defSize;
      }
    },
  },
};
</script>

<style scoped>
</style>
