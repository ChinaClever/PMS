<!-- 顶栏消息图标 -->
<template>
  <el-popover
    :width="330"
    trigger="click"
    v-model="visible"
    class="ele-notice-group"
    transition="el-zoom-in-top"
    popper-class="ele-notice-pop">
    <div slot="reference" class="ele-notice-group">
      <el-badge :value="allNum" :hidden="!allNum">
        <i class="el-icon-bell"></i>
      </el-badge>
    </div>
    <el-tabs v-model="active">
      <el-tab-pane name="notice" :label="noticeLabel">
        <div class="ele-notice-list ele-scrollbar-mini">
          <div v-for="(item, index) in notice" :key="index" class="ele-notice-item">
            <div class="ele-cell ele-notice-item-wrapper">
              <i :class="[item.icon, 'ele-notice-item-icon']"></i>
              <div class="ele-cell-content">
                <div class="ele-elip">{{ item.title }}</div>
                <div class="ele-text-secondary ele-elip">{{ item.time }}</div>
              </div>
            </div>
            <el-divider/>
          </div>
        </div>
        <div v-if="notice.length" class="ele-cell ele-notice-actions">
          <div class="ele-cell-content" @click="clear('notice')">清空通知</div>
          <el-divider direction="vertical" class="line-color-light"/>
          <div class="ele-cell-content" @click="more('notice')">查看更多</div>
        </div>
        <ele-empty v-if="!notice.length" text="已查看所有通知"/>
      </el-tab-pane>
      <el-tab-pane name="message" :label="messageLabel">
        <div class="ele-notice-list ele-scrollbar-mini">
          <div v-for="(item, index) in message" :key="index" class="ele-notice-item">
            <div class="ele-cell ele-notice-item-wrapper ele-cell-align-top">
              <el-avatar :src="item.avatar" size="medium"/>
              <div class="ele-cell-content">
                <div class="ele-elip">{{ item.title }}</div>
                <div class="ele-text-secondary ele-elip">{{ item.content }}</div>
                <div class="ele-cell-desc ele-elip">{{ item.time }}</div>
              </div>
            </div>
            <el-divider/>
          </div>
        </div>
        <div v-if="message.length" class="ele-cell ele-notice-actions">
          <div class="ele-cell-content" @click="clear('message')">清空消息</div>
          <el-divider direction="vertical" class="line-color-light"/>
          <div class="ele-cell-content" @click="more('message')">查看更多</div>
        </div>
        <ele-empty v-if="!message.length" text="已读完所有私信"/>
      </el-tab-pane>
      <el-tab-pane :label="todoLabel" name="todo">
        <div class="ele-notice-list ele-scrollbar-mini">
          <div v-for="(item, index) in todo" :key="index" class="ele-notice-item">
            <div class="ele-notice-item-wrapper">
              <div class="ele-cell ele-cell-align-top">
                <div class="ele-cell-content ele-elip">{{ item.title }}</div>
                <el-tag size="mini" :type="['info','danger',''][item.state]">
                  {{ ['未开始', '即将到期', '进行中'][item.state] }}
                </el-tag>
              </div>
              <div class="ele-text-secondary ele-elip">{{ item.desc }}</div>
            </div>
            <el-divider/>
          </div>
        </div>
        <div v-if="todo.length" class="ele-cell ele-notice-actions">
          <div class="ele-cell-content" @click="clear('todo')">清空待办</div>
          <el-divider direction="vertical" class="line-color-light"/>
          <div class="ele-cell-content" @click="more('todo')">查看更多</div>
        </div>
        <ele-empty v-if="!todo.length" text="已完成所有任务"/>
      </el-tab-pane>
    </el-tabs>
  </el-popover>
</template>

