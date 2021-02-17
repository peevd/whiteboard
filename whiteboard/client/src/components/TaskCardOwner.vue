<template>
  <div class="card bg-default shadow">
    <div class="card-body row">
      <div class="col-sm-12 text-center">
        <h3>{{ task.name }}</h3>
      </div>
    </div>
    <div class="card-footer text-center pt-0">
      <button
        class="btn btn-success"
        @click="editTask">Edit</button>
      <button
        class="btn btn-danger"
        @click="deleteTask">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    courseId: { type: Number, default: 0 },
    task: {
      type: Object,
      default() {
        return {
          id: 0,
          name: '',
          description: '',
        };
      },
    },
  },
  methods: {
    deleteTask() {
      this.$store.dispatch(
        'deleteTask',
        {
          courseId: this.courseId,
          taskId: this.task.id,
        },
      );
    },
    editTask() {
      this.$store.commit('setCurrentTask', this.task);
      this.$store.commit('toggleTaskEdit');
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
