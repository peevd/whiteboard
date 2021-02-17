import Vue from 'vue';
import Vuex from 'vuex';
import _ from 'lodash';
import router from '@/router';
import config from '@/config.json';


const errHandler = (e) => {
  console.log('axios err:', e);
  if (e.response) {
    console.log('ResErr', e.response);

    if (e.response.status === 401) {
      // bind store to `this`
      this.dispatch('authLogout');
    }
  } else if (e.request) {
    console.log('ReqErr', e.request);
  } else {
    console.log('Error', e.message);
  }
  console.log('Config', e.config);
};

Vue.use(Vuex);

let apiUrl = `${config.hostname}${config.apiPath}`;

if (apiUrl.endsWith('/')) {
  apiUrl = apiUrl.slice(0, -1);
}

export default new Vuex.Store(
  {
    state: {
      icons: {},
      user: null,
      token: localStorage.getItem('ut') || '',
      ownedCourses: [],
      currentCourse: {},
      currentTasks: [],
      currentGroups: [],
      currentTask: {},
      currentTaskAnswered: false,
      currentQuestions: [],
      currentGroup: {},
      currentBoard: {},
      currentBoardSnapshot: null,
      currentBoardData: null,
      currentGroupMembers: [],
      currentAnswers: [],
      showGroupCreate: false,
      showGroupEdit: false,
      showTaskCreate: false,
      showTaskEdit: false,
      courses: [],
      joinedCourses: [],
      students: [],
      breadcrumbs: [],
      events: [],
      approvalRequests: [],
      approvalRequest: {},
      indexCourses: [],
      coursesCount: null,
      requestsCount: {},
      usersCount: {},
      currentPPTs: [],
      currentPPT: {},
    },
    getters: {
      isAuthenticated: state => !!state.token,
      isTeacher: state => state.user && state.user.role_id === 3,
      isStudent: state => state.user && state.user.role_id === 4,
      isMod: state => state.user && state.user.role_id === 2,
      isAdmin: state => state.user && state.user.role_id === 1,
      isUndefined: state => state.user && state.user.role_id === null,
    },
    actions: {
      authLogin({ commit }, data) {
        window.localStorage.setItem('ut', `Bearer ${data.token}`);
        Vue.axios.defaults.headers.Authorization = `Bearer ${data.token}`;
        commit('setToken', `Bearer ${data.token}`);
        router.push(data.redirectUrl);
      },
      authLogout({ commit }) {
        window.localStorage.removeItem('ut');
        commit('setToken', '');
        commit('setUser', null);
        router.push('/login');
      },
      fetchMyCourses({ commit }) {
        Vue.axios.get(`${apiUrl}/api/courses?f=mine`)
          .then(response => commit('addOwnCourses', response.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCourses({ commit }) {
        Vue.axios.get(`${apiUrl}/api/courses?f=all`)
          .then(response => commit('addCourses', response.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCourse({ commit }, id) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/courses/${id}`)
            .then((response) => {
              commit('setCourse', response.data);
              resolve();
            })
            .catch((e) => {
              _.bind(errHandler, self)(e);
              reject();
            });
        });
      },
      newCourse({ commit }, data) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.post(`${apiUrl}/api/courses`, data)
            .then((response) => {
              commit('addCourse', response.data);
              resolve(response.data.id);
            })
            .catch((err) => {
              _.bind(errHandler, self)(err);
              reject();
            });
        });
      },
      postThumbnail({ commit }, data) {
        const self = this;
        Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/images`, data.formData)
          .then(() => {
            Vue.axios.get(`${apiUrl}/api/courses/${data.cId}`)
              .then(response => commit('updateCourse', response.data))
              .catch(_.bind(errHandler, self));
          })
          .catch(_.bind(errHandler, this));
      },
      updateThumbnail({ commit }, data) {
        const self = this;
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/images`, data.formData)
          .then(() => {
            Vue.axios.get(`${apiUrl}/api/courses/${data.cId}`)
              .then((response) => {
                const randStr = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
                const fixedCourse = Object.assign(
                  {}, response.data,
                  {
                    picture: `${response.data.picture}?x=${randStr}`,
                  },
                );
                commit('updateCourse', fixedCourse);
              })
              .catch(_.bind(errHandler, self));
          })
          .catch(_.bind(errHandler, this));
      },
      deleteCourse({ commit }, id) {
        // todo: make request to api
        Vue.axios.delete(`${apiUrl}/api/courses/${id}`)
          .then(() => commit('deleteCourse', id))
          .catch(_.bind(errHandler, this));
      },
      updateCourse({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.id}`, data)
          .then(resp => commit('updateCourse', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchTasks({ commit }, courseId) {
        Vue.axios.get(`${apiUrl}/api/courses/${courseId}/tasks`)
          .then(response => commit('setTasks', response.data))
          .catch(_.bind(errHandler, this));
      },
      updateTask({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.courseId}/tasks/${data.task.id}`, data.task)
          .then(response => commit('updateTask', response.data))
          .catch(_.bind(errHandler, this));
      },
      deleteTask({ commit }, data) {
        Vue.axios.delete(`${apiUrl}/api/courses/${data.courseId}/tasks/${data.taskId}`)
          .then(response => commit('deleteTask', response.data.id))
          .catch(_.bind(errHandler, this));
      },
      createTask({ commit }, data) {
        Vue.axios.post(`${apiUrl}/api/courses/${data.courseId}/tasks`, data.task)
          .then(response => commit('createTask', response.data))
          .catch(_.bind(errHandler, this));
      },
      createGroup({ commit }, data) {
        Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/groups`, data.group)
          .then(resp => commit('addGroup', resp.data))
          .catch(_.bind(errHandler, this));
      },
      updateGroup({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/groups/${data.group.id}`, data.group)
          .then(resp => commit('updateGroup', resp.data))
          .catch(_.bind(errHandler, this));
      },
      deleteGroup({ commit }, data) {
        Vue.axios.delete(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}`)
          .then(resp => commit('deleteGroup', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCourseGroups({ commit }, cId) {
        Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups`)
          .then(resp => commit('setCourseGroups', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchGroup({ commit }, data) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}`)
            .then((resp) => {
              commit('setCurrentGroup', resp.data);
              resolve();
            })
            .catch((e) => {
              _.bind(errHandler, self)(e);
              reject();
            });
        });
      },
      fetchGroupMembers({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/participants`)
          .then(resp => commit('setCurrentGroupMembers', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCurrentTask({ commit }, data) {
        // todo: remove hardcoded task
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/tasks/1`)
          .then(resp => commit('setCurrentTask', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchTask({ commit }, data) {
        const self = this;
        return new Promise((resolve) => {
          Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/tasks`)
            .then((resp) => {
              commit('setCurrentTask', resp.data.find(el => el.id === data.tId));
              const uId = self.state.user.id;
              Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/tasks/${data.tId}/answers/exist?u=${uId}`)
                .then((re) => {
                  commit('setCurrentTaskAnswered', re.data);
                  resolve();
                })
                .catch(_.bind(errHandler, this));
            })
            .catch(_.bind(errHandler, this));
        });
      },
      fetchBoard({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board`)
          .then(resp => commit('setCurrentBoard', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchBoardSnapshot({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board/snapshot`)
          .then(resp => commit('setCurrentBoardSnapshot', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchBoardData({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board/data`)
          .then(resp => commit('setCurrentBoardData', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchUser({ commit }, callback) {
        Vue.axios.get(`${apiUrl}/api/users/me`)
          .then((resp) => {
            commit('setUser', resp.data);
            if (callback) callback();
          })
          .catch(_.bind(errHandler, this));
      },
      updateBoard({ commit }, data) {
        const payload = Object.assign({}, this.state.currentBoard, data.payload);
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board`, payload)
          .then(resp => commit('setCurrentBoard', resp.data))
          .catch(_.bind(errHandler, this));
      },
      saveBoardData({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board/data`, data.payload)
          .then(() => commit('setCurrentBoardData', data.payload.board_data))
          .catch(_.bind(errHandler, this));
      },
      saveBoardSnapshot({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/board/snapshot`, data.payload)
          .then(() => commit('setCurrentBoardSnapshot', data.payload.board_snapshot))
          .catch(_.bind(errHandler, this));
      },
      setUserRole({ commit }, role) {
        const payload = Object.assign({}, this.state.user, { role_id: role });
        Vue.axios.put(`${apiUrl}/api/users/me`, payload)
          .then((resp) => {
            commit('setUser', resp.data);
            router.push('/');
          })
          .catch(_.bind(errHandler, this));
      },
      joinGroup({ commit }, data) {
        Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/participants`, { u_id: data.uId })
          .then((resp) => {
            commit('addParticipant', resp.data);
            router.push(`/joined-courses/${data.cId}`);
          })
          .catch(_.bind(errHandler, this));
      },
      joinCourse({ commit }, data) {  // eslint-disable-line
        return new Promise((resolve, reject) => {
          Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/participants`, { key: data.key })
            .then(() => resolve())
            .catch(() => reject());
        });
      },
      fetchJoinedCourses({ commit }) {
        Vue.axios.get(`${apiUrl}/api/courses?f=coursesIn`)
          .then(response => commit('addJoinedCourses', response.data))
          .catch(_.bind(errHandler, this));
      },
      fetchJoinedCourse({ commit }, cId) {
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/courses/${cId}`)
            .then((response) => {
              commit('setCourse', response.data);

              Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/in`)
                .then((resp) => {
                  commit('setCurrentGroup', resp.data);

                  const gId = resp.data.id;
                  Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/${gId}/board`)
                    .then((r) => {
                      commit('setCurrentBoard', r.data);

                      const tId = r.data.task_id;
                      Vue.axios.get(`${apiUrl}/api/courses/${cId}/tasks`)
                        .then((res) => {
                          commit('setTasks', res.data);
                          commit('setCurrentTask', res.data.find(el => el.id === tId));
                        })
                        .catch(_.bind(errHandler, this));
                    });

                  Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/${gId}/board/snapshot`)
                    .then(r => commit('setCurrentBoardSnapshot', r.data))
                    .catch(_.bind(errHandler, this));

                  resolve();
                })
                .catch(reject);
            })
            .catch(reject);
        });
      },
      fetchStudentBoard({ commit }, cId) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/courses/${cId}`)
            .then((cResp) => {
              commit('setCourse', cResp.data);
              Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/in`)
                .then((resp) => {
                  commit('setCurrentGroup', resp.data);

                  const gId = resp.data.id;
                  Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/${gId}/board`)
                    .then((r) => {
                      commit('setCurrentBoard', r.data);

                      const tId = r.data.task_id;
                      Vue.axios.get(`${apiUrl}/api/courses/${cId}/tasks/${tId}`)
                        .then((res) => {
                          commit('setCurrentTask', res.data);
                          if (self.state.currentTask.id === tId) {
                            const uId = self.state.user.id;
                            Vue.axios.get(`${apiUrl}/api/courses/${cId}/tasks/${tId}/answers/exist?u=${uId}`)
                              .then((re) => {
                                commit('setCurrentTaskAnswered', re.data);
                                resolve();
                              })
                              .catch(_.bind(errHandler, this));
                          }
                        })
                        .catch(() => {
                          _.bind(errHandler, self)();
                          resolve();
                        });
                    });

                  Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups/${gId}/board/data`)
                    .then(r => commit('setCurrentBoardData', r.data))
                    .catch(_.bind(errHandler, self));
                })
                .catch((e) => {
                  _.bind(errHandler, self)(e);
                  reject();
                });
            })
            .catch(e => _.bind(errHandler, self)(e));
        });
      },
      submitAnswer({ commit }, data) {
        Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/tasks/${data.tId}/answers`, data.payload)
          .then(() => commit('setCurrentTaskAnswered', { exists: true }))
          .catch(_.bind(errHandler, this));
      },
      addIcons({ commit }, data) {
        if (typeof data === 'object') {
          commit('addIcon', data);
        }
      },
      fetchStudents({ commit }) {
        Vue.axios.get(`${apiUrl}/api/users?r=student`)
          .then(resp => commit('setStudents', resp.data))
          .catch(_.bind(errHandler, this));
      },
      inviteStudents({ commit }, data) {  // eslint-disable-line
        data.studentsList.forEach((id) => {
          Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/invitations`, { u_id: id })
            .catch(_.bind(errHandler, this));
        });
      },
      kickParticipant({ commit }, data) {
        Vue.axios.delete(`${apiUrl}/api/courses/${data.cId}/groups/${data.gId}/participants/${data.pId}`)
          .then(() => commit('removeParticipant', data.pId))
          .catch(_.bind(errHandler, this));
      },
      fetchStudentAnswers({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/answers?p=${data.pId}`)
          .then(resp => commit('setCurrentAnswers', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchMyStudentAnswers({ commit }, data) {
        return new Promise((resolve) => {
          Vue.axios.get(`${apiUrl}/api/courses/${data.cId}/answers?p=me`)
            .then((resp) => {
              commit('setCurrentAnswers', resp.data);
              resolve();
            })
            .catch(_.bind(errHandler, this));
        });
      },
      gradeStudentAnswer({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/courses/${data.cId}/tasks/${data.tId}/grades?p=${data.pId}`, data.payload)
          .then(resp => commit('updateAnswer', { grade: resp.data.grade, aId: data.aId }))
          .catch(_.bind(errHandler, this));
      },
      setBreadcrumbs({ commit }, data) {
        commit('setBreadcrumbs', data);
      },
      fetchEvents({ commit }) {
        Vue.axios.get(`${apiUrl}/api/events?f=all`)
          .then(resp => commit('setEvents', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCourseEvents({ commit }, cId) {
        Vue.axios.get(`${apiUrl}/api/events?f=byCourse&c_id=${cId}`)
          .then(resp => commit('setEvents', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchGroupEvents({ commit }, data) {
        Vue.axios.get(`${apiUrl}/api/events?f=byCourseGroup&c_id=${data.cId}&g_id=${data.gId}`)
          .then(resp => commit('setEvents', resp.data))
          .catch(_.bind(errHandler, this));
      },
      createEvent({ commit }, data) {
        Vue.axios.post(`${apiUrl}/api/events`, data)
          .then(resp => commit('addEvent', resp.data))
          .catch(_.bind(errHandler, this));
      },
      updateEvent({ commit }, data) {
        Vue.axios.put(`${apiUrl}/api/events/${data.id}`, data)
          .then(resp => commit('updateEvent', resp.data))
          .catch(_.bind(errHandler, this));
      },
      submitPayment({ commit }, data) {  // eslint-disable-line
        return new Promise((resolve, reject) => {
          Vue.axios.post(`${apiUrl}/api/payments`, data)
            .then(() => {
              router.push(`/joined-courses/${data.c_id}`);
              resolve();
            })
            .catch((e) => {
              reject();
              _.bind(errHandler, this)(e);
            });
        });
      },
      sendOpenRequest({ commit }, cId) {
        Vue.axios.post(`${apiUrl}/api/requests`, { c_id: cId, note: '' })
          .then(resp => commit('setApprovalRequest', resp.data))
          .catch(_.bind(errHandler, this));
      },
      resendOpenRequest({ commit }, rId) {
        Vue.axios.put(`${apiUrl}/api/requests/${rId}`)
          .then(resp => commit('setApprovalRequest', resp.data))
          .catch(_.bind(errHandler, this));
      },
      fetchApprovalRequests({ commit }) {
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/requests`)
            .then((resp) => {
              commit('setApprovalRequests', resp.data);
              resolve();
            })
            .catch(() => {
              commit('setApprovalRequests', []);
              reject();
            });
        });
      },
      fetchApprovalRequest({ commit }, id) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/requests/${id}`)
            .then((resp) => {
              commit('setApprovalRequest', resp.data);
              resolve();
            })
            .catch((e) => {
              commit('setApprovalRequest', null);
              _.bind(errHandler, self)(e);
              reject();
            });
        });
      },
      fetchApprovalRequestByCourse({ commit }, cId) {
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/requests?courseID=${cId}`)
            .then((resp) => {
              commit('setApprovalRequest', resp.data);
              resolve();
            })
            .catch(() => {
              commit('setApprovalRequest', null);
              reject();
            });
        });
      },
      fetchApprovalRequestsByFilter({ commit }, filters) {
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/requests?${filters.join('&')}`)
            .then((resp) => {
              commit('setApprovalRequests', resp.data);
              resolve();
            })
            .catch(() => {
              commit('setApprovalRequests', []);
              reject();
            });
        });
      },
      updateApprovalRequest({ commit }, data) {
        const self = this;
        return new Promise((resolve, reject) => {
          Vue.axios.put(`${apiUrl}/api/requests/${data.id}`, data)
            .then((resp) => {
              commit('setApprovalRequest', resp.data);
              resolve();
            })
            .catch((e) => {
              _.bind(errHandler, self)(e);
              reject();
            });
        });
      },
      fetchCourseMod({ commit }, cId) {
        return new Promise((resolve, reject) => {
          Vue.axios.get(`${apiUrl}/api/courses/${cId}`)
            .then((response) => {
              commit('setCourse', response.data);

              const tasksPromise = Vue.axios.get(`${apiUrl}/api/courses/${cId}/tasks`)
                .then(res => commit('setTasks', res.data))
                .catch(_.bind(errHandler, this));

              const groupsPromise = Vue.axios.get(`${apiUrl}/api/courses/${cId}/groups`)
                .then(resp => commit('setCourseGroups', resp.data))
                .catch(_.bind(errHandler, this));

              const eventsPromise = Vue.axios.get(`${apiUrl}/api/events?f=byCourse&c_id=${cId}`)
                .then(resp => commit('setEvents', resp.data))
                .catch(_.bind(errHandler, this));

              Promise.all([tasksPromise, groupsPromise, eventsPromise])
                .then(resolve)
                .catch(reject);
            })
            .catch(reject);
        });
      },
      fetchIndexCourses({ commit }) {
        Vue.axios.get(`${apiUrl}/api/courses/index`)
          .then(r => commit('setIndexCourses', r.data))
          .catch(_.bind(errHandler, this));
      },
      fetchCoursesCount({ commit }) {
        Vue.axios.get(`${apiUrl}/api/courses?f=count`)
          .then(r => commit('setCoursesCount', r.data))
          .catch(_.bind(errHandler, this));
      },
      fetchApprovalRequstsCount({ commit }) {
        Vue.axios.get(`${apiUrl}/api/requests?count=1`)
          .then(r => commit('setRequestsCount', { count: r.data.count, status: 0 }))
          .catch(_.bind(errHandler, this));

        Vue.axios.get(`${apiUrl}/api/requests?status=1&count=1`)
          .then(r => commit('setRequestsCount', { count: r.data.count, status: 1 }))
          .catch(_.bind(errHandler, this));

        Vue.axios.get(`${apiUrl}/api/requests?status=2&count=1`)
          .then(r => commit('setRequestsCount', { count: r.data.count, status: 2 }))
          .catch(_.bind(errHandler, this));

        Vue.axios.get(`${apiUrl}/api/requests?status=3&count=1`)
          .then(r => commit('setRequestsCount', { count: r.data.count, status: 3 }))
          .catch(_.bind(errHandler, this));
      },
      fetchUsersCount({ commit }) {
        Vue.axios.get(`${apiUrl}/api/users?count=1`)
          .then(r => commit('setUsersCount', { count: r.data.count, role: 'all' }))
          .catch(_.bind(errHandler, this));

        Vue.axios.get(`${apiUrl}/api/users?role_id=3&count=1`)
          .then(r => commit('setUsersCount', { count: r.data.count, role: 'teacher' }))
          .catch(_.bind(errHandler, this));

        Vue.axios.get(`${apiUrl}/api/users?role_id=4&count=1`)
          .then(r => commit('setUsersCount', { count: r.data.count, role: 'student' }))
          .catch(_.bind(errHandler, this));
      },
      fetchPresentations({ commit }, cId) {
        commit('setPresentations', []);

        Vue.axios.get(`${apiUrl}/api/courses/${cId}/presentations`)
          .then(r => commit('setPresentations', r.data))
          .catch(_.bind(errHandler, this));
      },
      fetchPresentation({ commit }, url) {
        Vue.axios.get(url)
          .then(r => commit('setPresentation', r.data))
          .catch(_.bind(errHandler, this));
      },
      uploadPPT({ commmit }, data) { // eslint-disable-line
        Vue.axios.post(`${apiUrl}/api/courses/${data.cId}/presentations`, data.formData)
          .then(() => this.dispatch('fetchPresentations', data.cId))
          .catch(_.bind(errHandler, this));
      },
      deletePPT({ commit }, data) {
        commit('deletePPT', data);
      },
      selectPPT({ commit }, data) {
        commit('togglePPT', data);
      },
    },
    mutations: {
      setToken(state, token) {
        state.token = token;
      },
      setCourse(state, course) {
        state.currentCourse = course;
      },
      addCourses(state, courses) {
        state.courses = courses;
      },
      addOwnCourses(state, courses) {
        state.ownedCourses = courses;
      },
      addCourse(state, course) {
        state.ownedCourses.unshift(course);
      },
      deleteCourse(state, id) {
        state.ownedCourses = state.ownedCourses.filter(c => c.id !== id);
      },
      updateCourse(state, data) {
        if (state.ownedCourses.find(el => el.id === data.id)) {
          state.ownedCourses = state.ownedCourses.filter(el => el.id !== data.id);
          state.ownedCourses.unshift(data);
        }

        if (state.courses.find(el => el.id === data.id)) {
          state.courses = state.courses.filter(el => el.id !== data.id);
          state.courses.unshift(data);
        }

        if (state.joinedCourses.find(el => el.id === data.id)) {
          state.joinedCourses = state.joinedCourses.filter(el => el.id !== data.id);
          state.joinedCourses.unshift(data);
        }

        if (state.currentCourse.id === data.id) {
          state.currentCourse = data;
        }
      },
      setCurrentTask(state, task) {
        state.currentTask = task;
      },
      toggleTaskCreate(state) {
        state.showTaskCreate = !state.showTaskCreate;
      },
      toggleTaskEdit(state) {
        state.showTaskEdit = !state.showTaskEdit;
      },
      toggleGroupCreate(state) {
        state.showGroupCreate = !state.showGroupCreate;
      },
      toggleGroupEdit(state) {
        state.showGroupEdit = !state.showGroupEdit;
      },
      updateTask(state, data) {
        state.currentTasks = state.currentTasks.filter(el => el.id !== data.id);
        state.currentTasks.unshift(data);
      },
      deleteTask(state, id) {
        state.currentTasks = state.currentTasks.filter(el => el.id !== id);
      },
      createTask(state, data) {
        state.currentTasks.unshift(data);
      },
      setTasks(state, data) {
        state.currentTasks = data;
      },
      addGroup(state, data) {
        state.currentGroups.unshift(data);
      },
      updateGroup(state, data) {
        state.currentGroups = state.currentGroups.filter(el => el.id !== data.id);
        state.currentGroups.unshift(data);

        if (state.currentGroup && state.currentGroup.id === data.id) {
          state.currentGroup = data;
        }
      },
      deleteGroup(state, group) {
        state.currentGroups = state.currentGroups.filter(el => el.id !== group.id);
      },
      setCourseGroups(state, groups) {
        state.currentGroups = groups;
      },
      setCurrentGroup(state, group) {
        state.currentGroup = group;
      },
      setCurrentGroupMembers(state, members) {
        state.currentGroupMembers = members;
      },
      setCurrentBoard(state, board) {
        state.currentBoard = board;
      },
      setUser(state, user) {
        state.user = user;
      },
      addParticipant(state, user) {
        console.log(user);
      },
      removeParticipant(state, id) {
        state.currentGroupMembers = state.currentGroupMembers.filter(el => el.id !== id);
        state.currentGroup.members_in -= 1;
      },
      addJoinedCourses(state, data) {
        state.joinedCourses = data;
      },
      setCurrentBoardSnapshot(state, data) {
        state.currentBoardSnapshot = data;
      },
      setCurrentBoardData(state, data) {
        state.currentBoardData = data;
      },
      addQuestion(state, data) {
        state.currentQuestions.push(data);
      },
      setCurrentQuestions(state, data) {
        state.currentQuestions = data;
      },
      setCurrentTaskAnswered(state, data) {
        state.currentTaskAnswered = data.exists;
      },
      addIcon(state, icon) {
        state.icons = Object.assign({}, state.icons, icon);
      },
      setStudents(state, students) {
        state.students = students;
      },
      setCurrentAnswers(state, answers) {
        state.currentAnswers = answers;
      },
      updateAnswer(state, data) {
        state.currentAnswers = state.currentAnswers.map((el) => {
          if (el.id === data.aId) {
            return Object.assign({}, el, { grade: data.grade });
          }

          return el;
        });
      },
      setBreadcrumbs(state, data) {
        state.breadcrumbs = data;
      },
      setEvents(state, data) {
        state.events = data;
      },
      addEvent(state, data) {
        state.events.unshift(data);
      },
      updateEvent(state, data) {
        state.events = state.events.filter(el => el.id !== data.id);
        state.events.unshift(data);
      },
      setApprovalRequests(state, data) {
        state.approvalRequests = data;
      },
      setApprovalRequest(state, data) {
        state.approvalRequest = data;
      },
      setIndexCourses(state, data) {
        state.indexCourses = data;
      },
      setCoursesCount(state, data) {
        state.coursesCount = data.count;
      },
      setRequestsCount(state, data) {
        state.requestsCount = Object.assign(
          {},
          state.requestsCount,
          {
            [data.status]: data.count,
          },
        );
      },
      setUsersCount(state, data) {
        state.usersCount = Object.assign(
          {},
          state.usersCount,
          {
            [data.role]: data.count,
          },
        );
      },
      togglePPT(state, data) {
        if (state.currentPPT.name === data.name) {
          state.currentPPT = {};
        } else {
          state.currentPPT = {
            name: data.name,
            url: `${config.hostname}${config.apiPath}/static/presentations/course_${data.cId}/${data.name}`,
          };
        }
      },
      deletePPT(state, data) {
        state.currentPPTs = state.currentPPTs.filter(e => e.name !== data.name);
      },
      setPresentations(state, data) {
        state.currentPPTs = data;
      },
    },
  },
);

