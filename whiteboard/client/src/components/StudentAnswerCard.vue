<template>
  <div class="card mb-2">
    <div
      class="card-header py-3 bg-default click-pointer btn-hover"
      @click="toggleBody">

      <div class="row">
        <div class="col">
          <h5 class="m-0">{{ task.name }}</h5>
        </div>
        <div class="col-auto">
          <h5 class="m-0">{{ answer.grade !== null ? answer.grade + '%' : 'Not graded' }}</h5>
        </div>
      </div>

    </div>

    <div
      v-show="showBody"
      class="card-body">

      <div
        class="row mb-2">
        <div class="col">
          <div
            class="ProseMirror"
            v-html="task.description" />
        </div>
      </div>

      <div class="row">
        <div class="col">

          <template
            v-if="task.format === 1">

            <div
              v-for="(q, i) in task.test.questions"
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

                    <form>
                      <div
                        v-for="a in q.answers"
                        :key="a.id"
                        class="form-check">

                        <input
                          :id="`answer-${task.id}-${q.id}-${a.id}`"
                          :checked="isAnswered(answer, q.id, a.id)"
                          :value="a.id"
                          :name="`answers-${q.id}`"
                          disabled
                          class="form-check-input input-radio"
                          type="radio">
                        <label
                          :for="`answer-${task.id}-${q.id}-${a.id}`"
                          class="form-check-label">
                          {{ a.text }}
                        </label>

                      </div>
                    </form>

                  </div>
                </div>

              </div>

            </div>

          </template>
          <template
            v-else>

            <p>Answer: {{ answer.answers }}</p>

          </template>

        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentAnswerCard',
  props: {
    answer: {
      type: Object,
      default: () => {},
    },
    task: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      showBody: false,
    };
  },
  methods: {
    toggleBody() {
      this.showBody = !this.showBody;
    },
    isAnswered(answer, qId, aId) {
      let flag = false;
      answer.answers.forEach((ans) => {
        if (ans.q_id === qId) {
          flag = ans.a_id.indexOf(aId) !== -1;
        }
      });

      return flag;
    },
  },
};
</script>

<style scoped>
.asd {
  margin: -20px !important;
  padding: 20px 5px;
}
</style>
