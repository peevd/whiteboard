<template>
  <div
    id="modal"
    class="modal fade"
    tabindex="-1"
    role="dialog">
    <div
      class="modal-dialog"
      role="document">
      <div class="modal-content bg-default">
        <div class="modal-header bg-default">
          <h3 class="modal-title">Create New Appointment</h3>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form
            id="new-course-form"
            ref="eventForm"
            :class="[ formValidated ? 'was-validated' : '' ]"
            class="text-left"
            @submit="createAppointment">
            <div
              class="form-group row">
              <label
                for="appointment-subject"
                class="col-sm-3 col-form-label">Subject</label>
              <div class="col-sm-9">
                <input
                  id="appointment-subject"
                  v-model="subject"
                  type="text"
                  required
                  class="form-control">
                <div class="invalid-feedback">
                  Subject can not be empty
                </div>
              </div>
            </div>
            <div class="form-group row">
              <label
                for="appointment-description"
                class="col-sm-3 col-form-label">Description</label>
              <div class="col-sm-9">
                <textarea
                  id="appointment-description"
                  v-model="description"
                  required
                  class="form-control" />
                <div class="invalid-feedback">
                  Description can not be empty
                </div>
              </div>
            </div>
            <div class="form-group row">
              <label
                for="appointment-description"
                class="col-sm-3 col-form-label">Date</label>
              <div class="col-sm-9">
                <Datetime
                  v-model="date"
                  type="datetime"
                  input-id="datetime-input"
                  input-class="form-control"
                  class="td"
                  format="DD T">
                  <template slot="after">
                    <div class="invalid-feedback">
                      Please enter correct date
                    </div>
                  </template>
                </Datetime>
              </div>
            </div>
            <div class="form-group row">
              <label
                for="appointment-tasks"
                class="col-sm-3 col-form-label">Tasks</label>
              <div class="col-sm-9">
                <select
                  v-model="taskIds"
                  class="custom-select"
                  multiple>
                  <option
                    v-for="t in tasks"
                    :key="t.id"
                    :value="t.id">
                    {{ t.name }}
                  </option>
                </select>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer bg-default">
          <button
            type="button"
            class="btn btn-secondary"
            data-dismiss="modal">Close</button>
          <button
            type="button"
            class="btn btn-success"
            @click="createAppointment">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import moment from 'moment';
import 'vue-datetime/dist/vue-datetime.min.css';
import { Datetime } from 'vue-datetime';

export default {
  name: 'AppointmentsCreateModal',
  components: {
    Datetime,
  },
  props: {
    show: { type: Boolean, default: false },
    cId: { type: Number, default: null },
    gId: { type: Number, default: null },
  },
  data() {
    return {
      subject: '',
      description: '',
      date: '',
      formValidated: false,
      taskIds: [],
    };
  },
  computed: {
    tasks() {
      return this.$store.state.currentTasks;
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');
      } else {
        $(this.$el).modal('hide');
      }

      const component = this;
      if (newVal === true) {
        $(this.$el).one('hide.bs.modal', () => {
          component.$emit('hide');
        });
      }
    },
  },
  mounted() {
    const dtInput = this.$el.querySelector('#datetime-input');
    dtInput.required = true;

    this.$store.dispatch('fetchTasks', this.cId);
  },
  methods: {
    createAppointment() {
      if (!this.$refs.eventForm.checkValidity()) {
        this.formValidated = true;
        return;
      }

      const data = {
        c_id: this.cId,
        g_id: this.gId,
        subject: this.subject,
        body: this.description,
        date: moment(this.date).format('YYYY-MM-DD H:mm'),
        task_ids: this.taskIds,
      };

      this.$store.dispatch('createEvent', data);

      this.subject = '';
      this.description = '';
      this.date = '';
      this.formValidated = false;

      $(this.$el).modal('hide');
    },
  },
};
</script>

<style>
.td .vdatetime-popup {
  top: initial;
}
</style>
