<template>
  <div class="row">
    <AppointmentsEditModal
      v-if="!disableEdit"
      :show="showAppointmentEditModal"
      :event="eventToEdit"
      @hide="toggleAppointmentEditModal" />
    <template v-if="!events || events.length === 0">
      <div class="col-12 col-md-6 offset-md-3">
        <div class="jumbotron">
          <h3 class="text-center">
            No appointments
          </h3>
        </div>
      </div>
    </template>
    <template v-else>
      <div
        v-for="e in events"
        :key="e.id"
        class="col-12">
        <div class="card shadow mb-4">
          <div
            class="card-header bg-default btn-hover p-0"
            @click="toggleAppointment(e.id)">
            <div class="row equal mx-0">

              <router-link
                :to="isTeacher ? `/my-courses/${e.course_id}/groups/${e.group_id}` :
                `/joined-courses/${e.course_id}`"
                class="col-auto p-4 btn-success">
                <div class="row h-100 align-items-center">
                  <div class="col">
                    <div class="row">
                      <div class="col">
                        {{ e.course_name }}
                      </div>
                    </div>
                    <div class="row">
                      <div class="col">
                        {{ e.group_name }}
                      </div>
                    </div>
                  </div>
                </div>
              </router-link>

              <div class="col p-4">
                <div class="row">
                  <div class="col">
                    <h3>{{ e.subject }}</h3>
                  </div>
                </div>
              </div>

              <div
                v-if="!disableEdit"
                class="col-auto show-hover">
                <div class="row h-100 align-items-center">
                  <div class="col">
                    <button
                      id="edit-course"
                      class="btn btn-sm btn-default border"
                      title="Edit"
                      @click.stop="toggleAppointmentEditModal(e.id)">
                      <font-awesome-icon
                        icon="edit"
                        size="1x" />
                    </button>
                  </div>
                </div>
              </div>

              <div class="col-auto p-4 bg-danger">
                <div class="row h-100 align-items-center">
                  <div class="col">
                    <div class="row">
                      <div class="col">
                        {{ parseTime(e.date) }}
                      </div>
                    </div>
                    <div class="row">
                      <div class="col">
                        {{ parseDate(e.date) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
          <div
            v-show="isOpen(e.id)"
            class="card-body">
            <div class="row">
              <div class="col-6">
                <h5>Description:</h5>
                {{ e.body }}
              </div>
              <div class="col-6">
                <h5>Tasks:</h5>
                <p
                  v-for="t in e.tasks_data"
                  :key="t.id"
                  class="mb-0">
                  {{ t.name }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import moment from 'moment';
import AppointmentsEditModal from '@/components/AppointmentsEditModal';

export default {
  name: 'AppointmentsListDetailed',
  components: {
    AppointmentsEditModal,
  },
  props: {
    disableEdit: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showAppointmentEditModal: false,
      eventToEdit: {},
      openAppointments: [],
    };
  },
  computed: {
    events() {
      return this.$store.state.events;
    },
    isTeacher() {
      return this.$store.getters.isTeacher;
    },
    isStudent() {
      return this.$store.getters.isStudent;
    },
  },
  created() {
    this.$store.dispatch('fetchEvents');
  },
  methods: {
    parseDate(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('DD/MM/YYYY');
    },
    parseTime(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('H:mm');
    },
    toggleAppointmentEditModal(id) {
      if (id) {
        const event = this.events.find(el => el.id === id);
        if (event) {
          this.eventToEdit = event;
        } else {
          this.eventToEdit = {};
        }
      } else {
        this.eventToEdit = {};
      }

      this.showAppointmentEditModal = !this.showAppointmentEditModal;
      return false;
    },
    isOpen(id) {
      return this.openAppointments.findIndex(el => el === id) !== -1;
    },
    toggleAppointment(id) {
      if (this.openAppointments.findIndex(el => el === id) !== -1) {
        this.openAppointments = this.openAppointments.filter(el => el !== id);
      } else {
        this.openAppointments = this.openAppointments.concat([id]);
      }
    },
  },
};
</script>

<style scoped>
.card .show-hover {
  display: none;
}

.card:hover .show-hover {
  display: initial;
}

.rounded-top-left {
  border-top-left-radius: 0.25rem !important;
}

.rounded-top-right {
  border-top-right-radius: 0.25rem !important;
}

.bg-orange {
  background-color: orange;
}
</style>
