<template>
  <div
    id="user-banner"
    class="row align-items-center shadow mb-4">
    <div
      class="header-bg"
      v-html="headerBg" />

    <div class="col-1" />

    <div class="col-auto d-none d-md-block">

      <img
        :src="`${pic}&size=75`"
        class="profile-pic">

    </div>

    <div class="col d-none d-md-block">
      <h3>{{ me }}</h3>
      <p class="mb-0">Role/ {{ role }}</p>
    </div>

    <div
      v-if="role === 'Teacher'"
      class="col-12 col-md-auto">

      <div class="row align-items-center">

        <div class="col-6 align-middle">

          <h3 class="mb-0 text-center">{{ ownCoursesNum }}</h3>
          <p class="text-center mb-0">Courses</p>

        </div>

        <div class="col-6 align-middle">

          <h3 class="mb-0 text-center">{{ participantsNum }}</h3>
          <p class="text-center mb-0">Students</p>

        </div>

      </div>

    </div>

    <div
      v-else
      class="col-12 col-md-auto">

      <div class="row align-items-center">

        <div class="col-6 align-middle">

          <h3 class="mb-0 text-center">{{ JoinedCoursesNum }}</h3>
          <p class="text-center mb-0">Courses</p>

        </div>

        <div class="col-6 align-middle">

          <h3 class="mb-0 text-center">{{ points }}</h3>
          <p class="text-center mb-0">Points</p>

        </div>

      </div>

    </div>

    <div class="col-1" />

  </div>
</template>

<script>
import LogoPng from '@/assets/logo.png';
import HeaderBg from '@/assets/bg_header.svg';

const rolesMap = {
  4: 'Student',
  3: 'Teacher',
  1: 'Admin',
};

export default {
  name: 'UserBanner',
  data() {
    return {
      defaultPic: LogoPng,
    };
  },
  computed: {
    pic() {
      return this.$store.state.user ? this.$store.state.user.picture : this.defaultPic;
    },
    headerBg() {
      return HeaderBg;
    },
    ownCoursesNum() {
      return this.$store.state.coursesNum || 0;
    },
    participantsNum() {
      return this.$store.state.participantsNum || 0;
    },
    points() {
      return this.$store.state.studentPoints || 0;
    },
    JoinedCoursesNum() {
      return this.$store.state.JoinedCoursesNum || 0;
    },
    me() {
      return this.$store.state.user ? `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}` : '';
    },
    role() {
      return this.$store.state.user ? rolesMap[this.$store.state.user.role_id] : 'N/A';
    },
  },
};
</script>

<style>
#user-banner {
  height: 125px;
  position: relative;
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
}

.header-bg > svg {
  height: 125px;
  max-width: 100%;
}
</style>

