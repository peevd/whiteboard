<template>
  <div
    id="group-edit"
    class="page-content row justify-content-between">
    <div class="col-md-12 col-xl-6">
      <div class="row mb-4">
        <div class="col-sm-12">
          <div class="bg-default card shadow">
            <div class="card-body">

              <div
                v-if="!editGroup"
                class="row">
                <div class="col">
                  <h3 class="mb-3">{{ group.name }}</h3>
                  <p class="mb-0">Members: {{ group.members_in || 0 }}/{{ group.max_members }}</p>
                </div>
                <div class="col-auto">
                  <button
                    id="edit-group"
                    class="btn btn-sm btn-default border"
                    title="Edit"
                    @click="enableEditGroup">
                    <font-awesome-icon
                      icon="edit"
                      size="1x" />
                  </button>
                </div>
              </div>

              <div
                v-else
                class="row">
                <div class="col">
                  <form
                    class="form"
                    @submit="updateGroup">
                    <div class="form-group">
                      <input
                        v-model="groupModified.name"
                        class="form-control"
                        placeholder="Group name..."
                        type="text">
                    </div>
                    <div class="form-group">
                      <input
                        v-model="groupModified.max_members"
                        class="form-control"
                        placeholder="Group Size"
                        type="number">
                    </div>
                    <div class="d-flex justify-content-end">
                      <button
                        class="btn btn-sm btn-success mr-2"
                        @click="updateGroup">Save</button>
                      <button
                        class="btn btn-sm btn-danger"
                        @click="disableEditGroup">Cancel</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-12">
          <BoardCard :data="boardCardData" />
        </div>
      </div>
    </div>
    <div class="col-md-12 col-xl-6">
      <div class="row mb-4">
        <div class="col-sm-12">
          <div class="bg-default card shadow">
            <div class="card-body">

              <div class="row mb-3">
                <div class="col">
                  <h3>Participants</h3>
                </div>
              </div>

              <div
                v-if="members.length !== 0"
                class="row">
                <div class="col">
                  <table
                    class="table table-borderless table-hover">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Remove</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(member, i) in members"
                        :key="member.id"
                        class="student-row"
                        @click="toggleStudentModal(member.id)">
                        <td class="align-middle">{{ ++i }}</td>
                        <td class="align-middle content">
                          {{ member.first_name }} {{ member.last_name }}
                        </td>
                        <td class="align-middle">
                          <button
                            class="btn btn-danger"
                            @click="kickStudent(member.id)">
                            <font-awesome-icon
                              icon="trash"
                              size="xs" />
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- no participants here -->
              <div
                v-else
                class="row">
                <div class="col">
                  <div class="jumbotron p-4 mb-0 text-center">
                    <h5 class="mb-0">No participants yet</h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-12">
          <AppointmentsCard
            :events="events"
            :c-id="cId"
            :g-id="gId" />
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <PPTSelectCard :c-id="cId" />
        </div>
      </div>

    </div>

    <MembersInviteModal
      :show="showInviteModal"
      :c-id="cId"
      :g-id="gId"
      @hide="toggleInviteModal" />

    <StudentModal
      :show="showStudentModal"
      :student="currentStudent"
      :c-id="cId"
      @hide="toggleStudentModal" />

  </div>
</template>

<script>
import AppointmentsCard from '@/components/AppointmentsCard';
import BoardCard from '@/components/BoardCard';
import EditField from '@/components/EditField';
import MembersInviteModal from '@/components/MembersInviteModal';
import PPTSelectCard from '@/components/PPTSelectCard';
import StudentModal from '@/components/StudentModal';

export default {
  name: 'EditGroup',
  components: {
    AppointmentsCard,
    BoardCard,
    EditField,
    MembersInviteModal,
    PPTSelectCard,
    StudentModal,
  },
  data() {
    return {
      editGroup: false,
      showInviteModal: false,
      showStudentModal: false,
      groupModified: {
        name: '',
        max_members: '',
      },
      currentStudent: {},
    };
  },
  computed: {
    cId() {
      return Number(this.$route.params.cId);
    },
    course() {
      return this.$store.state.currentCourse;
    },
    gId() {
      return Number(this.$route.params.gId);
    },
    group() {
      return this.$store.state.currentGroup;
    },
    members() {
      return this.$store.state.currentGroupMembers;
    },
    board() {
      return this.$store.state.currentBoard;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    boardSnapshot() {
      return this.$store.state.currentBoardSnapshot;
    },
    events() {
      return this.$store.state.events;
    },
    currentTask() {
      const taskId = this.board.task_id;
      const task = this.$store.state.currentTasks.find(el => el.id === taskId);
      return task ? task.name : 'unknown';
    },
    boardCardData() {
      return {
        board: this.board,
        boardSnapshot: this.boardSnapshot,
        currentTask: this.currentTask,
        cId: this.cId,
        gId: 1,
        href: `/my-courses/${this.cId}/groups/${this.gId}/board`,
      };
    },
  },
  created() {
    this.$store.dispatch('fetchCourse', this.cId)
      .then(() => {
        this.$store.dispatch('setBreadcrumbs', [
          {
            name: this.course.name,
            href: `/my-courses/${this.course.id}`,
          },
        ]);
      });
    this.$store.dispatch('fetchGroup', { cId: this.cId, gId: this.gId });
    this.$store.dispatch('fetchGroupMembers', { cId: this.cId, gId: this.gId });
    this.$store.dispatch('fetchBoard', { cId: this.cId, gId: this.gId });
    this.$store.dispatch('fetchBoardSnapshot', { cId: this.cId, gId: this.gId });
    this.$store.dispatch('fetchGroupEvents', { cId: this.cId, gId: this.gId });
  },
  methods: {
    updateGroup() {
      // todo: check if max_members is > members_in
      this.$store.dispatch('updateGroup', { cId: this.cId, group: this.groupModified });
      this.editGroup = false;
    },
    enableEditGroup() {
      this.groupModified = Object.assign({}, this.group);
      this.editGroup = true;
    },
    disableEditGroup() {
      this.editGroup = false;
    },
    toggleInviteModal() {
      this.showInviteModal = !this.showInviteModal;
    },
    kickStudent(id) {
      // todo: remove student
      const data = {
        cId: this.cId,
        gId: this.gId,
        pId: id,
      };

      this.$store.dispatch('kickParticipant', data);
    },
    toggleStudentModal(id) {
      this.currentStudent = this.members.find(el => el.id === id);
      this.showStudentModal = !this.showStudentModal;
    },
  },
};
</script>

<style>
#group-edit > div {
  padding: 20px;
}

#group-edit .readonly > *:first-child {
  padding: 0.375rem 0.75rem !important;
  width: 1% !important;
  -ms-flex: 1 1 auto;
  -webkit-box-flex: 1;
  flex: 1 1 auto;
}

#group-edit .readonly:hover > *:first-child {
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  // cursor: pointer;
}

#group-edit .readonly input[type='number'] {
  -moz-appearance:textfield;
}

#group-edit .readonly input[type=number]::-webkit-inner-spin-button,
#group-edit .readonly input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  display: none;
  margin: 0;
}

#group-edit .readonly >div {
  display: none;
}

#group-edit .readonly:hover >div {
  display: inherit;
}

td.content {
  width: 100%;
}

.board-preview {
  width: 100%;
  padding: 10px;
  background: url('../assets/bg_plus.png');
}

.board-preview > svg {
  width: 100%;
  height: 100%;
}

.card-body #edit-group {
  display: none;
}

.card-body:hover #edit-group {
  display: block;
}

.student-row {
  cursor: pointer;
}
</style>
