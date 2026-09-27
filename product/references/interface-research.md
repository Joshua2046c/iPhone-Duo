# 接口资料检索记录

检索日期：2026-09-27。当前仅完成产品定义所需研究，未选定或采购零件。

## iPhone Duo
用户上传的两幅图为外形尺寸与显示屏规格证据；原始照片保持不变。
Apple 技术规格：https://www.apple.com.cn/iphone-duo/specs/ 。
Apple 配件设计入口：https://developer.apple.com/accessories/ 。
公开尺寸图列表：https://developer.apple.com/accessories/dimensional-drawings/ 。本次读取的列表有 iPhone 18 Pro 等型号，未找到 iPhone Duo 条目；不是断言不存在其他渠道的尺寸图。
未取得：音量键与机身基准间坐标、按键间距及行程、相机凸台轮廓、铰链运动包络、接口避让尺寸。不得从渲染图估计后宣称实配。

## 初代 Joy-Con
任天堂官方安装说明：https://www.nintendo.com/en-gb/Support/Troubleshooting/How-to-Attach-Detach-the-Joy-Con-Controllers-from-the-Nintendo-Switch-Console-1379043.html 。原生滑入方向自上而下，不是朝手机中心水平推入。
官方外形规格：https://www.nintendo.com/my/hardware/switch/modal/specs/joy-con.html 。102 × 35.9 × 28.4 mm 包含突出部件，不能用于反推轨道截面。
参数化 CAD 目录查询 Nintendo Switch Joy-Con rail，返回通用 V-slot/C-beam 零件；这些是不同标准，不适用，未选择任何替代品。
step.parts 查询 Nintendo Switch Joy-Con rail 和 Joycon 均返回 0 个匹配，未下载或生成替代轨道。
原作者社区模型线索：https://cults3d.com/en/3d-model/gadget/nintendo-switch-joy-con-controller-mount-rail 。搜索结果列出 STEP 文件；尚未下载、检查许可、尺寸和左右锁止接口，不能视为已验证制造模型，也不等于所拟采用的金属轨道。

## 机构可行性边界
两个独立正面柱塞、转向摇臂和导向推杆为设计提案，尚未计算行程、传动比、摩擦、回位力及空间干涉。固定后壳范围、设备方向和手柄插入方向后才能确定传力路径。若采用只固定单半片机身的方案，手柄载荷应经过背壳承力梁闭合，避免将另一半屏幕及铰链当作承力梁。

## 当前状态
用户于本轮明确上向下插入、仅后盖半片且不得影响开合；新增第一张图只用于朝向，后三张红框用于滑轨形式。产品方向问题已关闭。
已建立五个对象的参数化结构模型：主壳、左右自定义滑轨、两路独立柔性音量转向键；输出准备为一体打印原型。没有原机或手柄验证实体。已检查静态几何、俯视及滑轨侧视，并测量底板 2.4 mm、轨道内腔 4.6 mm、总宽 173.2 mm。均仅证实自定义模型与其参数相符，不证明外部设备兼容。
未解决的接口尺寸维持原记录，不再重复询问已确认的产品方向。
