<template>
  <div
    id="modal"
    class="modal fade"
    tabindex="-1"
    role="dialog">
    <div
      class="modal-dialog"
      role="document">
      <div class="modal-content bg-default rounded">
        <div class="modal-header bg-default">
          <h5 class="modal-title">Invite students</h5>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <select
            v-model="studentsList"
            class="custom-select"
            multiple>
            <option
              v-for="student in students"
              :key="student.id"
              :value="student.id">
              {{ student.first_name }} {{ student.last_name }}
            </option>
          </select>
        </div>
        <div class="modal-footer bg-default">
          <button
            type="button"
            class="btn btn-secondary"
            data-dismiss="modal">Close</button>
          <button
            type="button"
            class="btn btn-success"
            @click="inviteStudents">Invite</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  name: 'MembersInviteModal',
  props: {
    show: { type: Boolean, default: false },
    cId: { type: Number, default: 0 },
    gId: { type: Number, default: 0 },
  },
  data() {
    return {
      studentsList: [],
    };
  },
  computed: {
    students() {
      return this.$store.state.students;
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
  created() {
    this.$store.dispatch('fetchStudents');
  },
  methods: {
    inviteStudents() {
      const data = {
        cId: this.cId,
        gId: this.gId,
        studentsList: this.studentsList,
      };

      this.$store.dispatch('inviteStudents', data);

      $(this.$el).modal('hide');
    },
  },
};
</script>
