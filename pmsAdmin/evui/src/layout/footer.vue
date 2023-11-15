<!-- 页脚 -->
<template>
  <div class="ele-text-center" style="padding: 16px 0;">
    <div>
      <a
        target="_blank"
        class="ele-text-secondary"
        href="https://www.djangoadmin.cn">
        {{ $t('layout.footer.website') }}
      </a>
      <em/>
      <a
        target="_blank"
        class="ele-text-secondary"
        href="http://docs.django.elevue.djangoadmin.cn">
        {{ $t('layout.footer.document') }}
      </a>
      <em/>
      <a
        target="_blank"
        class="ele-text-secondary"
        href="https://www.djangoadmin.cn/goods/detail/2">
        {{ $t('layout.footer.authorization') }}
      </a>
    </div>
    <div class="ele-text-secondary" style="margin-top: 8px;">
      {{ $t('layout.footer.copyright') }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'EleFooter'
}
</script>
