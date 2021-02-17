<template>
  <div class="card bg-default shadow">
    <AppointmentsCreateModal
      :show="showAppointmentCreateModal"
      :c-id="cId"
      :g-id="gId"
      @hide="toggleAppointmentCreateModal" />
    <AppointmentsEditModal
      v-if="!disableEdit"
      :show="showAppointmentEditModal"
      :event="eventToEdit"
      @hide="toggleAppointmentEditModal" />
    <div class="card-body">
      <div class="row mb-3 align-items-center">
        <div class="col-auto pr-1">
          <custom-icon
            icon="task"
            size="3x" />
        </div>
        <div class="col">
          <h3 class="mb-0 pt-1">Appointments</h3>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div
            v-if="cId && gId"
            class="card mt-2 mb-2">
            <a
              id="add-btn"
              href="#"
              class="btn-hover"
              @click.prevent="toggleAppointmentCreateModal">
              <div class="card-body p-2 row justify-content-center">
                <custom-icon
                  icon="addButton"
                  size="2x" />
              </div>
            </a>
          </div>
          <template v-if="!events || events.length === 0">
            <div>
              <h5 class="text-center"> No appointments available </h5>
            </div>
          </template>
          <template v-else>
            <div
              v-for="e in events"
              :key="e.id"
              class="card mt-2 mb-2 event-card">
              <div class="card-header bg-white p-0">
                <div
                  class="row mx-0 equal btn-hover"
                  @click="toggleBody(e.id)">
                  <div
                    class="col-auto bg-success rounded-top-left p-2">
                    <div class="row">
                      <div class="col text-center">
                        {{ parseTime(e.date) }}
                      </div>
                    </div>
                    <div class="row">
                      <div class="col text-center">
                        {{ parseDate(e.date) }}
                      </div>
                    </div>
                  </div>
                  <div class="col">
                    <div class="row h-100 align-items-center">
                      <div class="col">
                        {{ e.course_name || getCourseName(e.course_id) }}
                        / {{ e.group_name || getGroupName(e.group_id) }}
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
                  <div class="col-auto bg-danger w-10 p-0 rounded-top-right" />
                </div>
              </div>
              <div
                v-show="showBody(e.id)"
                class="card-body">
                <div class="row">
                  <div class="col">
                    <h5>{{ e.subject }}</h5>
                  </div>
                </div>
                <div class="row mb-4">
                  <div class="col">
                    {{ e.body }}
                  </div>
                </div>
                <div class="row">
                  <div class="col">
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
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import AppointmentsCreateModal from '@/components/AppointmentsCreateModal';
import AppointmentsEditModal from '@/components/AppointmentsEditModal';

export default {
  name: 'AppointmentsCard',
  components: {
    AppointmentsCreateModal,
    AppointmentsEditModal,
  },
  props: {
    events: {
      type: Array,
      default() { return []; },
    },
    cId: {
      type: Number,
      default: null,
    },
    gId: {
      type: Number,
      default: null,
    },
    disableEdit: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      openAppointments: [],
      showAppointmentCreateModal: false,
      showAppointmentEditModal: false,
      eventToEdit: {},
    };
  },
  computed: {
    groups() {
      return this.$store.state.currentGroups;
    },
  },
  methods: {
    toggleBody(id) {
      if (this.openAppointments.indexOf(id) === -1) {
        this.openAppointments.unshift(id);
      } else {
        this.openAppointments = this.openAppointments.filter(el => el !== id);
      }
    },
    showBody(id) {
      return this.openAppointments.indexOf(id) !== -1;
    },
    parseDate(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('DD/MM/YYYY');
    },
    parseTime(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('H:mm');
    },
    getGroupName(gId) {
      if (this.$store.state.currentGroup && this.$store.state.currentGroup.id === gId) {
        return this.$store.state.currentGroup.name;
      }

      const group = this.groups.find(el => el.id === gId);
      return group ? group.name : 'N/A';
    },
    getCourseName(cId) {
      if (this.$store.state.currentCourse && this.$store.state.currentCourse.id === cId) {
        return this.$store.state.currentCourse.name;
      }

      const course = this.$store.state.ownedCourses.find(el => el.id === cId);
      return course ? course.name : 'N/A';
    },
    toggleAppointmentCreateModal() {
      this.showAppointmentCreateModal = !this.showAppointmentCreateModal;
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
  },
};
</script>

<style>
.rounded-top-left {
  border-top-left-radius: 0.25rem !important;
}

.rounded-top-right {
  border-top-right-radius: 0.25rem !important;
}

.w-10 {
  width: 10px !important;
}

.event-card .show-hover {
  display: none;
}

.event-card:hover .show-hover {
  display: initial;
}
</style>
