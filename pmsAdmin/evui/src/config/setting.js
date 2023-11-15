/**
 * 框架全局配置
 */
export default {
  // 不显示侧栏的路由
  hideSidebars: [],
  // 不显示全局页脚的路由
  hideFooters: ['/system/dictionary', '/system/organization', '/form/advanced', '/example/choose'],
  // 页签可重复打开的路由
  repeatableTabs: ['/system/user/info'],
  // 不需要登录的路由
  whiteList: ['/login', '/forget'],
  // 菜单数据接口
  menuUrl: '/index/menu',
  // 自定义解析菜单接口数据
  parseMenu: null,
  // 自定义解析菜单接口单个数据格式
  parseMenuItem: null,
  // 直接指定菜单数据
  menus: null,
  // 用户信息接口
  userUrl: '/index/user',
  // 自定义解析接口用户信息
  parseUser(res) {
    // code为0是成功, 不一样可以处理如: {code: res.code === 200 ? 0 : res.code, msg: res.message}
    let result = {code: res.code, msg: res.msg};
    if (res.data) {
      result.data = Object.assign({}, res.data, {
        // 姓名和头像会显示在顶栏, 字段不一样可以在这处理, 如:
        //avatar: res.data.avatarUrl,
        //nickname: res.data.userName,
        // 角色和权限信息, 需要为string数组类型
        roles: res.data.roles ? res.data.roles.map(d => d.code) : [],
        authorities: res.data.authorities ? res.data.authorities.map(d => d.permission) : []
      });
    }
    return result;
  },
  // token传递的header名称
  tokenHeaderName: 'Authorization',
  // token存储的名称
  tokenStoreName: 'access_token',
  // 用户信息存储的名称
  userStoreName: 'user',
  // 主题配置存储的名称
  themeStoreName: 'theme',
  // 首页tab显示标题, null会根据菜单自动获取
  homeTitle: '主页',
  // 首页路径, null会自动获取
  homePath: null,
  // 顶栏是否显示主题设置按钮
  showSetting: true,
  // 开启多页签是否缓存组件
  tabKeepAlive: true,
  // 是否折叠侧边栏
  collapse: false,
  // 侧边栏风格: light(亮色), dark(暗色)
  sideStyle: 'dark',
  // 顶栏风格: light(亮色), dark(暗色), primary(主色)
  headStyle: 'light',
  // 标签页风格: default(默认), dot(圆点), card(卡片)
  tabStyle: 'default',
  // 布局风格: side(默认), top(顶栏菜单), mix(混合菜单)
  layoutStyle: 'side',
  // 侧边栏菜单风格: default(默认), mix(双排菜单)
  sideMenuStyle: 'default',
  // 是否固定侧栏
  fixedSidebar: true,
  // 是否固定顶栏
  fixedHeader: false,
  // 是否固定主体
  fixedBody: true,
  // logo是否自适应宽度
  logoAutoSize: false,
  // 内容区域宽度是否铺满
  bodyFull: true,
  // 是否开启多标签
  showTabs: true,
  // 侧栏是否多彩图标
  colorfulIcon: false,
  // 侧边栏是否只保持一个子菜单展开
  sideUniqueOpen: true,
  // 是否开启页脚
  showFooter: true,
  // 是否是色弱模式
  weakMode: false,
  // 是否是暗黑模式
  darkMode: false,
  // 默认主题色
  color: null,
  /**
   * 获取缓存的token的方法
   * @returns {string}
   */
  takeToken() {
    let token = localStorage.getItem(this.tokenStoreName);
    if (!token) {
      token = sessionStorage.getItem(this.tokenStoreName);
    }
    return token;
  },
  /**
   * 缓存token的方法
   * @param token
   * @param remember 是否永久存储
   */
  cacheToken(token, remember) {
    localStorage.removeItem(this.tokenStoreName);
    sessionStorage.removeItem(this.tokenStoreName);
    if (token) {
      if (remember) {
        localStorage.setItem(this.tokenStoreName, token);
      } else {
        sessionStorage.setItem(this.tokenStoreName, token);
      }
    }
  },
  /**
   * 获取缓存的用户信息
   * @returns {object}
   */
  takeUser() {
    try {
      return JSON.parse(localStorage.getItem(this.userStoreName)) || {};
    } catch (e) {
      console.error(e);
    }
    return {};
  },
  /**
   * 缓存用户信息
   * @param user
   */
  cacheUser(user) {
    if (user) {
      localStorage.setItem(this.userStoreName, JSON.stringify(user));
    } else {
      localStorage.removeItem(this.userStoreName);
    }
  }
}
