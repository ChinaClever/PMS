/**
 * 国际化配置
 */
import Vue from 'vue';
import VueI18n from 'vue-i18n';
import eleEnLocale from 'ele-admin/packages/lang/en';
import eleZhCNLocale from 'ele-admin/packages/lang/zh-CN';
import eleZhTWLocale from 'ele-admin/packages/lang/zh-TW';
import enLocale from './en';
import zhCNLocale from './zh_CN';
import zhTWLocale from './zh_TW';

Vue.use(VueI18n);

const messages = {
  en: {
    ...eleEnLocale,
    ...enLocale
  },
  zh_CN: {
    ...eleZhCNLocale,
    ...zhCNLocale
  },
  zh_TW: {
    ...eleZhTWLocale,
    ...zhTWLocale
  }
};

const i18n = new VueI18n({
  messages: messages,
  silentTranslationWarn: true,
  // 默认语言
  locale: localStorage.getItem('i18n-lang') || 'zh_CN'
});

export default i18n;
