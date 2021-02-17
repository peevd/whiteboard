<template>
  <div class="card border shadow">
    <div class="card-body">
      <div class="row mb-4">
        <div class="col">
          <h3 class="mb-0">Presentations</h3>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col">
          <form
            class="form-inline row"
            @submit.prevent="handleUpload" >
            <div class="col">
              <div class="custom-file">
                <input
                  id="ppt-file"
                  ref="pptinput"
                  type="file"
                  class="custom-file-input"
                  @change="handleChange">
                <label
                  id="ppt-file-label"
                  class="custom-file-label"
                  for="ppt-file" >
                  {{ filename }}
                </label>
              </div>
            </div>
            <div class="col-auto">
              <button
                type="submit"
                class="btn btn-success col-auto">
                Upload
              </button>
            </div>
            <small
              v-show="extError"
              class="text-danger">
              Filetype is not supported. Supported types are .ppt and .pptx
            </small>
          </form>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <PPTList
            :c-id="cId"
            :allow-select="false" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PPTList from '@/components/PPTList';

export default {
  name: 'PPTUploadCard',
  components: {
    PPTList,
  },
  props: {
    cId: { type: Number, default: 0 },
  },
  data() {
    return {
      file: null,
      filename: 'Choose file...',
      extError: false,
    };
  },
  computed: {
    ppts() {
      return this.$store.state.currentPPTs;
    },
  },
  methods: {
    handleChange() {
      this.file = this.$refs.pptinput.files[0];
      this.filename = this.file.name;

      const parts = this.filename.split('.');
      const ext = parts[parts.length - 1];

      if (ext !== 'ppt' && ext !== 'pptx') {
        this.extError = true;
        return;
      }

      this.extError = false;
    },
    handleUpload() {
      const formData = new FormData();
      formData.append('file', this.file);

      const data = {
        cId: this.cId,
        formData,
      };

      this.$store.dispatch('uploadPPT', data);

      this.$refs.pptinput.value = '';
      this.filename = 'Choose file...';
    },
  },
};
</script>

<style>
#ppt-file-label {
  justify-content: initial;
}
</style>
