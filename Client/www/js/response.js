var responseCode = {
	Login_Fail: "登录失败",
  Login_Success: "登录成功",
  Phone_Not_Empty: "请输入手机号",
  Phone_Not_Right: "手机格式不正确",
  Password_Not_Empty: "请输入密码",
  Register_Wrong_Verification_Code: "验证码不正确",
  Verification_Code_Not_Empty: "请输入验证码",
  Logining: "正在登录...",
  Uploading: '正在上传...',
  Registering: "正在注册..",
  Register_Fail: "注册失败",
  Network_Error: "网络连接失败",
  Update_Success: "修改成功",
  Updateing: "更新中...",
  Delete_Success: "删除成功",
  Save_Success: "保存成功",
};

/*var userType = {
  0: "家长",
  1: "已审核老师",
  2: "未审核老师",
  3: "大学生",
  4: "教育机构"
};*/

var userType = ["家长","老师"];

/*var academic = {
  0: "中学",
  1: "本科",
  2: "本科",
  3: "硕士研究生",
  4: "硕士研究生",
  5: "博士研究生",
  6: "博士研究生"
}*/
var academic = [
  "中学",
  "本科",
  "在读本科",
  "硕士研究生",
  "在读硕士研究生",
  "博士研究生",
  "在读博士研究生"
];

var course_type = [
  "老师上门",
  "学生上门",
  "双方协商"
];

var course = [
  {
    key: 1001,
    name: "小学语文"
  },
  {
    key: 1002,
    name: "小学数学"
  },
  {
    key: 1003,
    name: "小学英语"
  }
]