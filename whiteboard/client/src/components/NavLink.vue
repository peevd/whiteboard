<template>
  <li :class="classes">
    <a
      :href="path"
      class="nav-link">{{ name }}</a>
  </li>
</template>

<script>
export default {
  name: 'NavLink',
  props: {
    name: { type: String, default: '' },
    path: { type: String, default: '' },
  },
  data() {
    return {
      active: this.$router.history.current.fullPath === this.path.substring(1),
    };
  },
  computed: {
    classes() {
      return {
        'nav-item': true,
        active: this.active,
      };
    },
  },
  watch: {
    $route() {
      this.active = this.$router.history.current.fullPath === this.path.substring(1);
    },
  },
};
</script>

<style scope>
a:focus {
  outline: 0;
}
</style>
