import Vue from 'vue';
import Router from 'vue-router';

import store from '@/store';

import AdminDash from '@/components/AdminDash';
import ApprovalRequest from '@/components/ApprovalRequest';
import ApprovalRequests from '@/components/ApprovalRequests';
import Board from '@/components/Board';
import CoursePage from '@/components/CoursePage';
import EditCourse from '@/components/EditCourse';
import EditGroup from '@/components/EditGroup';
import Home from '@/components/Home';
import JoinedCourse from '@/components/JoinedCourse';
import JoinedCourseBoard from '@/components/JoinedCourseBoard';
import JoinedCourses from '@/components/JoinedCourses';
import Login from '@/components/Login';
import MyCourses from '@/components/MyCourses';
import RandomBoard from '@/components/RandomBoard';
import RoleSelect from '@/components/RoleSelect';

Vue.use(Router);

const requiresAuth = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    if (store.getters.isUndefined) {
      next('/first-login');
      return;
    }

    next();
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const requiresNoAuth = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const requiresRoleStudent = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    if (store.getters.isStudent) {
      next();
      return;
    }

    next('/');
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const requiresRoleTeacher = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    if (store.getters.isTeacher) {
      next();
      return;
    }

    next('/');
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const requiresRoleModAdmin = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    if (store.getters.isMod || store.getters.isAdmin) {
      next();
      return;
    }

    next('/');
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const requiresRoleUndefined = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    if (store.getters.isUndefined) {
      next();
      return;
    }

    next('/');
    return;
  }

  console.log(to);
  const toPath = encodeURIComponent(to.fullPath);
  next(`/login?redirect=${toPath}`);
};

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      beforeEnter: requiresAuth,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: requiresNoAuth,
    },
    {
      path: '/my-courses',
      name: 'My Courses',
      component: MyCourses,
      beforeEnter: requiresRoleTeacher,
    },
    {
      path: '/my-courses/:cId',
      name: 'Edit Course',
      component: EditCourse,
      beforeEnter: requiresRoleTeacher,
    },
    {
      path: '/my-courses/:cId/groups/:gId',
      name: 'Edit Group',
      component: EditGroup,
      beforeEnter: requiresRoleTeacher,
    },
    {
      path: '/my-courses/:cId/groups/:gId/board',
      name: 'Group Board',
      component: Board,
      beforeEnter: requiresRoleTeacher,
    },
    {
      path: '/first-login',
      name: 'Role Selectt',
      component: RoleSelect,
      beforeEnter: requiresRoleUndefined,
    },
    {
      path: '/courses/:cId',
      name: 'Course Page',
      component: CoursePage,
      beforeEnter: requiresRoleStudent,
    },
    {
      path: '/joined-courses',
      name: 'Joined Courses',
      component: JoinedCourses,
      beforeEnter: requiresRoleStudent,
    },
    {
      path: '/joined-courses/:cId',
      name: 'Joined Course',
      component: JoinedCourse,
      beforeEnter: requiresRoleStudent,
    },
    {
      path: '/joined-courses/:cId/board',
      name: 'Course Board',
      component: JoinedCourseBoard,
      beforeEnter: requiresRoleStudent,
    },
    {
      path: '/boards/:boardId',
      name: 'Random Board',
      component: RandomBoard,
      beforeEnter: requiresAuth,
    },
    {
      path: '/admin',
      name: 'AdminDash',
      component: AdminDash,
      beforeEnter: requiresRoleModAdmin,
    },
    {
      path: '/admin/requests',
      name: 'ApprovalRequests',
      component: ApprovalRequests,
      beforeEnter: requiresRoleModAdmin,
    },
    {
      path: '/admin/requests/:id',
      name: 'ApprovalRequest',
      component: ApprovalRequest,
      beforeEnter: requiresRoleModAdmin,
    },
  ],
});

router.beforeEach((to, from, next) => {
  store.dispatch('setBreadcrumbs', []);
  if (store.getters.isAuthenticated && store.state.user === null) {
    store.dispatch('fetchUser', next);
  } else {
    next();
  }
});

export default router;

