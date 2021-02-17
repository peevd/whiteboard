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
        <div class="modal-header">
          <h5 class="modal-title">Edit Thumbnail</h5>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form class="form">
            <div class="form-group row align-items-center">
              <label
                for="input-thumbnail"
                class="col-sm-3 col-form-label">Course Thumbnail</label>
              <div class="col-sm-9">
                <div class="custom-file">
                  <input
                    id="input-thumbnail"
                    type="file"
                    class="custom-file-input"
                    @change="handleThumbnailChange">
                  <label class="custom-file-label">{{ fileName || 'Choose file...' }}</label>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-dismiss="modal">Close</button>
          <button
            type="button"
            class="btn btn-success"
            @click="updateThumbnail">Update</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  name: 'CourseThumbnailEditModal',
  props: {
    show: { type: Boolean, default: false },
    cId: { type: Number, default: 0 },
    oldPicture: { type: String, default: '' },
  },
  data() {
    return {
      file: null,
      fileName: null,
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
  },
  methods: {
    updateThumbnail() {
      const formData = new FormData();
      formData.append('file', this.file);

      const data = {
        cId: this.cId,
        formData,
      };

      if (this.oldPicture === '') {
        this.$store.dispatch('postThumbnail', data);
      } else {
        this.$store.dispatch('updateThumbnail', data);
      }

      $(this.$el).modal('hide');
    },
    handleThumbnailChange() {
      const input = this.$el.querySelector('#input-thumbnail');
      this.file = input.files[0];
      this.fileName = this.file.name;
    },
  },
};
</script>
