# P2E_blender_visn
一个基于官方代码改编的增强型的P2E脚本

## 起因
1. 由于官方 Parent to Empty 的功能比较单一，在需要做多层摄像机或场景文件整理的时候，需要多种不同的组合需求
2. 由于和C4D不同的逻辑，blender创建的父子级会保留原本对象的空间坐标，有一层转换。工程实际使用的时候可能用不上这层转换，于是把全部的父子级关联都改成了C4D默认的：移动到父级之后，PSR=0

## 实现的功能
1. **空物体父级（Parent To Empty）**：原代码只支持将所有物体移动到一个最顶层的空物体之下。改进之后的代码允许在多层父子级中间创建，不会把东西都拎出来到最外面。和C4D的“alt+G”同等效果。![](./Preview/1%20P2EfuncPV.mp4.gif)

2. **快速父级（Fast Parent）、清除父级（Clear Parent）**：快速创建父级或重新指定父级，快速清除父级并保留当前位置信息![](./Preview/2%20FP_CPfuncPV.mp4.gif)

3. **选择所有子级（Select Children）、选择父级（Select Parent）**![](./Preview/3%20SC_SP_funcPV.mp4.gif)

3. **释放子级到世界（Release to World）、释放子级到上一层（Release to Sub-parent）**![](./Preview/4%20RW_RSP_funcPV.mp4.gif)

4. **拎出（Pickup Solo）、拎出到父级（Pickup to New Parent）**：不同层级之间的物体，单独拎出来，或放进一个新的父级![](./Preview/5%20PS_PNPfuncPV.mp4.gif)

5. **快速摄像机（Fast Camera）**：以所选物体为中心，创建目标摄像机，带有一层保护。![](./Preview/6%20FCfuncPV.mp4.gif)
