/**
 * 页签操作封装
 */
import store from '../store';
import router from '../router';

/**
 * 刷新当前页签
 */
export function reloadPageTab() {
  const {path, query, matched} = router.currentRoute;
  const components = new Set();
  matched.forEach((m) => {
    if (m.components && m.components.default && m.components.default.name) {
      if (!['EleEmptyLayout', 'EleLayout'].includes(m.components.default.name)) {
        components.add(m.components.default.name);
      }
    }
  });
  return store.dispatch('theme/setKeepAliveExclude', Array.from(components)).then(() => {
    return router.replace({
      query: query,
      path: '/redirect' + path
    });
  });
}

/**
 * 关闭当前tab
 */
export function finishPageTab() {
  return store.dispatch('theme/tabRemove', router.currentRoute.fullPath).then(({lastPath}) => {
    return router.push(lastPath || '/');
  });
}

/**
 * 移除指定tab
 * @param key {String}
 * @returns {Promise<Object>}
 */
export function removePageTab(key) {
  return store.dispatch('theme/tabRemove', key);
}

/**
 * 移除所有tab
 */
export function removeAllPageTab() {
  return store.dispatch('theme/tabRemoveAll');
}

/**
 * 移除左侧tab
 * @param key {String}
 */
export function removeLeftPageTab(key) {
  return store.dispatch('theme/tabRemoveLeft', key);
}

/**
 * 移除右侧tab
 * @param key {String}
 */
export function removeRightPageTab(key) {
  return store.dispatch('theme/tabRemoveRight', key);
}

/**
 * 移除其他tab
 * @param key {String}
 */
export function removeOtherPageTab(key) {
  return store.dispatch('theme/tabRemoveOther', key);
}

/**
 * 添加tab
 * @param obj
 */
export function addPageTab(obj) {
  return store.dispatch('theme/tabAdd', obj);
}

/**
 * 修改指定tab
 * @param obj
 */
export function setPageTab(obj) {
  return store.dispatch('theme/tabSetTitle', obj);
}
