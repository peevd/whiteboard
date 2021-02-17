<template>
  <div class="col-sm-12">
    <div class="row mb-2">
      <div class="col-sm-12">
        <div class="bg-default card shadow">
          <div class="card-body">
            <h3>Groups</h3>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12 col-xl-6 p-3">
        <div class="card bg-default shadow full-height">
          <div class="card-body row align-items-center justify-content-center">
            <a
              id="add-btn"
              href="#"
              class="link-success"
              @click.prevent="createGroup">
              <font-awesome-icon
                icon="plus-circle"
                size="6x" />
            </a>
          </div>
        </div>
      </div>
      <template v-for="group in groups">
        <div
          :key="group.id"
          class="col-md-12 col-xl-6 p-3">
          <GroupCard
            :group="group"
            :course-id="courseId"/>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import GroupCard from '@/components/GroupCard';

export default {
  name: 'CourseGroups',
  components: {
    GroupCard,
  },
  props: {
    courseId: { type: Number, default: 0 },
  },
  computed: {
    groups() {
      return this.$store.state.currentGroups;
    },
  },
  created() {
    this.$store.dispatch('fetchCourseGroups', this.courseId);
  },
  methods: {
    createGroup() {
      this.$store.commit('toggleGroupCreate');
    },
  },
};
</script>
