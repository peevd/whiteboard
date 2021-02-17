<template>
  <div class="row mt-4 justify-content-center">
    <div class="col-sm-12 col-md-6 text-center">

      <p>
        <strong>Are you a</strong>
      </p>

      <a
        href="#"
        @click="setRole(4)">
        <div class="jumbotron mb-3">
          <strong>Student</strong>
        </div>
      </a>

      <p>
        <strong>- or a -</strong>
      </p>

      <a
        href="#"
        @click="setRole(3)">
        <div class="jumbotron mb-4">
          <strong>Teacher</strong>
        </div>
      </a>

    </div>
  </div>
</template>

<script>
export default {
  name: 'RoleSelect',
  methods: {
    setRole(role) {
      this.$store.dispatch('setUserRole', role);
    },
  },
};
</script>

<style scoped>
.jumbotron {
  font-size: 2rem;
}

a {
  text-decoration: none !important;
  color: #00b894;
}

a:hover {
  color: #009074;
}

p {
  font-size: 1.5rem;
}
</style>
