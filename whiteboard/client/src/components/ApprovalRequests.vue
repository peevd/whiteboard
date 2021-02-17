<template>
  <div
    class="row page-content justify-content-between">
    <div class="col-md-12">
      <div class="row mb-4">
        <div class="col">
          <div class="card bg-default shadow">
            <div class="card-body">
              <div class="row">
                <div class="col-6">
                  <div class="input-group">
                    <div class="input-group-prepend">
                      <span class="input-group-text">Status</span>
                    </div>
                    <select
                      v-model="filterStatus"
                      class="custom-select">
                      <option value="1">New</option>
                      <option value="2">Needs Fixing</option>
                      <option value="3">Approved</option>
                    </select>
                  </div>
                </div>
                <div class="col-6">
                  <Datetime
                    v-model="filterDate"
                    type="date"
                    input-id="datetime-input"
                    input-class="form-control"
                    class="input-group cd"
                    format="DD">
                    <template slot="before">
                      <div class="input-group-prepend">
                        <span class="input-group-text">Date</span>
                      </div>
                    </template>
                    <template slot="after">
                      <div class="input-group-append">
                        <button
                          class="btn btn-outline-secondary round-right"
                          type="button"
                          @click="clearDate">X</button>
                      </div>
                    </template>
                  </Datetime>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="loading"
        class="row justify-content-center">
        <div class="col-auto">
          <custom-icon
            icon="spinner"
            size="4x"
            class="spin-svg" />
        </div>
      </div>

      <div
        v-else
        class="row">
        <template v-if="requests.length === 0">
          <div class="col-12 col-md-6 offset-md-3">
            <div class="jumbotron">
              <h3 class="text-center mb-0">No requests available</h3>
            </div>
          </div>
        </template>
        <template v-else>
          <ApprovalRequestCard
            v-for="r in requests"
            :key="r.id"
            :request="r"
            :show-open-btn="true" />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import ApprovalRequestCard from '@/components/ApprovalRequestCard';
import 'vue-datetime/dist/vue-datetime.min.css';
import { Datetime } from 'vue-datetime';

export default {
  name: 'ApprovalRequests',
  components: {
    ApprovalRequestCard,
    Datetime,
  },
  data() {
    return {
      filterStatus: 1,
      filterDate: null,
      loading: false,
    };
  },
  computed: {
    requests() {
      return this.$store.state.approvalRequests;
    },
  },
  watch: {
    filterStatus() { this.onFilterChange(); },
    filterDate() { this.onFilterChange(); },
  },
  mounted() {
    this.loading = true;
    this.$store.dispatch('fetchApprovalRequests')
      .then(() => { this.loading = false; })
      .catch(() => { this.loading = false; });
  },
  methods: {
    onFilterChange() {
      const filters = [];

      if (this.filterStatus) {
        filters.push(`status=${this.filterStatus}`);
      }

      if (this.filterDate) {
        filters.push(`date=${this.filterDate.split('T')[0]}`);
      }

      this.loading = true;
      this.$store.dispatch('fetchApprovalRequestsByFilter', filters)
        .then(() => { this.loading = false; })
        .catch(() => { this.loading = false; });
    },
    clearDate() {
      this.filterDate = null;
    },
  },
};
</script>

<style>
.round-right {
  border-top-right-radius: 0.25rem !important;
  border-bottom-right-radius: 0.25rem !important;
}

.cd .vdatetime-popup {
  top: 50% !important;
}
</style>
