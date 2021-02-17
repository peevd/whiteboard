<template>
  <div class="card bg-default shadow">

    <div class="card-img">
      <img
        :src="image"
        class="course-pic">
    </div>

    <div class="card-body">
      <div class="row mb-4">
        <div class="col">
          <h5 class="card-title">{{ course.name }}</h5>

          <div
            class="ProseMirror"
            v-html="course.description" />
        </div>
      </div>

      <div class="row justify-content-end">
        <div class="col-auto">
          <router-link
            :to="'/my-courses/' + id"
            class="btn btn-success">
            Manage
          </router-link>
          <a
            href="#"
            class="btn btn-danger mr-2"
            @click.prevent="deleteCourse">
            Delete
          </a>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import Placeholder from '@/assets/boardSnapshot.jpg';

export default {
  name: 'CourseCardOwner',
  props: {
    course: {
      type: Object,
      default() {
        return {
          id: 0,
          image: '',
          name: '',
          description: '',
          owner: '',
        };
      },
    },
  },
  computed: {
    id() {
      return this.course.id;
    },
    image() {
      return this.course.picture || Placeholder;
    },
    name() {
      return this.course.name;
    },
    description() {
      return this.course.description;
    },
    owner() {
      return this.course.owner;
    },
  },
  methods: {
    deleteCourse() {
      this.$store.dispatch('deleteCourse', this.id);
    },
  },
};
</script>

<style scoped>
.card-footer {
  background: inherit;
  border-top: 0;
}

.card-footer > a {
  margin: 0 20px;
}

.card-header h3 {
  margin-top: 10px;
}

.course-pic {
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.25);
}
</style>
