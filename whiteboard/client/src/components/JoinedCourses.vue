<template>
  <div
    id="joined-courses"
    class="row">

    <div
      v-if="!courses || courses.length == 0"
      class="jumbotron mx-auto text-center">
      <h3>Sorry, you haven't joined any courses yet :(</h3>
    </div>

    <div class="col-12">
      <div class="card-columns">
        <template v-for="course in courses">
          <CourseCard
            :key="course.id"
            :course="course"
            :href="'/joined-courses/' + course.id"
            class="mb-4" />
        </template>
      </div>
    </div>

  </div>
</template>

<script>
import CourseCard from '@/components/CourseCard';

export default {
  name: 'JoinedCourses',
  components: {
    CourseCard,
  },
  computed: {
    name() {
      return this.$store.state.user.name;
    },
    courses() {
      return this.$store.state.joinedCourses;
    },
  },
  created() {
    this.$store.dispatch('fetchJoinedCourses');
  },
};
</script>

<style scoped>
#joined-courses {
}
</style>
