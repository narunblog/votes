import Vue from "vue";
import VueRouter from "vue-router";

//index
import IndexView from "@/components/IndexView.vue"

// accouts
import Login from "@/components/accounts/Login";
import Logout from "@/components/accounts/Logout";
import PasswordChange from "@/components/accounts/PasswordChange";
import PasswordChangeDone from "@/components/accounts/PasswordChangeDone";
import PasswordReset from "@/components/accounts/PasswordReset";
import PasswordResetConfirm from "@/components/accounts/PasswordResetConfirm";
import PasswordResetDone from "@/components/accounts/PasswordResetDone";
import SignUp from '@/components/accounts/SignUp';
import SignUpDone from '@/components/accounts/SignUpDone';
import UserActivation from '@/components/accounts/UserActivation';

//votes
import VoteSelect from "@/components/votes/VoteSelect";
import VoteHistory from "@/components/votes/VoteHistory";
import VoteResult from "@/components/votes/VoteResult";
import VoteStart from "@/components/votes/VoteStart";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "indexView",
    component: IndexView,
    children: [
      {
        path: "vote-select",
        name: "voteSelect",
        component: VoteSelect,
      },
      {
        path: "vote-history",
        name: "voteHistory",
        component: VoteHistory,
      },
      {
        path: "vote-result",
        name: "voteResult",
        component: VoteResult,
      },
      {
        path: "vote-start",
        name: "voteStart",
        component: VoteStart,
      },
    ],
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/logout",
    name: "logout",
    component: Logout,
  },
  {
    path: "/password/change",
    name: "passwordChange",
    component: PasswordChange,
  },
  {
    path: "/password/change/done",
    name: "passwordChangeDone",
    component: PasswordChangeDone,
  },
  {
    path: "/password/reset",
    name: "passwordReset",
    component: PasswordReset,
  },
  {
    path: "/password/reset/confirm/:uid/:token",
    name: "passwordResetConfirm",
    component: PasswordResetConfirm,
  },
  {
    path: "/password/reset/done",
    name: "passwordResetDone",
    component: PasswordResetDone,
  },
  {
    path: "/signup",
    name: "signUp",
    component: SignUp,
  },
  {
    path: "/signup/done",
    name: "signUpDone",
    component: SignUpDone,
  },
  {
    path: "/activate/:uid/:token",
    name: "userActivation",
    component: UserActivation,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
