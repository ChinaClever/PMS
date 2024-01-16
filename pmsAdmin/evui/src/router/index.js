/**
 * 路由配置
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';
import setting from '@/config/setting';
import EleLayout from '@/layout';
import {menuToRoutes} from 'ele-admin';
import NProgress from 'nprogress';

Vue.use(VueRouter);

// 静态路由
const routes = [
  {
    path: '/login',
    component: () => import('@/views/login/login'),
    meta: {title: '登录'}
  },
  {
    path: '/supplier/batchadd',
    component: () => import('@/views/supplier/supplier/supplier-batch-add'),
    meta: {title: '物料绑定'}
  },
  {
    path: '/packing/batchadd',
    component: () => import('@/views/packing/packing/packing-batch-add'),
    meta: {title: '打包记录绑定'}
  },
  {
    path: '/burning/batchadd',
    component: () => import('@/views/burning/burningreport/burning-add'),
    meta: {title: '烧录绑定'}
  },
  // {
  //   path: '/forget',
  //   component: () => import('@/views/login/forget'),
  //   meta: {title: '忘记密码'}
  // },
  {
    path: '*',
    component: () => import('@/views/exception/404')
  }
];

const router = new VueRouter({
  routes,
  mode: 'history'
});

// 路由守卫
router.beforeEach((to, from, next) => {
  NProgress.start();
  updateTitle(to);
  if(from.path === '/inspect/testdata'){
    store.state.routerchange.isLeaveTestdata = true;
  }
  if(to.path === '/inspect/testdata'){
    store.state.routerchange.isLeaveTestdata = false;
  }
  // 判断是否登录
  if (setting.takeToken()) {
    // 判断是否已经注册动态路由
    if (!store.state.user.menus) {
      // 获取动态路由
      store.dispatch('user/getMenus').then(({menus, home}) => {
        // menuToRoutes方法是把菜单数据转成路由数据格式
        router.addRoute({
          path: '/',
          component: EleLayout,
          redirect: setting.homePath || home,
          children: menuToRoutes(menus, (component) => import('@/views' + component))
        });
        next({...to, replace: true});
      }).catch(() => {
        next();
      });
    } else {
      next();
    }
  } else if (setting.whiteList.includes(to.path)) {
    next();
  } else {
    next({path: '/login', query: to.path === '/' ? {} : {from: to.path}});
  }
});

router.afterEach(() => {
  setTimeout(() => {
    NProgress.done(true);
  }, 300);
});

export default router;

/**
 * 更新浏览器标题
 * @param route 路由
 */
function updateTitle(route) {
  if (!route.path.startsWith('/redirect/')) {
    let names = [];
    if (route && route.meta && route.meta.title) {
      names.push(route.meta.title);
    }
    const appName = process.env.VUE_APP_NAME;
    if (appName) {
      names.push(appName);
    }
    document.title = names.join(' - ');
  }
}
