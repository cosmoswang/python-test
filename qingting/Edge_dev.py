# -*- coding: utf-8 -*-

import uiautomation as automation
import time

class Edge_dev:

	def prepare(self):
		time.sleep(3)
		automation.SendKey(automation.Keys.VK_F12)
		time.sleep(3)
		win = automation.WindowControl(searchDepth=1, ClassName = 'ApplicationFrameWindow')
		control = win.WindowControl(searchDepth=1, ClassName = 'Windows.UI.Core.CoreWindow', searchWaitTime=100)
		# print(control)
		control = control.CustomControl(searchDepth=1, AutomationId = 'm_f12Docked')
		control = control.GroupControl(searchDepth=1)
		f12 = control.PaneControl(searchDepth=1)
		f12 = f12.PaneControl(searchDepth=1)
		f12 = f12.PaneControl(searchDepth=1, AutomationId='9')
		f12 = f12.PaneControl(searchDepth=1, Name='Network')
		toolbar = f12.ToolBarControl(searchDepth=1)
		self.button = toolbar.ButtonControl(searchDepth=1, Name='清除会话')
		self.button.Invoke()
		# button.Click()
		# contentFilter = toolbar.ButtonControl(searchDepth=1, Name = '内容类型筛选器')
		automation.SendKey(automation.Keys.VK_TAB)
		automation.SendKey(automation.Keys.VK_SPACE)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_DOWN)
		automation.SendKey(automation.Keys.VK_SPACE)
		automation.SendKey(automation.Keys.VK_ESCAPE)

		self.groupControl = f12.GroupControl(searchDepth=1, Name = '名称, 协议, 方法, 结果, 内容类型, 已接收, 时间, 发起程序, 开始时间,')

	def getUrl(self):
		children = self.groupControl.GetChildren()

		while len(children) < 3:
			time.sleep(3)
			children = self.groupControl.GetChildren()

		msg_control = children[len(children) - 1]
		msg = []
		for t in msg_control.GetChildren():
			msg.append(t.Name)
		
		time.sleep(2)
		self.button.Invoke()
		return msg[1] + msg[0]