<script>
export default {
  name: 'EleNotice',
  data() {
    return {
      visible: false,
      active: 'notice',
      notice: [
        {
          icon: 'el-icon-s-comment',
          title: '你收到了一封2份新周报',
          time: '2020-07-27 18:30:18'
        },
        {
          icon: 'el-icon-s-check',
          title: '一米阳光同意了你的请假申请',
          time: '2020-07-27 09:08:36'
        },
        {
          icon: 'el-icon-video-camera',
          title: '孤城凉梦邀请你参加视频会议',
          time: '2020-07-26 18:30:01'
        },
        {
          icon: 'el-icon-s-claim',
          title: '你推荐的孤城凉梦已通过第三轮面试',
          time: '2020-07-25 16:38:46'
        },
        {
          icon: 'el-icon-message-solid',
          title: '你的8月加班奖金已发放',
          time: '2020-07-25 11:03:31'
        }
      ],
      message: [
        {
          avatar: require('@/assets/logo.png'),
          title: '落叶不随风 评论了你的日志',
          content: '写的不错, 以后多多向你学习~',
          time: '2020-07-27 18:30:18'
        },
        {
          avatar: require('@/assets/logo.png'),
          title: '雨晨的清风 点赞了你的日志',
          content: '写的不错, 以后多多向你学习~',
          time: '2020-07-27 09:08:36'
        },
        {
          avatar: require('@/assets/logo.png'),
          title: '孤城凉梦 评论了你的周报',
          content: '写的不错, 以后多多向你学习~',
          time: '2020-07-26 18:30:01'
        },
        {
          avatar: require('@/assets/logo.png'),
          title: '淡墨无殇 点赞了你的周报',
          content: '写的不错, 以后多多向你学习~',
          time: '2020-07-25 11:03:31'
        }
      ],
      todo: [
        {
          state: 0,
          title: '半岛弥音的请假审批',
          desc: '半岛弥音在 07-27 18:30 提交的请假申请'
        },
        {
          state: 1,
          title: '第三方代码紧急变更',
          desc: '需要在 2020-07-27 之前完成'
        },
        {
          state: 2,
          title: '信息安全考试',
          desc: '需要在 2020-07-26 18:30 前完成'
        },
        {
          state: 2,
          title: 'DjangoAdmin发布新版本',
          desc: '需要在 2020-07-25 11:03 前完成'
        }
      ]
    };
  },
  computed: {
    // 通知标题
    noticeLabel() {
      return this.notice.length ? `通知(${this.notice.length})` : '通知';
    },
    // 私信标题
    messageLabel() {
      return this.message.length ? `私信(${this.message.length})` : '私信';
    },
    // 待办标题
    todoLabel() {
      return this.todo.length ? `待办(${this.todo.length})` : '待办';
    },
    // 所有消息数量
    allNum() {
      return this.notice.length + this.message.length + this.todo.length;
    }
  },
  methods: {
    /* 清空消息 */
    clear(type) {
      if (type === 'notice') {
        this.notice = [];
      } else if (type === 'message') {
        this.message = [];
      } else if (type === 'todo') {
        this.todo = [];
      }
    },
    /* 查看更多 */
    more(type) {
      this.visible = false;
      if (this.$route.path !== '/user/message' || this.$route.query.type !== type) {
        this.$router.push({
          path: '/user/message',
          query: {
            type: type
          }
        });
      }
    }
  }
}
</script>

<style lang="scss">
.ele-notice-group {
  display: block;

  .el-badge {
    line-height: 1;
    display: block;
  }
}

/* 消息通知pop */
.ele-notice-pop {
  padding: 0 !important;

  /* tab */
  .el-tabs__nav-scroll {
    text-align: center;
  }

  .el-tabs__nav {
    float: none;
    display: inline-block;
  }

  .el-tabs__item {
    height: 44px;
    line-height: 44px;
    padding: 0 20px !important;
  }

  /* 空视图 */
  .ele-empty {
    padding: 100px 0;
  }
}

/* 列表 */
.ele-notice-list {
  padding-top: 8px;
  max-height: 360px;
  overflow: auto;
}

.ele-notice-item {
  .ele-notice-item-wrapper {
    padding: 12px 15px;
    transition: background-color .2s;
    cursor: pointer;

    &:hover {
      background-color: hsla(0, 0%, 60%, .05);
    }
  }

  .ele-text-secondary {
    margin-top: 5px;
    font-size: 13px;
  }

  .ele-cell-desc {
    margin-top: 3px !important;
    font-size: 12px !important;
  }
}

.ele-notice-item-icon {
  width: 32px;
  height: 32px;
  line-height: 32px !important;
  color: #FFF;
  font-size: 16px;
  background-color: #60B2FC;
  border-radius: 50%;
  text-align: center;


  &.el-icon-s-check {
    background-color: #F5686F;
  }

  &.el-icon-video-camera {
    background-color: #7CD734;
  }

  &.el-icon-s-claim {
    background-color: #FAAD14;
  }

  &.el-icon-message-solid {
    background-color: #2BCACD;
  }
}

/* 操作按钮 */
.ele-notice-actions > .ele-cell-content {
  line-height: 42px;
  text-align: center;
  cursor: pointer;

  &:hover {
    background-color: hsla(0, 0%, 60%, .05);
  }
}
</style>
