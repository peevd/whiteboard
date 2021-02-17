<template>
  <div
    id="course-edit"
    class="row page-content justify-content-between">
    <TaskEditModal
      v-if="editable"
      :course-id="id" />
    <TaskCreateModal
      v-if="editable"
      :course-id="id" />
    <GroupCreateModal
      v-if="editable"
      :course-id="id" />
    <GroupEditModal
      v-if="editable"
      :course-id="id" />
    <CourseThumbnailEditModal
      v-if="editable"
      :show="thumbnailEditModal"
      :c-id="id"
      :old-picture="course.picture"
      @hide="toggleThumbnailModal" />
    <div class="col-md-12 col-lg-6">
      <div class="row mb-4">
        <div class="col-sm-12">
          <div
            id="course-card"
            class="bg-default card shadow">
            <img
              :src="image"
              class="card-img-top"
              @click="toggleThumbnailModal">
            <div class="card-body">
              <div
                v-if="!editCourse"
                class="row">
                <div class="col">
                  <div class="row">
                    <div class="col">
                      <h1>{{ course.name }}</h1>
                    </div>
                    <div
                      v-if="editable"
                      class="col-auto">
                      <button
                        id="edit-course"
                        class="btn btn-sm btn-default border"
                        title="Edit"
                        @click="enableEditCourse">
                        <font-awesome-icon
                          icon="edit"
                          size="1x" />
                      </button>
                    </div>
                  </div>
                  <div
                    class="ProseMirror"
                    v-html="course.description"/>
                  <div class="row">
                    <div class="col">
                      <h5>Price: {{ course.price ? `${course.price}$` : '0' }}</h5>
                    </div>
                  </div>
                  <div
                    v-if="course.status !== 'open'"
                    class="row justify-content-end">
                    <div class="col-auto">
                      <button
                        v-if="!request || Object.keys(request).length === 0"
                        class="btn btn-success"
                        @click="sendOpenRequest">
                        Send open request
                      </button>
                      <button
                        v-else-if="request.status === 1"
                        class="btn btn-success disabled">
                        Awaiting approval
                      </button>
                      <button
                        v-else-if="request.status === 2"
                        class="btn btn-success"
                        @click="resendOpenRequest(request.id)">
                        Resend open request
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div
                v-if="editCourse"
                class="row">
                <div class="col">
                  <form
                    class="form"
                    @submit="updateCourse">
                    <div class="form-group">
                      <input
                        v-model="courseModified.name"
                        class="form-control"
                        placeholder="Course name..."
                        required
                        type="text">
                    </div>
                    <div class="form-group">
                      <FancyEditor
                        v-model="courseModified.description" />
                    </div>
                    <div class="form-group">
                      <input
                        v-model="courseModified.price"
                        class="form-control"
                        type="number"
                        required
                        min="0"
                        placeholder="Course price">
                    </div>
                    <div class="d-flex justify-content-end">
                      <button
                        class="btn btn-sm btn-success mr-2"
                        @click="updateCourse">Save</button>
                      <button
                        class="btn btn-sm btn-danger"
                        @click="disableEditCourse">Cancel</button>
                    </div>
                  </form>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
      <div class="row">

        <div class="col">
          <div class="card bg-default shadow">
            <div class="card-body">

              <div class="row mb-3 align-items-center">
                <div class="col-auto pr-1">
                  <custom-icon
                    icon="group"
                    size="3x" />
                </div>
                <div class="col">
                  <h3 class="mb-0 pt-1">Groups</h3>
                </div>
              </div>

              <div
                v-if="editable"
                class="card mb-4">
                <a
                  href="#"
                  class="btn-hover"
                  @click.prevent="createGroup">
                  <div class="card-body py-2 row justify-content-center">
                    <custom-icon
                      icon="addButton"
                      size="2x" />
                  </div>
                </a>
              </div>

              <div
                v-if="groups.length === 0"
                class="text-center pt-3">
                <p>No groups yet</p>
              </div>

              <div
                v-for="group in groups"
                :key="group.id"
                class="card mb-2">
                <div class="card-body py-3">
                  <div class="row align-items-center">
                    <div class="col">
                      <div class="row">
                        <div class="col">
                          <h5>{{ group.name }}</h5>
                        </div>
                      </div>
                      <div class="row justify-content-around">

                        <router-link
                          :to="`/my-courses/${id}/groups/${group.id}`"
                          class="btn btn-sm btn-success col-5">
                          Manage
                        </router-link>

                        <button
                          v-if="editable"
                          class="btn btn-sm btn-danger col-5"
                          @click="deleteGroup(group.id)">
                          Delete
                        </button>

                      </div>
                    </div>
                    <div class="col-auto text-center">
                      <p class="mb-0">Members</p>
                      <h3 class="mb-0 px-3">{{ group.members_in || 0 }}/{{ group.max_members }}</h3>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
    <div class="col-md-12 col-lg-6">
      <div class="row mb-4">
        <div class="col-sm-12">
          <div
            v-if="editable"
            class="bg-default card shadow">
            <div class="card-body">

              <div class="row mb-3 align-items-center">
                <div class="col-auto pr-1">
                  <custom-icon
                    icon="task"
                    size="3x" />
                </div>
                <div class="col">
                  <h3 class="mb-0 pt-1">Tasks</h3>
                </div>
              </div>

              <div
                v-if="editable"
                class="card mb-4">
                <a
                  href="#"
                  class="btn-hover"
                  @click.prevent="createTask">
                  <div class="card-body py-2 row justify-content-center">
                    <custom-icon
                      icon="addButton"
                      size="2x" />
                  </div>
                </a>
              </div>

              <div
                v-if="tasks.length === 0"
                class="text-center pt-3">
                <p>No tasks yet</p>
              </div>

              <div
                v-for="task in tasks"
                :key="task.id"
                class="card mb-2">
                <div class="card-body py-3">
                  <div class="row align-items-center">
                    <div class="col">
                      <div class="row">
                        <div class="col">
                          <h5>{{ task.name }}</h5>
                        </div>
                      </div>
                      <div class="row justify-content-around">

                        <button
                          class="btn btn-sm btn-success col-5"
                          @click="editTask(task.id)">
                          Edit
                        </button>

                        <button
                          class="btn btn-sm btn-danger col-5"
                          @click="deleteTask(task.id)">
                          Delete
                        </button>

                      </div>
                    </div>
                    <div class="col-auto">
                      <h3 class="mb-0 px-3">{{ task.task_number }}</h3>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
          <TasksCardMod
            v-else
            :tasks="tasks" />
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-12">
          <AppointmentsCard :events="events"/>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <PPTUploadCard :c-id="id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Placeholder from '@/assets/boardSnapshot.jpg';

