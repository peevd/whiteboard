<template>
  <div class="card bg-default shadow">
    <div class="card-body text-center">
      <router-link :to="'/my-courses/' + courseId + '/groups/' + group.id">
        <h3>{{ group.name }}</h3>
      </router-link>
    </div>
    <div class="card-footer text-center pt-0">
      <button
        class="btn btn-success"
        @click="editGroup">Edit</button>
      <button
        class="btn btn-danger"
        @click="deleteGroup">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GroupCard',
  props: {
    courseId: { type: Number, default: 0 },
    group: {
      type: Object,
      default() {
        return {
          id: 0,
          name: '',
        };
      },
    },
  },
  methods: {
    editGroup() {
      this.$store.commit('setCurrentGroup', this.group);
      this.$store.commit('toggleGroupEdit');
    },
    deleteGroup() {
      this.$store.dispatch(
        'deleteGroup',
        {
          courseId: this.courseId,
          groupId: this.group.id,
        },
      );
    },
  },
};
</script>

<style scoped>
.card {
  height: 100%;
}

.card-footer {
  background: inherit;
  border-top: 0;
}
</style>
