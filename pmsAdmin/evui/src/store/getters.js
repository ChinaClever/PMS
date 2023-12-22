export default {
  user: state => state.user,
  theme: state => state.theme,
  permission: state => state.user.permission,
  isLeaveTestdata: state=> state.routerchange.isLeaveTestdata,
}
