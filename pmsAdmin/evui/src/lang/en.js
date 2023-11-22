/**
 * 英语
 */
export default {
  route: {
    dashboard: {
      _name: 'Dashboard',
      workplace: {_name: 'Workplace'},
      analysis: {_name: 'Analysis'},
      monitor: {_name: 'Monitor'}
    },
    system: {
      _name: 'System',
      user: {
        _name: 'User',
        info: {_name: ''}
      },
      role: {_name: 'Role'},
      menu: {_name: 'Menu'},
      dictionary: {_name: 'Dictionary'},
      organization: {_name: 'Organization'},
      loginRecord: {_name: 'LoginRecord'},
      operRecord: {_name: 'OperRecord'}
    },
    form: {
      _name: 'Form',
      basic: {_name: 'Basic Form'},
      advanced: {_name: 'Advanced Form'},
      step: {_name: 'Step Form'}
    },
    list: {
      _name: 'List',
      basic: {_name: 'Basic List'},
      advanced: {_name: 'Advanced List'},
      card: {
        _name: 'Card List',
        project: {_name: 'Project'},
        application: {_name: 'Application'},
        article: {_name: 'Article'}
      }
    },
    result: {
      _name: 'Result',
      success: {_name: 'Success'},
      fail: {_name: 'Fail'}
    },
    exception: {
      _name: 'Exception',
      '403': {_name: '403'},
      '404': {_name: '404'},
      '500': {_name: '500'}
    },
    user: {
      _name: 'User',
      profile: {_name: 'Profile'},
      message: {_name: 'Message'}
    },
    extension: {
      _name: 'Extension',
      icon: {_name: 'Icon'},
      file: {_name: 'File'},
      printer: {_name: 'Printer'},
      excel: {_name: 'Excel'},
      dragsort: {_name: 'DragSort'},
      map: {_name: 'Map'},
      player: {_name: 'Player'},
      editor: {_name: 'Editor'},
      more: {_name: 'More'}
    },
    example: {
      _name: 'Example',
      document: {_name: 'Document'},
      choose: {_name: 'Choose'},
    },
    'https://www.djangoadmin.cn/goods/detail/2': {_name: 'Authorization'}
  },
  layout: {
    home: 'Home',
    header: {
      profile: 'Profile',
      password: 'Password',
      logout: 'SignOut'
    },
    footer: {
      website: 'Website',
      document: 'Document',
      authorization: 'Authorization',
      copyright: 'Copyright © 2023 ShenZhen Clever Electronic Co.Ltd'
    },
    logout: {
      title: 'Confirm',
      message: 'Are you sure you want to log out?'
    }
  },
  login: {
    title: 'User Login',
    username: 'please input username',
    password: 'please input password',
    captcha: 'please input code',
    remember: 'remember',
    forget: 'forget',
    login: 'login',
    loading: 'loading'
  }
}
