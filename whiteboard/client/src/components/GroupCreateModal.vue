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
          <h5 class="modal-title">Group</h5>
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
            class="text-left"
            @submit="createGroup">
            <div class="form-group row">
              <label
                for="input-name"
                class="col-sm-3 col-form-label">Group Name</label>
              <div class="col-sm-9">
                <input
                  id="input-name"
                  v-model="group.name"
                  type="text"
                  class="form-control"
                  placeholder="Group Name">
                <small v-if="nameEmpty">Field is required</small>
              </div>
            </div>
            <div class="form-group row">
              <label
                for="input-size"
                class="col-sm-3 col-form-label">Group Size</label>
              <div class="col-sm-9">
                <input
                  id="input-size"
                  v-model="group.max_members"
                  type="number"
                  class="form-control"
                  placeholder="Group Size"
                  min="1">
                <small v-if="sizeError">Field is required and must be a number</small>
                <small v-if="sizeTooSmall">Size must be greater than 0</small>
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
            @click="createGroup">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  name: 'GroupCreateModal',
  props: {
    'course-id': { type: Number, default: 0 },
  },
  data() {
    return {
      group: {
        name: '',
        max_members: '',
      },
      sizeError: false,
      sizeTooSmall: false,
      nameEmpty: false,
    };
  },
  computed: {
    show() {
      return this.$store.state.showGroupCreate;
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');

        const component = this;
        $(this.$el).one('hidden.bs.modal', () => {
          component.$store.commit('toggleGroupCreate');
        });
      }
    },
  },
  methods: {
    checkName() {
      this.nameEmpty = this.group.name === '';
    },
    checkSize() {
      this.sizeError = this.group.max_members === '';

      if (!this.sizeError) {
        const size = parseInt(this.group.max_members, 10);
        this.sizeTooSmall = size <= 0;
      }
    },
    createGroup() {
      this.checkName();
      this.checkSize();

      if (this.nameEmpty || this.sizeError || this.sizeTooSmall) {
        return;
      }

      this.group.max_members = parseInt(this.group.max_members, 10);

      this.$store.dispatch(
        'createGroup',
        {
          group: this.group,
          cId: this.courseId,
        },
      );

      $(this.$el).modal('hide');
      this.group = { name: '', max_members: null };
      this.nameEmpty = false;
      this.sizeError = false;
      this.sizeTooSmall = false;
    },
  },
};
</script>

<style scoped>
.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.25);
  background-color: rgba(0, 0, 0, 0.10);
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.25);
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
