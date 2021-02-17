<template>
  <div
    class="row page-content justify-content-between">
    <div class="col-md-12">
      <div class="row">
        <ApprovalRequestCard
          :enable-edit="true"
          :request="request" />
      </div>
      <div class="row">
        <div class="col-sm-12 col-md-6">

          <div class="row mb-4">
            <div class="col">
              <CourseCardDetailed :course="course" />
            </div>
          </div>

          <div class="row mb-4">
            <div class="col">
              <AppointmentsCard
                :disable-edit="true"
                :events="events" />
            </div>
          </div>

        </div>

        <div class="col-sm-12 col-md-6">

          <div class="row mb-4">
            <div class="col">
              <TasksCardMod :tasks="tasks" />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <div class="card bg-default shadow">
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <h3 class="mb-0">Groups</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <div
                        v-for="g in groups"
                        :key="g.id"
                        class="card bg-default mt-4">
                        <div class="card-body">
                          <div class="row">
                            <div class="col">
                              <h3 class="mb-0">{{ g.name }}</h3>
                            </div>
                            <div class="col-auto align-self-center">
                              <h5 class="mb-0">{{ g.max_members }}</h5>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApprovalRequestCard from '@/components/ApprovalRequestCard';
import AppointmentsCard from '@/components/AppointmentsCard';
import CourseCardDetailed from '@/components/CourseCardDetailed';
import TasksCardMod from '@/components/TasksCardMod';

export default {
  name: 'ApprovalRequest',
  components: {
    ApprovalRequestCard,
    AppointmentsCard,
    CourseCardDetailed,
    TasksCardMod,
  },
  computed: {
    id() {
      return Number(this.$route.params.id);
    },
    request() {
      return this.$store.state.approvalRequest;
    },
    course() {
      return this.$store.state.currentCourse;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    events() {
      return this.$store.state.events;
    },
    groups() {
      return this.$store.state.currentGroups;
    },
  },
  created() {
    this.$store.dispatch('setBreadcrumbs', [
      {
        name: 'Requests',
        href: '/admin/requests',
      },
    ]);

    this.$store.dispatch('fetchApprovalRequest', this.id)
      .then(() => { this.$store.dispatch('fetchCourseMod', this.request.course_id); })
      .catch(() => this.$toastr.error('Failed to fetch request'));
  },
};
</script>
