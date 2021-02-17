<template>
  <div class="form-group row">
    <label
      for="field"
      class="col-sm-3 col-form-label">{{ label }}</label>
    <div
      :class="{readonly: readonly}"
      class="input-group col-sm-9">
      <textarea
        v-if="type === 'textarea'"
        id="field"
        :value="value"
        :readonly="readonly"
        :class="[readonly ? readonlyClass : editClass]"
        :type="type"
        @focus="focusField"
        @blur="blurField"
        @input="$emit('input', $event.target.value)" />
      <input
        v-else
        id="field"
        :value="value"
        :readonly="readonly"
        :class="[readonly ? readonlyClass : editClass]"
        :type="type"
        @focus="focusField"
        @blur="blurField"
        @input="$emit('input', $event.target.value)">
      <div
        v-if="readonly"
        class="input-group-append">
        <span
          class="input-group-text bg-default">
          <font-awesome-icon
            icon="edit"/>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditField',
  props: {
    label: { type: String, default: '' },
    value: { type: [String, Number], default: '' },
    editable: { type: Boolean, default: true },
    type: { type: String, default: 'text' },
  },
  data() {
    return {
      readonly: true,
      readonlyClass: 'form-control-plaintext',
      editClass: 'form-control',
    };
  },
  watch: {
    value() {
      this.changed = true;
    },
  },
  methods: {
    focusField() {
      this.readonly = false;
    },
    blurField() {
      this.readonly = true;
      if (this.changed) {
        this.$emit('save');
        this.changed = false;
      }
    },
  },
};
</script>

<style scoped>
</style>
