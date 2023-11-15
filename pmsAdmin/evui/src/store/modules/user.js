/**
 * 登录状态管理
 */
import axios from 'axios';
import setting from '@/config/setting';
import {formatMenus} from 'ele-admin';

export default {
  namespaced: true,
  state: {
    // 当前用户信息
    user: setting.takeUser(),
    // 当前用户权限
    authorities: [],
    // 当前用户角色
    roles: [],
    // 当前用户的菜单
    menus: null,
    // 当前登录用户所拥有的权限节点
    permission:[]
  },
  mutations: {
    // 修改值
    SET(state, obj) {
      state[obj.key] = obj.value;
    },
    // 修改token
    SET_TOKEN(state, obj) {
      setting.cacheToken(obj.token, obj.remember);
      state.token = obj.token;
      if (!obj.token) {
        state.user = {};
        state.menus = null;
        setting.cacheUser();
      }
    },
    // 设置权限
    SET_PERMISSION(state,data){
      state.permission = data
    }
  },
  actions: {
    /**
     * 设置节点权限
     * @param {*} commit 
     * @param {*} data 
     */
     setPermission({commit},data){
      commit('SET_PERMISSION',data)
    },
    /**
     * 缓存token
     * @param commit
     * @param token {String, {token: String, remember: String}}
     */
    setToken({commit}, token) {
      let remember = true;
      if (typeof token === 'object') {
        remember = token.remember;
        token = token.token;
      }
      commit('SET_TOKEN', {token: token, remember: remember});
    },
    /**
     * 移除token
     * @param commit
     */
    removeToken({commit}) {
      commit('SET_TOKEN', {});
    },
    /**
     * 设置用户信息
     * @param commit
     * @param user {Object} 用户信息
     */
    setUser({commit}, user) {
      setting.cacheUser(user);
      commit('SET', {key: 'user', value: user});
    },
    /**
     * 设置用户权限
     * @param commit
     * @param authorities {Array<String>} 权限
     */
    setAuthorities({commit}, authorities) {
      commit('SET', {key: 'authorities', value: authorities});
    },
    /**
     * 设置用户角色
     * @param commit
     * @param roles {Array<String>} 角色
     */
    setRoles({commit}, roles) {
      commit('SET', {key: 'roles', value: roles});
    },
    /**
     * 设置用户菜单
     * @param commit
     * @param menus {Array} 菜单
     */
    setMenus({commit}, menus) {
      commit('SET', {key: 'menus', value: menus});
    },
    /**
     * 获取用户菜单路由
     * @param commit
     * @returns {Promise} {Array}
     */
    getMenus({commit}) {
      return new Promise((resolve, reject) => {
        if (!setting.menuUrl) {
          const {menus, homePath} = formatMenus(setting.menus);
          commit('SET', {key: 'menus', value: menus});
          return resolve({menus: menus, home: homePath});
        }
        // 请求接口获取用户菜单
        axios.get(setting.menuUrl).then((res) => {
          const result = typeof setting.parseMenu === 'function' ? setting.parseMenu(res.data) : res.data;
          // 获取用户的信息、角色、权限
          if (result.user) {
            setting.cacheUser(result.user);
            commit('SET', {key: 'user', value: result.user});
            commit('SET', {key: 'roles', value: result.user.roles});
            commit('SET', {key: 'authorities', value: result.user.authorities});
          }
          // 获取用户的菜单
          if (!result.data) {
            console.error('get menus error: ', result);
            return reject(new Error(result.msg));
          }
          // 处理菜单数据格式
          const {menus, homePath} = formatMenus(result.data, setting.parseMenuItem);
          commit('SET', {key: 'menus', value: menus});
          resolve({menus: menus, home: homePath});
        }).catch(e => {
          reject(e);
        });
      });
    }
  }
}
