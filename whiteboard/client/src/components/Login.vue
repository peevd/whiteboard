<template>
  <div
    id="login"
    class="row full-height">
    <div class="col-12 col-md-8 col-lg-9 order-2 order-md-1 h-100 scroll courses-preview">
      <div class="card-columns card-columns-medium">
        <CourseCard
          v-for="c in courses"
          :key="c.id"
          :course="c"
          :show-link="false" />
      </div>
    </div>
    <div
      class="col-12 col-md-4 col-lg-3 login-section order-1 order-md-2">
      <div
        class="login-bg"
        v-html="loginBg" />

      <div class="row h-100">
        <div class="col bg-transparent border shadow m-0 p-4 align-self-center text-center">

          <h2>Choose sign in method</h2>
          <hr>
          <a
            id="googleSignInBtn"
            @click="authenticate('google')">

            <GoogleSignInBtn />

          </a>

          <a
            id="facebookSignInBtn"
            @click="authenticate('facebook')">

            <FacebookSignInBtn />

          </a>

        </div>
      </div>

    </div>
  </div>
</template>

<script>
import LoginBg from '@/assets/bg_login.svg';

// import Vue from 'vue';
import GoogleSignInBtn from '@/components/GoogleSignInBtn';
import FacebookSignInBtn from '@/components/FacebookSignInBtn';
import CourseCard from '@/components/CourseCard';

export default {
  name: 'Login',
  components: {
    GoogleSignInBtn,
    FacebookSignInBtn,
    CourseCard,
  },
  computed: {
    redirectUrl() {
      const redirect = this.$route.query.redirect;
      return this.$route.query.redirect ? decodeURIComponent(redirect) : '/';
    },
    courses() {
      return this.$store.state.indexCourses;
    },
    loginBg() {
      return LoginBg;
    },
  },
  created() {
    this.$store.dispatch('fetchIndexCourses');
  },
  methods: {
    authenticate(provider) {
      this.$auth.authenticate(provider).then((authResponse) => {
        this.$store.dispatch('authLogin', {
          token: authResponse.data.token,
          redirectUrl: this.redirectUrl,
        });
      }).catch((e) => {
        console.log('auth error', e);
      });
    },
  },
};
</script>

<style>
#login {
}

.full-height {
  height: 100vh;
}

.bg-transparent {
  background-color: rgba(245, 245, 245, 0.95) !important;
}

.login-section {
  background-color: #eee;

  border-bottom: 1px solid gray;
  border-left: 0;

  padding: 20px;

  overflow: hidden;
}

.scroll {
  overflow-y: auto;
}

.courses-preview {
  padding: 10px !important;
}

@media (min-width: 768px) {
  .courses-preview {
    padding: 50px !important;
  }

  .login-section {
    border-left: 1px solid gray;
    border-bottom: 0;
  }
}

.login-bg {
  display: inline;
  position: absolute;
  top: 0;
  left: 0;
  min-width: 100%;
  min-height: 100%;
}

.bg-gray {
  background-color: #e0e0e0;
}
</style>

