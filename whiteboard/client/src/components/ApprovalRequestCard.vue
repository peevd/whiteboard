<template>
  <div
    class="col-md-12 mb-4">
    <div class="card shadow bg-default">
      <div class="card-body">
        <div class="row">
          <div class="col-auto align-self-center">
            <div class="row">
              <div class="col text-center">
                {{ parseTime(request.date) }}
              </div>
            </div>
            <div class="row">
              <div class="col text-center">
                {{ parseDate(request.date) }}
              </div>
            </div>
          </div>
          <div class="col-auto align-self-center">
            {{ request.course_name }}
          </div>
          <div class="col">
            <template v-if="!enableEdit">
              {{ request.note || 'No note available' }}
            </template>
            <template v-else>
              <textarea
                v-model="note"
                class="form-control"
                @input="onNoteChange" />
              <small
                v-if="noteError"
                class="text-danger">Note is required</small>
            </template>
          </div>
          <div class="col-auto align-self-center">
            <template v-if="!enableEdit">
              {{ parseStatus(request.status) }}
            </template>
            <template v-else>
              <select
                v-model="status"
                class="custom-select"
                @change="onChange">
                <option
                  value="1"
                  disabled>
                  {{ parseStatus(1) }}
                </option>
                <option value="2">{{ parseStatus(2) }}</option>
                <option value="3">{{ parseStatus(3) }}</option>
              </select>
            </template>
          </div>
          <div
            v-if="showOpenBtn"
            class="col-auto align-self-center">
            <button
              class="btn btn-success"
              @click="openRequest(request.id)">
              Open
            </button>
          </div>
          <div
            v-if="enableEdit"
            class="col-auto align-self-center">
            <button
              :class="[ !modified || loading ? 'disabled' : '' ]"
              class="btn btn-success"
              @click="updateRequest">
              <template v-if="loading">
                <custom-icon
                  icon="spinner"
                  size="1x"
                  class="spin-svg" />
              </template>
              <template v-else>
                Save
              </template>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'ApprovalRequestCard',
  props: {
    request: {
      type: Object,
      default: () => {},
    },
    showOpenBtn: {
      type: Boolean,
      default: false,
    },
    enableEdit: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      note: '',
      noteError: false,
      status: '1',
      modified: false,
      loading: false,
    };
  },
  watch: {
    request(r) {
      this.note = r.note;
      this.status = r.status;
    },
  },
  methods: {
    parseDate(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('DD/MM/YYYY');
    },
    parseTime(input) {
      return moment(input, 'YYYY-MM-DD h:mm:ss').format('H:mm');
    },
    parseStatus(input) {
      switch (input) {
        case 1:
          return 'New';
        case 2:
          return 'Needs Fixing';
        case 3:
          return 'Approved';
        default:
          return 'N/A';
      }
    },
    openRequest(id) {
      this.$router.push(`/admin/requests/${id}`);
    },
    onNoteChange() {
      if (this.note !== this.request.note || Number(this.status) !== this.request.status) {
        this.modified = true;
      } else {
        this.modified = false;
      }

      if (!this.note) {
        this.noteError = true;
      } else {
        this.noteError = false;
      }
    },
    onChange() {
      if (this.note !== this.request.note || Number(this.status) !== this.request.status) {
        this.modified = true;
      } else {
        this.modified = false;
      }
    },
    updateRequest() {
      if (!this.note || this.note === '') {
        this.noteError = true;
        return;
      }

      this.noteError = false;

      if (this.note !== this.request.note || this.status !== this.request.status) {
        // update
        const data = Object.assign({}, this.request, { note: this.note, status: this.status });
        this.loading = true;
        this.$store.dispatch('updateApprovalRequest', data)
          .then(() => { this.modified = false; this.loading = false; })
          .catch(() => { this.loading = false; });
      }
    },
  },
};
</script>
