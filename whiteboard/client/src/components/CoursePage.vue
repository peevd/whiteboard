<template>
  <div
    id="course-page"
    class="row">
    <div class="col-sm-12 col-md-6">
      <CourseCardDetailed :course="course" />
    </div>
    <div class="col-sm-12 col-md-6">
      <div class="row mb-2">
        <div class="col-sm-12">
          <div class="bg-default card shadow">
            <div class="card-body">

              <div class="row mb-3">
                <div class="col">
                  <h3 class="mb-0">Groups</h3>
                </div>
              </div>

              <vue-stripe-checkout
                ref="checkoutRef"
                :image="image"
                :name="name"
                :description="description"
                :currency="currency"
                :amount="course.price * 100"
                :allow-remember-me="false"
                :panel-label="panelLabel"
                @done="done" />

              <div
                v-for="group in groups"
                :key="group.id"
                class="card mb-2">
                <div class="card-body">
                  <div class="row align-items-center">
                    <div class="col">
                      <div class="row">
                        <div class="col">
                          <h5>{{ group.name }}</h5>
                        </div>
                      </div>
                    </div>
                    <div
                      v-if="course.price"
                      class="col-auto">
                      <button
                        class="btn btn-success"
                        @click="checkout(group.id)">Join</button>
                    </div>
                    <div class="col-auto text-center">
                      <p class="mb-0">Members</p>
                      <h3 class="mb-0 px-3">{{ group.members_in }}/{{ group.max_members }}</h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <LoadingModal :show="loading" />
  </div>
</template>

<script>
import CourseCardDetailed from '@/components/CourseCardDetailed';
import PayBtn from '@/components/PayBtn';
import LoadingModal from '@/components/LoadingModal';

export default {
  name: 'CoursePage',
  components: {
    CourseCardDetailed,
    PayBtn,
    LoadingModal,
  },
  data() {
    return {
      loading: false,
      image: 'https://i.imgur.com/HhqxVCW.jpg',
      currency: 'USD',
      description: '',
      panelLabel: 'Pay {{amount}}',
      tokenFromPromise: {},
      tokenFromEvent: {},
    };
  },
  computed: {
    cId() {
      return Number(this.$route.params.cId);
    },
    course() {
      return this.$store.state.currentCourse;
    },
    groups() {
      return this.$store.state.currentGroups;
    },
    user() {
      return this.$store.state.user;
    },
    name() {
      return `Sign up for ${this.courseName}!`;
    },
  },
  created() {
    this.$store.dispatch('fetchCourse', this.cId);
    this.$store.dispatch('fetchCourseGroups', this.cId);
  },
  methods: {
    joinGroup(cId, gId, uId) {
      this.$store.dispatch('joinGroup', { cId, gId, uId });
    },
    async checkout(gId) {
      this.tokenFromPromise = await this.$refs.checkoutRef.open();
      this.submit(this.tokenFromPromise.token, gId);
    },
    done(token) {
      this.tokenFromEvent = token;
      // this.submit(token.token);
    },
    submit(token, gId) {
      this.loading = true;
      this.$store.dispatch('submitPayment', {
        c_id: this.cId,
        g_id: gId,
        stripeToken: token.id,
        email: token.email,
      }).then(() => { this.loading = false; })
        .catch(() => { this.loading = false; });
    },
  },
};
</script>

<style>
#course-page {
  margin: 10px;
  padding: 30px;
}

#course-page > div {
  padding: 20px;
}
</style>

