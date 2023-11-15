<template>
  <div class="ele-body ele-body-card">
    <!-- 顶部卡片 -->
    <el-card shadow="never" body-style="padding: 20px;">
      <div class="ele-cell workplace-user-card">
        <div class="ele-cell-content ele-cell">
          <el-avatar :size="68" :src="loginUser.avatar"/>
          <div class="ele-cell-content">
            <h4 class="ele-elip">早安，{{ loginUser.nickname }}，开始您一天的工作吧！</h4>
            <div class="ele-text-secondary ele-elip" style="margin-top: 8px;">
              <i class="el-icon-heavy-rain"></i>
              <span><s/><s/>今日阴转小雨，22℃ - 32℃，出门记得带伞哦。</span>
            </div>
          </div>
        </div>
        <div class="workplace-count-group">
          <div class="workplace-count-item">
            <div class="workplace-count-header">
              <el-tag size="small" class="ele-tag-round">
                <i class="el-icon-menu"></i>
              </el-tag>
              <span class="workplace-count-name">项目数</span>
            </div>
            <div class="workplace-count-num">3</div>
          </div>
          <div class="workplace-count-item">
            <div class="workplace-count-header">
              <el-tag type="warning" size="small" class="ele-tag-round">
                <i class="el-icon-finished"></i>
              </el-tag>
              <span class="workplace-count-name">待办项</span>
            </div>
            <div class="workplace-count-num">6 / 24</div>
          </div>
          <div class="workplace-count-item">
            <div class="workplace-count-header">
              <el-tag type="success" size="small" class="ele-tag-round">
                <i class="el-icon-bell"></i>
              </el-tag>
              <span class="workplace-count-name">消息</span>
            </div>
            <div class="workplace-count-num">1,689</div>
          </div>
        </div>
      </div>
    </el-card>
    <!-- 快捷方式 -->
    <el-row :gutter="15">
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/system/user" class="app-link-block">
            <i class="app-link-icon el-icon-user"></i>
            <div class="app-link-title">系统用户</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/system/role" class="app-link-block">
            <i class="app-link-icon el-icon-data-line" style="color: #95de64;"></i>
            <div class="app-link-title">角色管理</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/system/menu" class="app-link-block">
            <i class="app-link-icon el-icon-shopping-cart-2" style="color: #ff9c6e;"></i>
            <div class="app-link-title">菜单管理</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/system/dict" class="app-link-block">
            <i class="app-link-icon el-icon-tickets" style="color: #b37feb;"></i>
            <div class="app-link-title">字典管理</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/data/config" class="app-link-block">
            <i class="app-link-icon el-icon-bank-card" style="color: #ffd666;"></i>
            <div class="app-link-title">配置管理</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/message/notice" class="app-link-block">
            <i class="app-link-icon el-icon-message" style="color: #5cdbd3;"></i>
            <div class="app-link-title">通知公告</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/tool/generate" class="app-link-block">
            <i class="app-link-icon el-icon-discount" style="color: #ff85c0;"></i>
            <div class="app-link-title">代码生成器</div>
          </router-link>
        </el-card>
      </el-col>
      <el-col :lg="3" :md="6" :sm="6" :xs="12">
        <el-card shadow="hover" body-style="padding: 0;">
          <router-link to="/user/profile" class="app-link-block">
            <i class="app-link-icon el-icon-s-operation" style="color: #ffc069;"></i>
            <div class="app-link-title">个人中心</div>
          </router-link>
        </el-card>
      </el-col>
    </el-row>
    <!-- 最新动态、我的任务、本月目标 -->
    <el-row :gutter="15">
      <el-col :lg="8" :md="12">
        <el-card
          shadow="never"
          header="版本信息"
          body-style="padding: 0;">
          <el-scrollbar
            style="height: 318px;"
            wrapStyle="overflow-x: hidden;"
            viewStyle="padding: 20px 10px;">
            <el-timeline
              :reverse="false"
              class="ele-timeline ele-timeline-act">
              <el-timeline-item
                v-for="(act, index) in activities"
                :key="index"
                :timestamp="act.timestamp"
                :type="act.primary ? 'primary' : ''">
                {{ act.title }}
              </el-timeline-item>
            </el-timeline>
          </el-scrollbar>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="12">
        <el-card
          shadow="never"
          header="升级计划"
          body-style="padding: 0;"
          class="workplace-table-card">
          <el-table-draggable handle=".sort-handle" :animate="300">
            <el-table :data="taskList" :height="318" class="ele-table-default-head">
              <el-table-column width="38" align="center">
                <i class="sort-handle el-icon-_nav ele-text-placeholder"></i>
              </el-table-column>
              <el-table-column label="优先级" width="65">
                <template slot-scope="{row}">
                  <el-tag
                    size="mini"
                    class="ele-tag-round"
                    :type="['danger','warning','primary'][row.priority-1]">
                    {{ row.priority }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="任务名称">
                <template slot-scope="{row}">
                  <el-link
                    type="primary"
                    :underline="false">
                    {{ row.taskName }}
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column label="状态" width="70" align="center">
                <template slot-scope="{row}">
                  <span
                    :class="['ele-text-warning','ele-text-success','ele-text-info'][row.state]">
                      {{ ['未开始', '进行中', '已完成'][row.state] }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </el-table-draggable>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="12" class="hidden-md-and-down">
        <el-card shadow="never" header="本月目标">
          <div class="workplace-goal-group">
            <el-progress
              :width="170"
              :percentage="80"
              type="dashboard"
              :format="()=>{return ''}"/>
            <div class="workplace-goal-content">
              <el-tag
                size="large"
                class="ele-tag-round">
                <i class="el-icon-s-data"></i>
              </el-tag>
              <div class="workplace-goal-num">365</div>
            </div>
            <div class="workplace-goal-text">恭喜，本月目标已达标！</div>
          </div>
        </el-card>
      </el-col>
      <el-col :lg="16" :md="24">
        <el-card
          shadow="never"
          header="项目进度"
          body-style="padding: 12px;"
          class="workplace-table-card">
          <el-table :data="projectList" height="358">
            <el-table-column
              type="index"
              width="35"
              min-width="35"
              align="right"/>
            <el-table-column
              label="项目名称"
              min-width="110">
              <template slot-scope="{row}">
                <el-link
                  type="primary"
                  :underline="false">
                  {{ row.projectName }}
                </el-link>
              </template>
            </el-table-column>
            <el-table-column
              label="开始时间"
              prop="startDate"
              width="95"
              min-width="80"
              align="center"/>
            <el-table-column
              prop="endDate"
              label="结束时间"
              width="95"
              min-width="80"
              align="center"/>
            <el-table-column
              label="状态"
              width="70"
              min-width="60"
              align="center">
              <template slot-scope="{row}">
                <span
                  :class="['ele-text-success','ele-text-danger','ele-text-warning','ele-text-info ele-text-delete'][row.state]">
                    {{ ['进行中', '已延期', '未开始', '已结束'][row.state] }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="进度"
              width="160"
              min-width="100"
              align="center">
              <template slot-scope="{row}">
                <el-progress :percentage="row.progress" class="ele-text-small"/>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="12">
        <el-card
          shadow="never"
          header="小组成员"
          body-style="padding: 19px 0;">
          <div
            v-for="(item, index) in userList"
            :key="index"
            class="ele-cell user-list-item">
            <el-avatar :size="42" :src="item.avatar"/>
            <div class="ele-cell-content">
              <div class="ele-cell-title">{{ item.name }}</div>
              <div class="ele-cell-desc">{{ item.desc }}</div>
            </div>
            <el-tag
              size="mini"
              :type="['success','danger'][item.state]">
              {{ ['在线', '离线'][item.state] }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="12" class="hidden-lg-and-up">
        <el-card
          shadow="never"
          header="本月目标"
          body-style="padding: 46px 0;">
          <div class="workplace-goal-group">
            <el-progress
              :width="170"
              :percentage="80"
              type="dashboard"
              :format="()=>{return ''}"/>
            <div class="workplace-goal-content">
              <el-tag
                size="large"
                class="ele-tag-round">
                <i class="el-icon-s-data"></i>
              </el-tag>
              <div class="workplace-goal-num">365</div>
            </div>
            <div class="workplace-goal-text">恭喜，本月目标已达标！</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'DashboardWorkplace',
  data() {
    return {
      // 最新动态数据
      activities: [
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '20:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '19:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '18:30',
          primary: true
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '17:30',
          primary: true
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '16:30',
          primary: true
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '15:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '14:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '12:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '11:30',
          primary: true
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '10:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '09:30',
          primary: false
        },
        {
          title: '基于Python语言Django+EleVue前后端分离版',
          timestamp: '08:30',
          primary: false
        }
      ],
      // 我的任务数据
      taskList: [
        {
          id: 1,
          priority: 1,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 0
        },
        {
          id: 2,
          priority: 2,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 0
        },
        {
          id: 3,
          priority: 2,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 1
        },
        {
          id: 4,
          priority: 3,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 1
        },
        {
          id: 5,
          priority: 3,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 2
        },
        {
          id: 6,
          priority: 3,
          taskName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 2
        }
      ],
      // 项目进度数据
      projectList: [
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 0,
          startDate: '2020-03-01',
          endDate: '2020-06-01',
          progress: 30
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 0,
          startDate: '2020-03-01',
          endDate: '2020-08-01',
          progress: 10
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 1,
          startDate: '2020-01-01',
          endDate: '2020-05-01',
          progress: 60
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 1,
          startDate: '2020-06-01',
          endDate: '2020-10-01',
          progress: 0
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 2, startDate: '2020-01-01',
          endDate: '2020-03-01',
          progress: 100
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 3,
          startDate: '2020-01-01',
          endDate: '2020-03-01',
          progress: 100
        },
        {
          projectName: 'DjangoAdmin敏捷开发框架Django+EleVue版本',
          state: 3,
          startDate: '2020-01-01',
          endDate: '2020-03-01',
          progress: 100
        }
      ],
      // 小组成员数据
      userList: [
        {
          name: '一米阳光',
          desc: '系统架构师、高级研发工程师',
          state: 0,
          avatar: require('@/assets/logo.png')
        },
        {
          name: '一米阳光',
          desc: 'WEB前端工程师',
          state: 0,
          avatar: require('@/assets/logo.png')
        },
        {
          name: '一米阳光',
          desc: 'GO后端工程师',
          state: 0,
          avatar: require('@/assets/logo.png')
        },
        {
          name: '一米阳光',
          desc: '产品经理、视觉设计师',
          state: 1,
          avatar: require('@/assets/logo.png')
        },
        {
          name: '一米阳光',
          desc: '测试工程师、运维工程师',
          state: 1,
          avatar: require('@/assets/logo.png')
        }
      ]
    };
  },
  computed: {
    // 当前登录用户信息
    loginUser() {
      return this.$store.state.user.user;
    }
  }
}
</script>

<style scoped>
/* 顶部用户信息卡片 */
.workplace-user-card .ele-cell-content {
  overflow: hidden;
}

.workplace-count-group {
  white-space: nowrap;
}

.workplace-count-item {
  padding: 0 5px 0 25px;
  box-sizing: border-box;
  display: inline-block;
  text-align: right;
}

.workplace-count-name {
  padding-left: 8px;
}

.workplace-count-num {
  font-size: 24px;
  margin-top: 6px;
}

@media screen and (max-width: 992px) {
  .workplace-count-item {
    padding: 0 5px 0 10px;
  }
}

@media screen and (max-width: 768px) {
  .workplace-user-card,
  .workplace-count-group {
    display: block;
  }

  .workplace-count-group {
    margin-top: 15px;
    text-align: right;
  }

  .workplace-user-card ::v-deep .el-avatar {
    width: 45px !important;
    height: 45px !important;
  }

  .workplace-user-card h4 {
    font-size: 16px;
  }

  .workplace-user-card h4 + .ele-text-secondary {
    font-size: 12px;
  }

  .workplace-user-card {
    margin: -10px;
  }
}

/* 快捷方式 */
.app-link-block {
  display: block;
  color: inherit;
  padding: 15px 0;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
}

.app-link-block .app-link-icon {
  color: #69c0ff;
  font-size: 30px;
  margin-top: 5px;
}

.app-link-block .app-link-title {
  margin-top: 8px;
}

/* 最新动态时间轴 */
.ele-timeline-act {
  padding-left: 50px;
}

.ele-timeline-act ::v-deep .el-timeline-item__timestamp {
  margin: 0;
  position: absolute;
  top: 3px;
  left: -45px;
}

.ele-timeline-act ::v-deep .el-timeline-item {
  padding-bottom: 19px;
}

.ele-timeline-act ::v-deep .el-timeline-item:last-child {
  padding-bottom: 0;
}

/* 表格 */
.workplace-table-card ::v-deep .el-table tbody > .el-table__row:last-child td {
  border-bottom: none;
}

.workplace-table-card ::v-deep .el-table:before {
  display: none;
}

.workplace-table-card .sort-handle {
  cursor: move;
  font-size: 18px;
  vertical-align: middle;
}

.workplace-table-card ::v-deep .el-table__row.sortable-chosen {
  background-color: hsla(0, 0%, 60%, .1);
}

.workplace-table-card ::v-deep .el-table__row.sortable-chosen td {
  background-color: transparent;
}

/* 本月目标 */
.workplace-goal-group {
  text-align: center;
  position: relative;
  padding: 48px 0;
}

.workplace-goal-group .workplace-goal-content {
  position: absolute;
  top: 90px;
  left: 0;
  width: 100%;
}

.workplace-goal-group .workplace-goal-num {
  font-size: 40px;
  margin-top: 15px;
}

/* 小组成员 */
.user-list-item {
  padding: 13px 18px;
}

.user-list-item + .user-list-item {
  border-top: 1px solid hsla(0, 0%, 60%, .15);
}

.user-list-item .ele-cell-desc {
  margin-top: 5px;
}

/* 小屏幕优化 */
@media screen and (max-width: 768px) {

}
</style>