import EditField from '@/components/EditField';
import EditFieldRich from '@/components/EditFieldRich';
import TaskEditModal from '@/components/TaskEditModal';
import TaskCreateModal from '@/components/TaskCreateModal';
import TaskCardOwner from '@/components/TaskCardOwner';
import TasksCardMod from '@/components/TasksCardMod';
import CourseGroups from '@/components/CourseGroups';
import GroupCreateModal from '@/components/GroupCreateModal';
import GroupEditModal from '@/components/GroupEditModal';
import FancyEditor from '@/components/FancyEditor';
import CourseThumbnailEditModal from '@/components/CourseThumbnailEditModal';
import AppointmentsCard from '@/components/AppointmentsCard';
import PPTUploadCard from '@/components/PPTUploadCard';

export default {
  name: 'EditCourse',
  components: {
    AppointmentsCard,
    CourseGroups,
    CourseThumbnailEditModal,
    EditField,
    EditFieldRich,
    FancyEditor,
    GroupCreateModal,
    GroupEditModal,
    PPTUploadCard,
    TaskCardOwner,
    TaskCreateModal,
    TaskEditModal,
    TasksCardMod,
  },
  data() {
    return {
      editCourse: false,
      courseModified: {
        name: '',
        description: '',
        price: '',
      },
      thumbnailEditModal: false,
    };
  },
  computed: {
    id() {
      return Number(this.$route.params.cId);
    },
    course() {
      return this.$store.state.currentCourse;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    groups() {
      return this.$store.state.currentGroups;
    },
    events() {
      return this.$store.state.events;
    },
    image() {
      return this.course.picture || Placeholder;
    },
    request() {
      return this.$store.state.approvalRequest;
    },
    editable() {
      return this.course.status !== 'open' &&
        (!this.request || Object.keys(this.request).length === 0 || this.request.status === 2);
    },
  },
  created() {
    this.$store.dispatch('fetchCourse', this.id);
    this.$store.dispatch('fetchTasks', this.id);
    this.$store.dispatch('fetchCourseGroups', this.id);
    this.$store.dispatch('fetchCourseEvents', this.id);
    this.$store.dispatch('fetchApprovalRequestByCourse', this.id)
      .catch(() => {});
  },
  methods: {
    updateCourse() {
      const payload = {
        id: this.course.id,
        name: this.courseModified.name,
        description: this.courseModified.description,
        price: this.courseModified.price,
      };

      this.editCourse = false;
      this.$store.dispatch('updateCourse', payload);
    },
    editTask(id) {
      const task = this.tasks.find(el => el.id === id);
      this.$store.commit('setCurrentTask', task);
      this.$store.commit('toggleTaskEdit');
    },
    deleteTask(id) {
      this.$store.dispatch(
        'deleteTask',
        {
          courseId: this.id,
          taskId: id,
        },
      );
    },
    createTask() {
      this.$store.commit('toggleTaskCreate');
    },
    createGroup() {
      this.$store.commit('toggleGroupCreate');
    },
    deleteGroup(id) {
      this.$store.dispatch('deleteGroup', { cId: this.id, gId: id });
    },
    enableEditCourse() {
      this.courseModified = Object.assign({}, this.course);
      this.editCourse = true;
    },
    disableEditCourse() {
      this.editCourse = false;
    },
    toggleThumbnailModal() {
      this.thumbnailEditModal = !this.thumbnailEditModal;
    },
    sendOpenRequest() {
      this.$store.dispatch('sendOpenRequest', this.id);
    },
    resendOpenRequest(rId) {
      this.$store.dispatch('resendOpenRequest', rId);
    },
  },
};
</script>

<style>
#course-edit > div {
  padding: 20px;
}

#course-edit .readonly > *:first-child {
  padding: 0.375rem 0.75rem !important;
  width: 1% !important;
  -ms-flex: 1 1 auto;
  -webkit-box-flex: 1;
  flex: 1 1 auto;
}

#course-edit .readonly:hover > *:first-child {
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  // cursor: pointer;
}

#course-edit .readonly .input-group-append {
  display: none;
}

#course-edit .readonly:hover .input-group-append {
  display: inherit;
}

.border-bottom-only {
  border-width: 0 0 1px 0;
  margin-bottom: 1px;
}

.ProseMirror > *:last-child {
  margin-bottom: 0 !important;
}

#course-card #edit-course {
  display: none !important;
}

#course-card:hover #edit-course {
  display: block !important;
}
</style>
