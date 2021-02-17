<template>
  <div
    class="form-group row">
    <label class="col-sm-3 col-form-label">
      {{ label }}
    </label>
    <div class="col-sm-9">
      <FancyEditor
        v-model="val"
        @change="onChange"/>
    </div>
  </div>
</template>

<script>
import FancyEditor from '@/components/FancyEditor';

export default {
  name: 'EditFieldRich',
  components: { FancyEditor },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    enableReadonly: { type: Boolean, default: true },
    label: { type: String, default: '' },
    value: { type: String, default: '' },
  },
  data() {
    return {
      editor: null,
      changed: false,
      afterChange: false,
      val: this.value,
    };
  },
  watch: {
    value(newVal) {
      this.val = newVal;
    },
  },
  methods: {
    onChange() {
      this.$emit('change', this.val);
    },
  },
};
</script>

<style scoped>
.btn.border {
  border-color: #b7b7b7 !important;
  border-radius: 0.25rem;
  margin-bottom: 0.25rem;
  padding: 5px;
}

.editor {
  padding: 10px;
  border-radius: 0.25rem;
}

.editor:hover {
  border-radius: 0.25rem;
}

.bg-light {
  background-color: #f9f9f9;
}

.editor > .ProseMirror-focused {
  outline: none;
}

.o-0 {
  outline: none !important;
}

.input-group-append > .input-group-text {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
</style>
