<template>
  <div
    id="my-courses"
    class="row">

    <div class="col-12 mb-4 justify-content-center">
      <div class="card bg-default shadow">

        <a
          id="add-btn"
          href="#"
          class="btn-hover"
          @click.prevent="toggleModal">
          <div class="card-body p-2 row justify-content-center">
            <custom-icon
              icon="addButton"
              size="3x" />
          </div>
        </a>

      </div>
    </div>

    <div class="col-12">
      <div class="card-columns">
        <template v-for="course in courses">
          <CourseCardOwner
            :key="course.id"
            :course="course" />
        </template>
      </div>
    </div>
    <CreateCourse
      :show="showModal"
      @hide="toggleModal" />
  </div>
</template>

<script>
import CreateCourse from '@/components/CreateCourse';
import CourseCardOwner from '@/components/CourseCardOwner';

export default {
  name: 'MyCourses',
  components: {
    CreateCourse,
    CourseCardOwner,
  },
  data() {
    return {
      showModal: false,
    };
  },
  computed: {
    courses() {
      return this.$store.state.ownedCourses;
    },
  },
  created() {
    this.$store.dispatch('fetchMyCourses');
  },
  methods: {
    openCourse() {},
    toggleModal() {
      this.showModal = !this.showModal;
    },
  },
};
</script>

<style>
#my-courses {
}

#my-courses > div {
}

a:focus {
  outline: none;
}
</style>
