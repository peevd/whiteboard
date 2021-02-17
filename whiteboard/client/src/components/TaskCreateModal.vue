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
          <h5 class="modal-title">New Task</h5>
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
            @submit.prevent="createTask">
            <div class="form-group row">
              <label
                for="input-name"
                class="col-sm-3 col-form-label">Task Name</label>
              <div class="col-sm-9">
                <input
                  id="input-name"
                  v-model="task.name"
                  type="text"
                  class="form-control"
                  placeholder="Task Name">
              </div>
            </div>
            <EditFieldRich
              v-model="task.description"
              :enable-readonly="false"
              label="Task Description" />

            <div class="form-group row">
              <label
                for="input-format"
                class="col-sm-3 col-form-label">Task Format</label>
              <div class="col-sm-9">
                <select
                  id="input-description"
                  v-model="task.format"
                  class="form-control custom-select">
                  <option :value="2">Open Question</option>
                  <option :value="1">Test</option>
                </select>
              </div>
            </div>

            <template v-if="task.format === 1">
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
              <div
                v-if="missingCorrectAnswer"
                class="row">
                <div class="col text-center">
                  <small class="text-danger">
                    All questions need to have atleast one correct answer
                  </small>
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
                      placeholder="What?"
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
                      placeholder="That?"
                      @input="answerChange(i, j)">
                  </div>
                </div>
              </form>
            </template>

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
            @click="createTask">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import EditFieldRich from '@/components/EditFieldRich';

export default {
  name: 'TaskCreateModal',
  components: {
    EditFieldRich,
  },
  props: {
    'course-id': { type: Number, default: 0 },
  },
  data() {
    return {
      missingCorrectAnswer: false,
      task: {
        name: null,
        description: null,
        format: 2,
      },
      questions: [{
        text: '',
        answers: [
          {
            text: '',
            isCorrect: false,
          },
        ],
      }],
      substractPoints: false,
    };
  },
  computed: {
    show() {
      return this.$store.state.showTaskCreate;
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');

        const component = this;
        $(this.$el).one('hidden.bs.modal', () => {
          component.$store.commit('toggleTaskCreate');
        });
      }
    },
  },
  methods: {
    createTask() {
      const payload = { courseId: this.courseId };

      if (this.task.format === 1) {
        this.missingCorrectAnswer = false;

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

            if (correctAnswers[i].length === 0) {
              this.missingCorrectAnswer = true;
            }

            answers = answers.map(({ id, text }) => ({ id, text }));

            return Object.assign({}, el, { id: i, answers });
          });

        if (this.missingCorrectAnswer) return;

        payload.task = Object.assign(
          {},
          this.task,
          {
            test: {
              questions: questionsData,
              correctAnswers,
              computing_system: this.substractPoints ? 2 : 1,
            },
          });
      } else {
        payload.task = this.task;
      }

      this.$store.dispatch(
        'createTask',
        payload,
      );

      $(this.$el).modal('hide');
      this.task = { name: '', description: '', format: 2 };
      this.substractPoints = false;
      this.questions = [{
        text: '',
        answers: [
          {
            text: '',
            isCorrect: false,
          },
        ],
      }];
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
</style>
