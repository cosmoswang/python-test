# -*- coding: utf-8 -*-

import uiautomation as automation
import time

frame = automation.WindowControl(searchDepth=1, ClassName = 'ApplicationFrameWindow')
frame.SetFocus()
time.sleep(2)
automation.SendKey(automation.Keys.VK_F12)
time.sleep(2)
frame.Minimize()
time.sleep(2)
frame.Maximize()
window1 = frame.WindowControl(searchDepth=1, ClassName = 'Windows.UI.Core.CoreWindow')
# window_custom = window1.WindowControl(searchDepth=1, AutomationId = 'm_f12Docked')
window_customs = window1.GetChildren()
for window_custom in window_customs:
	# print(window_custom)
	pass

window_custom = window1.CustomControl(searchDepth=1, AutomationId = 'm_f12Docked')
# print(window_custom)
children = window_custom.GetChildren()
g = window_custom.GroupControl(searchDepth=1)
f12 = g.PaneControl(searchDepth=1)
f12 = f12.PaneControl(searchDepth=1)
f12 = f12.PaneControl(searchDepth=1, AutomationId='9')
f12 = f12.PaneControl(searchDepth=1, Name='Network')
toolbar = f12.ToolBarControl(searchDepth=1)
button = toolbar.ButtonControl(searchDepth=1, Name='清除会话')
contentFilter = toolbar.ButtonControl(searchDepth=1, Name = '内容类型筛选器')
print(contentFilter)
contentFilter.Click()
time.sleep(2)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_DOWN)
automation.SendKey(automation.Keys.VK_SPACE)
children = toolbar.GetChildren()
for child in children:
	print(child)
# button.Click()
# children = toolbar.GetChildren()
# for child in children:
# 	print(child)
f12 = f12.GroupControl(searchDepth=1, Name = '名称, 协议, 方法, 结果, 内容类型, 已接收, 时间, 发起程序, 开始时间,')
children = f12.GetChildren()

while len(children) < 3:
	print('waiting...')
	time.sleep(1)
	children = f12.GetChildren()

msg_control = children[2]
msg = []
for t in msg_control.GetChildren():
	msg.append(t.Name)

print(msg)
# button.Click()