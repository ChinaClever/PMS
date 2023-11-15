/**
 * 繁体中文
 */
export default {
  route: {
    dashboard: {
      _name: 'Dashboard',
      workplace: {_name: '工作臺'},
      analysis: {_name: '分析頁'},
      monitor: {_name: '監控頁'}
    },
    system: {
      _name: '系統管理',
      user: {
        _name: '用戶管理',
        info: {_name: ''}
      },
      role: {_name: '角色管理'},
      menu: {_name: '選單管理'},
      dictionary: {_name: '字典管理'},
      organization: {_name: '機构管理'},
      loginRecord: {_name: '登入日誌'},
      operRecord: {_name: '操作日誌'}
    },
    form: {
      _name: '表單頁面',
      basic: {_name: '基礎表單'},
      advanced: {_name: '複雜表單'},
      step: {_name: '分步表單'}
    },
    list: {
      _name: '清單頁面',
      basic: {_name: '基礎清單'},
      advanced: {_name: '複雜清單'},
      card: {
        _name: '卡片清單',
        project: {_name: '項目清單'},
        application: {_name: '應用清單'},
        article: {_name: '文章清單'}
      }
    },
    result: {
      _name: '結果頁面',
      success: {_name: '成功頁'},
      fail: {_name: '失敗頁'}
    },
    exception: {
      _name: '异常頁面',
      '403': {_name: '403'},
      '404': {_name: '404'},
      '500': {_name: '500'}
    },
    user: {
      _name: '個人中心',
      profile: {_name: '個人資料'},
      message: {_name: '我的消息'}
    },
    extension: {
      _name: '擴展組件',
      icon: {_name: '字體圖標'},
      file: {_name: '檔案清單'},
      printer: {_name: '列印挿件'},
      excel: {_name: 'excel挿件'},
      dragsort: {_name: '拖拽排序'},
      map: {_name: '地圖組件'},
      player: {_name: '視頻播放'},
      editor: {_name: '富文本框'},
      more: {_name: '更多組件'}
    },
    example: {
      _name: '經典實例',
      document: {_name: '案卷調整'},
      choose: {_name: '批量選擇'},
    },
    'https://www.djangoadmin.cn/goods/detail/2': {_name: '獲取授權'}
  },
  layout: {
    home: '主頁',
    header: {
      profile: '個人中心',
      password: '修改密碼',
      logout: '安全登出'
    },
    footer: {
      website: '官網',
      document: '檔案',
      authorization: '授權',
      copyright: 'Copyright © 2021~2023 北京DjangoAdmin研发中心'
    },
    logout: {
      title: '詢問',
      message: '確定要登出嗎?'
    }
  },
  login: {
    title: 'Django+EleVue前后端分离版',
    username: '請輸入登入帳號',
    password: '請輸入登入密碼',
    captcha: '請輸入驗證碼',
    remember: '記住密碼',
    forget: '忘記密碼',
    login: '登入',
    loading: '登入中'
  }
}
