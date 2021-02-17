<template>
  <div
    class="row page-content justify-content-between">
    <div class="col col-md-auto mb-4">
      <div class="row justify-content-center">
        <div class="col-auto">
          <ul class="list-group shadow bg-white">
            <li class="list-group-item btn-hover">
              <router-link
                to="/admin/requests"
                class="btn">Course Approval Requests</router-link>
            </li>
            <li class="list-group-item btn-hover">
              <a
                :href="`${hostname}/miagi`"
                class="btn">DB Admin Panel</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card-columns card-columns-big">

        <div class="card bg-default shadow">
          <div class="card-body">

            <div class="row">
              <div class="col">
                <h3 class="mb-0">
                  Courses Info
                </h3>
              </div>
            </div>

            <div class="row mb-4 mt-4">
              <div class="col">
                <strong>All Courses</strong>
              </div>
              <div class="col-auto">
                {{ coursesCount }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>Open Courses</strong>
              </div>
              <div class="col-auto">
                N/A
              </div>
            </div>

          </div>
        </div>

        <div class="card bg-default shadow">
          <div class="card-body">

            <div class="row">
              <div class="col">
                <h3 class="mb-0">
                  Approval Requests
                </h3>
              </div>
            </div>

            <div class="row mb-4 mt-4">
              <div class="col">
                <strong>All Requests</strong>
              </div>
              <div class="col-auto">
                {{ requestsByStatus(0) }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>New Requests</strong>
              </div>
              <div class="col-auto">
                {{ requestsByStatus(1) }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>Need Fixing</strong>
              </div>
              <div class="col-auto">
                {{ requestsByStatus(2) }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>Approved Requests</strong>
              </div>
              <div class="col-auto">
                {{ requestsByStatus(3) }}
              </div>
            </div>

          </div>
        </div>

        <div class="card bg-default shadow">
          <div class="card-body">

            <div class="row">
              <div class="col">
                <h3 class="mb-0">
                  Users Info
                </h3>
              </div>
            </div>

            <div class="row mb-4 mt-4">
              <div class="col">
                <strong>All Users</strong>
              </div>
              <div class="col-auto">
                {{ usersByRole('all') }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>Teachers</strong>
              </div>
              <div class="col-auto">
                {{ usersByRole('teacher') }}
              </div>
            </div>

            <div class="row mt-4 mb-4">
              <div class="col">
                <strong>Students</strong>
              </div>
              <div class="col-auto">
                {{ usersByRole('student') }}
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import config from '@/config.json';

export default {
  name: 'AdminDash',
  computed: {
    hostname() {
      return config.hostname;
    },
    coursesCount() {
      return this.$store.state.coursesCount || 'N/A';
    },
    requestsCount() {
      return this.$store.state.requestsCount;
    },
    usersCount() {
      return this.$store.state.usersCount;
    },
  },
  created() {
    this.$store.dispatch('fetchCoursesCount');
    this.$store.dispatch('fetchApprovalRequstsCount');
    this.$store.dispatch('fetchUsersCount');
  },
  methods: {
    requestsByStatus(status) {
      return this.requestsCount[status] !== undefined ? this.requestsCount[status] : 'N/A';
    },
    usersByRole(role) {
      return this.usersCount[role] !== undefined ? this.usersCount[role] : 'N/A';
    },
  },
};
</script>
