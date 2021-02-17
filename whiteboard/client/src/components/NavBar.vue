<template>
  <nav class="navbar navbar-expand-md navbar-light bg-light shadow p-0">
    <div class="row text-truncate">
      <div class="col">
        <nav>
          <ol class="ml-2 mt-0 mb-0 p-0 bg-default breadcrumb">
            <li
              :class="[ atHome ? 'active' : '' ]"
              class="breadcrumb-item p-0">
              <router-link
                to="/"
                class="btn btn-default btn-hover">Home</router-link>
            </li>
            <li
              v-for="(b, i) in breadcrumbs"
              :key="i"
              class="breadcrumb-item p-0">
              <router-link
                :to="b.href"
                class="btn btn-default btn-hover">{{ b.name }}</router-link>
            </li>
          </ol>
        </nav>
      </div>
    </div>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation">
      <span class="navbar-toggler-icon" />
    </button>

    <div
      id="navbarSupportedContent"
      class="collapse navbar-collapse">
      <ul class="navbar-nav mr-auto" />
      <div class="my-2 my-lg-0 ml-2">
        <div class="dropdown">
          <button
            id="settings-btn"
            class="btn btn-default dropdown-toggle"
            type="button"
            data-toggle="dropdown" >
            <custom-icon
              icon="settings"
              size="1x" />
          </button>
          <div class="dropdown-menu dropdown-menu-right">
            <a
              class="dropdown-item"
              href="#"
              @click.prevent="() => {}">
              Profile
            </a>
            <a
              class="dropdown-item"
              href="#"
              @click.prevent="() => {}">
              Help
            </a>
            <a
              class="dropdown-item"
              href="#"
              @click.prevent="logout">
              Logout
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import NavLink from '@/components/NavLink';
import LogoPng from '@/assets/logo.png';

export default {
  name: 'NavBar',
  components: {
    NavLink,
  },
  data() {
    return {
      logo: LogoPng,
    };
  },
  computed: {
    atHome() {
      return this.$route.path === '/';
    },
    user() {
      return this.$store.state.user;
    },
    course() {
      return this.$store.state.breadcrumbs.course;
    },
    group() {
      return this.$store.state.breadcrumbs.group;
    },
    courseName() {
      let out = '';
      const cId = this.$route.params.cId ? Number(this.$route.params.cId) : null;

      if (cId && this.$store.state.currentCourse.id === cId) {
        out = `${this.$store.state.currentCourse.name}`;
      }

      const gId = this.$route.params.gId ? Number(this.$route.params.gId) : null;

      if (gId && this.$store.state.currentGroup.id === gId) {
        out = `${out} / ${this.$store.state.currentGroup.name}`;
      }

      return out;
    },
    breadcrumbs() {
      return this.$store.state.breadcrumbs;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('authLogout');
    },
  },
};
</script>

<style scope>
nav,
nav * {
  z-index: 1001;
}
nav.navbar {
  height: 40px;
  background-color: #fff !important;
  color: #010101 !important;
}

.navbar-light .navbar-nav .nav-item .nav-link {
  color: #010101;
  font-weight: 400;
}

.navbar-light .navbar-nav .nav-item.active .nav-link{
  color: #010101 !important;
  font-weight: 600;
}

#profile-btn{
  color: #010101;
}

#profile-btn:hover {
  color: #282828;
}

#settings-btn {
  color: #010101 !important;
  border-radius: 0;
}

.breadcrumb-item > a {
  font-size: 16px;
  color: #212529;
  border-radius: 0;
}

.breadcrumb-item::before {
  padding: 0 4px !important;
}

</style>
