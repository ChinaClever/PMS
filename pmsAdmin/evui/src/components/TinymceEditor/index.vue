<!-- tinymce富文本编辑器组件 -->
<template>
  <editor
    :init="config"
    :value="value"
    :disabled="disabled"
    @input="updateValue"/>
</template>

<script>
const BASE_URL = process.env.BASE_URL;
import tinymce from 'tinymce/tinymce';
import 'tinymce/icons/default';
import 'tinymce/themes/silver';
import 'tinymce/plugins/code';
import 'tinymce/plugins/print';
import 'tinymce/plugins/preview';
import 'tinymce/plugins/fullscreen';
import 'tinymce/plugins/paste';
import 'tinymce/plugins/searchreplace';
import 'tinymce/plugins/save';
import 'tinymce/plugins/autosave';
import 'tinymce/plugins/link';
import 'tinymce/plugins/autolink';
import 'tinymce/plugins/image';
import 'tinymce/plugins/imagetools';
import 'tinymce/plugins/media';
import 'tinymce/plugins/table';
import 'tinymce/plugins/codesample';
import 'tinymce/plugins/lists';
import 'tinymce/plugins/advlist';
import 'tinymce/plugins/hr';
import 'tinymce/plugins/charmap';
import 'tinymce/plugins/emoticons';
import 'tinymce/plugins/anchor';
import 'tinymce/plugins/directionality';
import 'tinymce/plugins/pagebreak';
import 'tinymce/plugins/quickbars';
import 'tinymce/plugins/nonbreaking';
import 'tinymce/plugins/visualblocks';
import 'tinymce/plugins/visualchars';
import 'tinymce/plugins/wordcount';
import 'tinymce/plugins/emoticons/js/emojis';
import Editor from '@tinymce/tinymce-vue';
// 默认配置
const DEFAULT_CONFIG = {
  height: 300,
  branding: false,
  skin_url: BASE_URL + 'tinymce/skins/ui/oxide',
  content_css: BASE_URL + 'tinymce/skins/content/default/content.min.css',
  language_url: BASE_URL + 'tinymce/langs/zh_CN.js',
  language: 'zh_CN',
  plugins: [
    'code',
    'print',
    'preview',
    'fullscreen',
    'paste',
    'searchreplace',
    'save',
    'autosave',
    'link',
    'autolink',
    'image',
    'imagetools',
    'media',
    'table',
    'codesample',
    'lists',
    'advlist',
    'hr',
    'charmap',
    'emoticons',
    'anchor',
    'directionality',
    'pagebreak',
    'quickbars',
    'nonbreaking',
    'visualblocks',
    'visualchars',
    'wordcount'
  ].join(' '),
  toolbar: [
    'fullscreen',
    'preview',
    'code',
    '|',
    'undo',
    'redo',
    '|',
    'forecolor',
    'backcolor',
    '|',
    'bold',
    'italic',
    'underline',
    'strikethrough',
    '|',
    'alignleft',
    'aligncenter',
    'alignright',
    'alignjustify',
    '|',
    'outdent',
    'indent',
    '|',
    'numlist',
    'bullist',
    '|',
    'formatselect',
    'fontselect',
    'fontsizeselect',
    '|',
    'link',
    'image',
    'media',
    'emoticons',
    'charmap',
    'anchor',
    'pagebreak',
    'codesample',
    '|',
    'ltr',
    'rtl'
  ].join(' '),
  draggable_modal: true,
  toolbar_mode: 'sliding',
  images_upload_handler: (blobInfo, success) => {
    success('data:image/jpeg;base64,' + blobInfo.base64());
  },
  file_picker_types: 'media',
  file_picker_callback: () => {
  }
};
// 暗黑主题
const DARK_CONFIG = {
  skin_url: BASE_URL + 'tinymce/skins/ui/oxide-dark',
  content_css: BASE_URL + 'tinymce/skins/content/dark/content.min.css'
};

export default {
  name: 'TinymceEditor',
  components: {Editor},
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    // 值(v-model)
    value: String,
    // 编辑器配置
    init: Object,
    // 是否禁用
    disabled: Boolean,
    // 自动跟随框架主题
    autoTheme: {
      type: Boolean,
      default: true
    },
    // 是否使用暗黑主题
    darkTheme: Boolean
  },
  data() {
    const dark = this.autoTheme ? this.$store.state.theme.darkMode : this.darkTheme;
    return {
      // 编辑器配置
      config: Object.assign({}, DEFAULT_CONFIG, dark ? DARK_CONFIG : {}, this.init)
    };
  },
  computed: {
    // 是否是暗黑模式
    darkMode() {
      try {
        return this.$store.state.theme.darkMode;
      } catch (e) {
        return false;
      }
    }
  },
  created() {
    tinymce.init({});
  },
  methods: {
    /* 更新value */
    updateValue(value) {
      this.$emit('change', value);
    },
    /* 切换编辑器主题 */
    changeTheme(dark) {
      document.head.querySelectorAll('[id^="mce-"]').forEach((elem) => {
        let href = elem.getAttribute('href');
        if (href.indexOf('/oxide-dark/') !== -1) {
          if (!dark) {
            href = href.replace('/oxide-dark/', '/oxide/');
            elem.setAttribute('href', href);
          }
        } else {
          if (dark) {
            href = href.replace('/oxide/', '/oxide-dark/');
            elem.setAttribute('href', href);
          }
        }
      });
      this.changeContentTheme(dark);
    },
    /* 切换编辑器内容区的主题 */
    changeContentTheme(dark) {
      document.body.querySelectorAll('iframe[id^="tiny-vue_"]').forEach((frame) => {
        const win = frame.contentWindow;
        if (win) {
          const doc = win.document;
          if (doc) {
            [].forEach.call(doc.head.querySelectorAll('[id^="mce-"]'), (elem) => {
              let href = elem.getAttribute('href');
              if (href.indexOf('/skins/ui/') !== -1) {
                if (href.indexOf('/oxide-dark/') !== -1) {
                  if (!dark) {
                    href = href.replace('/oxide-dark/', '/oxide/');
                    elem.setAttribute('href', href);
                  }
                } else {
                  if (dark) {
                    href = href.replace('/oxide/', '/oxide-dark/');
                    elem.setAttribute('href', href);
                  }
                }
              } else if (href.indexOf('/skins/content/') !== -1) {
                if (href.indexOf('/dark/') !== -1) {
                  if (!dark) {
                    href = href.replace('/dark/', '/default/');
                    elem.setAttribute('href', href);
                  }
                } else {
                  if (dark) {
                    href = href.replace('/default/', '/dark/');
                    elem.setAttribute('href', href);
                  }
                }
              }
            });
          }
        }
      });
    }
  },
  watch: {
    darkMode() {
      if (this.autoTheme) {
        this.changeTheme(this.darkMode);
      }
    }
  }
}
</script>

<style>
body .tox-tinymce-aux {
  z-index: 19892000;
}
</style>
