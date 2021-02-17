<template>
  <div
    id="home"
    class="row page-content">

    <div class="col-sm-12">

      <div class="row mb-4">
        <div class="col-sm-12">
          <div class="btn-group bg-white shadow w-100">

            <template v-if="isTeacher">
              <button
                :class="activePage === 0 ? 'btn-success' : 'btn-default'"
                class="btn border w-50"
                @click.prevent="setPage(0)">
                <strong>Appointments</strong>
              </button>
              <button
                :class="activePage === 1 ? 'btn-success' : 'btn-default'"
                class="btn border w-50"
                @click.prevent="setPage(1)">
                <strong>My Courses</strong>
              </button>
            </template>

            <template v-else>
              <button
                :class="activePage === 0 ? 'btn-success' : 'btn-default'"
                class="btn border w-50"
                @click.prevent="setPage(0)">
                <strong>Appointments</strong>
              </button>
              <button
                :class="activePage === 1 ? 'btn-success' : 'btn-default'"
                class="btn border w-50"
                @click.prevent="setPage(1)">
                <strong>My Courses</strong>
              </button>
              <button
                :class="activePage === 2 ? 'btn-success' : 'btn-default'"
                class="btn border w-50"
                @click.prevent="setPage(2)">
                <strong>All Courses</strong>
              </button>
            </template>

          </div>
        </div>
      </div>

      <template v-if="isTeacher">

        <template v-if="activePage === 0">
          <AppointmentsListDetailed />
        </template>

        <template v-else-if="activePage === 1">
          <MyCourses />
        </template>

        <template v-else>
          <div>nothing here</div>
        </template>

      </template>

      <template v-else>

        <template v-if="activePage === 0">
          <AppointmentsListDetailed :disable-edit="true" />
        </template>

        <template v-else-if="activePage === 1">
          <JoinedCourses />
        </template>

        <template v-else-if="activePage === 2">
          <AllCourses />
        </template>

        <template v-else>
          <div>nothing here</div>
        </template>

      </template>
    </div>

  </div>
</template>

<script>
import AppointmentsListDetailed from '@/components/AppointmentsListDetailed';
import CourseCard from '@/components/CourseCard';
import JoinedCourses from '@/components/JoinedCourses';
import MyCourses from '@/components/MyCourses';
import AllCourses from '@/components/AllCourses';

export default {
  name: 'Home',
  components: {
    AppointmentsListDetailed,
    CourseCard,
    JoinedCourses,
    MyCourses,
    AllCourses,
  },
  data() {
    let activePage = 0;
    if (this.$route.query.p) {
      activePage = Number(this.$route.query.p);
      activePage = activePage === 0 || activePage === 1 ? activePage : 0;
    }

    return {
      activePage,
    };
  },
  computed: {
    name() {
      return this.$store.state.user.name;
    },
    joinedCourses() {
      return this.$store.state.joinedCourses;
    },
    isTeacher() {
      return this.$store.getters.isTeacher;
    },
    isModAdmin() {
      return this.$store.getters.isMod || this.$store.getters.isAdmin;
    },
  },
  created() {
    if (this.isModAdmin) {
      this.$router.push('/admin');
    }
  },
  methods: {
    setPage(id) {
      this.activePage = id;
      const query = Object.assign({}, this.$route.query, { p: id });
      this.$router.push({ query });
    },
  },
};
</script>

<style>
.btn:focus {
  box-shadow: none;
}

.btn-default {
  background-color: #fff !important;
}

.btn-default:hover {
  background-color: #f8f8f8 !important;
}
</style>

