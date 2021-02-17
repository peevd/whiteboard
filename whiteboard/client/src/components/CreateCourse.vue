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
          <h3 class="modal-title">Create New Course</h3>
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
            class="text-left">
            <div class="form-group row">
              <label
                for="input-name"
                class="col-sm-3 col-form-label">Course Name</label>
              <div class="col-sm-9">
                <input
                  id="input-name"
                  v-model="newCourse.name"
                  type="text"
                  class="form-control"
                  placeholder="Course Name"
                  @change="checkName">
                <small v-if="nameError">Name is required</small>
              </div>
            </div>
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
            <EditFieldRich
              v-model="newCourse.description"
              :enable-readonly="false"
              label="Course Description"
              @change="checkDescription" />
            <div
              class="row mb-3"
              style="margin-top: -15px;">
              <div class="col-sm-9 offset-sm-3">
                <small v-if="descriptionError">Description is required</small>
              </div>
            </div>
            <div class="form-group row">
              <label
                for="input-price"
                class="col-sm-3 col-form-label">Course Price (€)</label>
              <div class="col-sm-9">
                <input
                  id="input-price"
                  v-model="newCourse.price"
                  type="number"
                  min="0.00"
                  step="0.01"
                  class="form-control"
                  required
                  placeholder="Course Price in €"
                  @change="checkPrice">
                <small v-if="priceError">Price is required and not less than 0</small>
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
            @click="createCourse">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import EditFieldRich from '@/components/EditFieldRich';

export default {
  name: 'CreateCourse',
  components: {
    EditFieldRich,
  },
  props: {
    show: { type: Boolean, default: false },
  },
  data() {
    return {
      newCourse: {
        name: '',
        description: '',
        price: null,
      },
      file: null,
      fileName: null,
      priceError: false,
      descriptionError: false,
      nameError: false,
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
  created() {
  },
  methods: {
    checkPrice() {
      if (this.newCourse.price === null || this.newCourse.price < 0) {
        this.priceError = true;
      } else {
        this.priceError = false;
      }
    },
    checkDescription() {
      if (this.newCourse.description === null || this.newCourse.description === '') {
        this.descriptionError = true;
      } else {
        this.descriptionError = false;
      }
    },
    checkName() {
      if (this.newCourse.name === null || this.newCourse.name === '') {
        this.nameError = true;
      } else {
        this.nameError = false;
      }
    },
    createCourse() {
      this.checkPrice();
      this.checkDescription();
      this.checkName();

      if (this.priceError || this.descriptionError || this.nameError) {
        return;
      }

      this.$store.dispatch('newCourse', this.newCourse)
        .then((cId) => {
          const formData = new FormData();
          formData.append('file', this.file);
          const data = {
            cId,
            formData,
          };
          this.$store.dispatch('postThumbnail', data);
          this.newCourse = {
            name: '',
            description: '',
            price: null,
          };
          this.file = null;
          this.fileName = null;
        });

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

<style>
</style>
