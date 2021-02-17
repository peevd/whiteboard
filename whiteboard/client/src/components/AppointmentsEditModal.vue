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
          <h3 class="modal-title">Edit Appointment</h3>
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
            @submit="updateAppointment">
            <fieldset disabled>
              <div
                class="form-group row">
                <label
                  for="appointment-subject"
                  class="col-sm-3 col-form-label">Course</label>
                <div class="col-sm-9">
                  <input
                    id="appointment-subject"
                    v-model="event.course_name"
                    type="text"
                    required
                    class="form-control">
                </div>
              </div>
              <div
                class="form-group row">
                <label
                  for="appointment-subject"
                  class="col-sm-3 col-form-label">Group</label>
                <div class="col-sm-9">
                  <input
                    id="appointment-subject"
                    v-model="event.group_name"
                    type="text"
                    required
                    class="form-control">
                </div>
              </div>
            </fieldset>
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
                  format="DD T">
                  <template slot="after">
                    <div class="invalid-feedback">
                      Please enter correct date
                    </div>
                  </template>
                </Datetime>
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
            @click="updateAppointment">Save</button>
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
  name: 'AppointmentsEditModal',
  components: {
    Datetime,
  },
  props: {
    show: { type: Boolean, default: false },
    event: { type: Object, default: () => {} },
  },
  data() {
    return {
      subject: '',
      description: '',
      date: '',
      formValidated: false,
    };
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
    event(newVal) {
      this.subject = newVal.subject;
      this.description = newVal.body;
      this.date = moment(newVal.date, 'YYYY-MM-DD H:mm:ss').toISOString();
      this.formValidated = false;
    },
  },
  mounted() {
    const dtInput = this.$el.querySelector('#datetime-input');
    dtInput.required = true;
  },
  methods: {
    updateAppointment() {
      if (!this.$refs.eventForm.checkValidity()) {
        this.formValidated = true;
        return;
      }

      if (this.subject !== event.subject || this.description !== event.body
          || this.date !== event.date) {
        const data = Object.assign({}, this.event, {
          subject: this.subject,
          body: this.description,
          date: moment(this.date).format('YYYY-MM-DD H:mm'),
        });

        this.$store.dispatch('updateEvent', data);
      }

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
.vdatetime-popup {
  top: initial;
}
</style>
