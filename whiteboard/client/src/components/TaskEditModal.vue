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
          <h5 class="modal-title">Edit Task</h5>
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
            @submit.prevent="updateTask">

            <div class="form-group row">
              <label
                for="input-name"
                class="col-sm-3 col-form-label">Task Name</label>
              <div class="col-sm-9">
                <input
                  id="input-name"
                  v-model="tmpTask.name"
                  type="text"
                  class="form-control"
                  placeholder="Task Name">
              </div>
            </div>

            <EditFieldRich
              v-model="tmpTask.description"
              :enable-readonly="false"
              label="Task Description:" />

            <div class="form-group row">
              <label
                for="input-format"
                class="col-sm-3 col-form-label">Task Format</label>
              <div class="col-sm-9">
                <select
                  id="input-description"
                  v-model="tmpTask.format"
                  class="form-control custom-select"
                  placeholder="Task Format">
                  <option :value="2">Open Question</option>
                  <option :value="1">Test</option>
                </select>
              </div>
            </div>

            <template v-if="tmpTask.format === 1">
              <div class="form-group row align-items-center">
                <label
                  for="eval-schema"
                  class="col-sm-3 col-form-label">Evaluation schema</label>
                <div class="col-sm-9">

                  <div class="form-group form-check pl-0 mb-0 align-middle">
                    <input
                      v-model="substractPoints"
                      type="checkbox">
                    <label class="form-check-label">Substract points for wrong answers</label>
                  </div>

                </div>
              </div>
              <form
                v-for="(question, i) in questions"
                :key="i">
                <div
                  class="form-group row">
                  <label
                    :for="'question-' + i"
                    class="col-sm-3 col-form-label">Question {{ i + 1 }}</label>
                  <div class="col-sm-9">
                    <input
                      :id="'question-' + i"
                      v-model="question.text"
                      class="form-control"
                      @input="questionChange(i)">
                  </div>
                </div>
                <div
                  v-for="(answer, j) in question.answers"
                  :key="j"
                  class="form-group row">
                  <label
                    :for="'answer-' + i + '-' + j"
                    class="col-sm-3 offset-sm-1 col-form-label">Answer {{ j + 1 }}</label>
                  <div class="input-group col-sm-8">
                    <div class="input-group-prepend">
                      <div class="input-group-text">
                        <input
                          v-model="answer.isCorrect"
                          type="checkbox"
                          @change="isCorrectChange(i, j)">
                      </div>
                    </div>
                    <input
                      :id="'answer-' + i + '-' + 'j'"
                      v-model="answer.text"
                      class="form-control"
                      @input="answerChange(i, j)">
                  </div>
                </div>
              </form>
            </template>

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
            @click="updateTask">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import EditFieldRich from '@/components/EditFieldRich';

export default {
  name: 'TaskEditModal',
  components: {
    EditFieldRich,
  },
  props: {
    'course-id': { type: Number, default: 0 },
  },
  data() {
    return {
      tmpTask: {
        name: null,
        description: null,
        format: 2,
      },
      questions: [],
      substractPoints: false,
    };
  },
  computed: {
    task() {
      return Object.assign({}, this.$store.state.currentTask);
    },
    show() {
      return this.$store.state.showTaskEdit;
    },
  },
  watch: {
    task(val) {
      if (Object.keys(val).length === 0) return;

      this.tmpTask = Object.assign({}, val);

      this.substractPoints = val.test.computing_system === 2;

      const questions = [];
      val.test.questions.forEach((q) => {
        const tmpQuestion = {};
        tmpQuestion.text = q.text;
        tmpQuestion.answers = [];


        q.answers.forEach((ans) => {
          const tmpAnswer = {};
          tmpAnswer.text = ans.text;
          tmpAnswer.isCorrect =
            val.test.correctAnswers[q.id].indexOf(ans.id) !== -1;

          tmpQuestion.answers.push(tmpAnswer);
        });

        tmpQuestion.answers.push({
          text: '',
          isCorrect: false,
        });
        questions.push(tmpQuestion);
      });

      questions.push({
        text: '',
        answers: [
          { text: '', isCorrect: false },
        ],
      });
      this.questions = questions;
    },
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');

        const component = this;
        $(this.$el).one('hidden.bs.modal', () => {
          component.$store.commit('setCurrentTask', {});
          component.$store.commit('toggleTaskEdit');
        });
      }
    },
  },
  methods: {
    updateTask() {
      const payload = { courseId: this.courseId };

      if (this.tmpTask.format === 1) {
        const correctAnswers = {};
        const questionsData = this.questions
          .filter(el => !!el.text)
          .map((el, i) => {
            let answers = el.answers
              .filter(answ => !!answ.text)
              .map((answ, j) => Object.assign({}, answ, { id: j }));

            correctAnswers[i] = answers.reduce((accumulator, currentVal) => {
              if (!!currentVal.text && currentVal.isCorrect) {
                accumulator.push(currentVal.id);
              }

              return accumulator;
            }, []);

            answers = answers.map(({ id, text }) => ({ id, text }));

            return Object.assign({}, el, { id: i, answers });
          });

        payload.task = Object.assign(
          {},
          this.tmpTask,
          {
            test: {
              questions: questionsData,
              correctAnswers,
              computing_system: this.substractPoints ? 2 : 1,
            },
          });
      } else {
        payload.task = this.tmpTask;
      }

      this.$store.dispatch(
        'updateTask',
        payload,
      );
      $(this.$el).modal('hide');
    },
    questionChange(id) {
      const questionVal = this.questions[id].text;
      const questionsNum = this.questions.length;

      if (questionVal !== '' && id === questionsNum - 1) {
        this.questions.push(
          {
            text: '',
            answers: [
              { text: '', isCorrect: false },
            ],
          },
        );
      } else if (questionVal === '' && id === questionsNum - 2) {
        this.questions.pop();
      }
    },
    answerChange(qId, aId) {
      const answerVal = this.questions[qId].answers[aId].text;
      const answersNum = this.questions[qId].answers.length;

      if (answerVal !== '' && aId === answersNum - 1) {
        this.questions[qId].answers.push({ text: '', isCorrect: false });
      } else if (answerVal === '' && aId === answersNum - 2) {
        this.questions[qId].answers.pop();
        this.questions[qId].answers[aId].isCorrect = false;
      }
    },
    isCorrectChange(qId, aId) {
      const answerVal = this.questions[qId].answers[aId].text;

      if (answerVal === '' || answerVal === null) {
        this.questions[qId].answers[aId].isCorrect = false;
      }
    },
  },
};
</script>

<style>
.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.25);
  background-color: rgba(0, 0, 0, 0.10);
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.25);
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
