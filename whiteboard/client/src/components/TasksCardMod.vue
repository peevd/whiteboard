<template>
  <div class="card shadow bg-default">
    <div class="card-body">
      <div class="row">
        <div class="col">
          <h3 class="mb-0">Tasks</h3>
        </div>
      </div>
      <div
        v-for="t in tasks"
        :key="t.id"
        class="card bg-default mt-4">
        <div
          class="card-header p-0 bg-default click-pointer btn-hover"
          @click="toggleExpand(t.id)">
          <div class="row m-0">
            <div class="col-8 p-3">
              <h5 class="mb-0">{{ t.name }}</h5>
            </div>
            <div class="col-4 p-3 bg-blue">
              <p class="mb-0">{{ parseFormat(t.format) }}</p>
            </div>
          </div>
        </div>
        <div
          v-show="isExpanded(t.id)"
          class="card-body">

          <div class="row">
            <div class="col">
              <div
                class="ProseMirror"
                v-html="t.description" />
            </div>
          </div>

          <div
            v-if="t.format === 1"
            class="row mt-4">
            <div class="col">
              <div
                v-for="(q, i) in t.test.questions"
                :key="q.id"
                class="row mb-4">
                <div class="col">
                  <div class="row">
                    <div
                      class="col">
                      {{ ++i }}. {{ q.text }}
                    </div>
                  </div>
                  <div class="row">
                    <div class="col pl-4">
                      <div
                        v-for="a in q.answers"
                        :key="a.id"
                        class="form-check">
                        <input
                          :id="`answer-${q.id}-${a.id}`"
                          :value="a.id"
                          :name="`answers-${q.id}`"
                          disabled
                          class="form-check-input input-radio"
                          type="radio">
                        <label
                          :for="`answer-${q.id}-${a.id}`"
                          class="form-check-label">
                          {{ a.text }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TasksCardMod',
  props: {
    tasks: {
      type: Array,
      default: () => ([]),
    },
  },
  data: () => ({
    expanded: [],
  }),
  methods: {
    toggleExpand(id) {
      if (this.expanded.findIndex(el => el === id) !== -1) {
        this.expanded = this.expanded.filter(el => el !== id);
      } else {
        this.expanded.push(id);
      }
    },
    isExpanded(id) {
      return this.expanded.findIndex(el => el === id) !== -1;
    },
    parseFormat(format) {
      switch (format) {
        case 1:
          return 'Test';
        case 2:
          return 'Open question';
        default:
          return 'N/A';
      }
    },
  },
};
</script>
