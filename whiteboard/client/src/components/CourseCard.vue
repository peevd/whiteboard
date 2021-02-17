<template>
  <div
    class="card shadow border bg-default">

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

      <div
        v-if="showLink"
        class="row justify-content-end">
        <div class="col-auto">
          <router-link
            :to="href"
            class="btn btn-success">
            Go to course
          </router-link>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import Placeholder from '@/assets/boardSnapshot.jpg';

export default {
  name: 'CourseCard',
  props: {
    course: {
      type: Object,
      default() {
        return {
          id: null,
          name: '',
          description: '',
          owner_id: null,
          date: '',
          owner: '',
        };
      },
    },
    href: { type: String, default: '#' },
    showLink: { type: Boolean, default: true },
  },
  computed: {
    image() {
      return this.course.picture || Placeholder;
    },
    title() {
      return this.course.title;
    },
    description() {
      return this.course.description;
    },
    author() {
      return this.course.author;
    },
  },
};
</script>

<style scoped>
.card-header h3 {
  margin-top: 10px;
}

.course-pic {
  width: 100%;
  border-radius: 0.25rem;
  border: 1px solid rgba(0, 0, 0, 0.25)
}
</style>
