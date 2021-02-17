<template>
  <div class="card-columns">
    <template
      v-for="course in courses">
      <CourseCard
        :key="course.id"
        :course="course"
        :href="'/courses/' + course.id"
        class="mb-4" />
    </template>
  </div>
</template>

<script>
import CourseCard from '@/components/CourseCard';

export default {
  name: 'AllCourses',
  components: {
    CourseCard,
  },
  computed: {
    joinedCourses() {
      return this.$store.state.joinedCourses;
    },
    courses() {
      return this.$store.state.courses.filter(el => !this.joinedCourses.find(e => e.id === el.id));
    },
  },
  created() {
    this.$store.dispatch('fetchCourses');
    this.$store.dispatch('fetchJoinedCourses');
  },
};
</script>
