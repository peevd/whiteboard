<template>
  <div class="card bg-default shadow">
    <img
      :src="image"
      class="card-img-top">
    <div class="card-body">
      <div class="row">
        <div class="col">
          <h1>{{ course.name }}</h1>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col">
          <div
            class="ProseMirror"
            v-html="course.description" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <h5>Price: {{ course.price ? `${course.price}$` : '0' }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Placeholder from '@/assets/boardSnapshot.jpg';

export default {
  name: 'CourseCardDetailed',
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
  },
  computed: {
    image() {
      return this.course.picture || Placeholder;
    },
  },
};
</script>

<style scoped>
</style>
