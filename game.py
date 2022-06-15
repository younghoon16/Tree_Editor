from TreeSprite import *
from PyQt5.QtWidgets import QFileDialog

class Game:
    def __init__(self, window, display=False):
        pg.init()
        # 窗口属性
        self.size = (1000, 618)
        self.window = window
        self.bg_color = (255, 242, 204)
        self.display = display
        self.icon = pg.image.load('image/node-tree.png')
        pg.display.set_icon(self.icon)
        self.title = "Tree Editor"
        self.cursors = []
        self.screen = pg.display.set_mode(self.size, pg.RESIZABLE)
        pg.display.set_caption(self.title)

        # 整颗树中点位置的纵坐标
        self.mid_ver = self.size[1] // 2

        # 控制变量
        self.playing = True
        self.speed = 1
        self.fps = 200
        self.clock = pg.time.Clock()

        # 初始化一个树结点
        self.Root = TreeSprite(self, self.size[0]//2, self.size[1]//2, display=self.display)
        self.TreeGroup = TreeGroup()
        self.TreeGroup.add(self.Root)

    def run(self):
        while self.playing:
            self.clock.tick(self.fps)
            self.draw()
            self.update()

    def update(self):
        events = pg.event.get()
        self.TreeGroup.update(events)
        if pg.SYSTEM_CURSOR_IBEAM in self.cursors:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_IBEAM)
        elif pg.SYSTEM_CURSOR_HAND in self.cursors:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.cursors.clear()
        # 持续按键列表，检查上下左右按键
        keys_list = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # 按下Esc键退出
                    self.playing = False
                elif event.key == pg.K_SPACE:
                    # 按下空格键可以将树重置到中心位置
                    self.reset_to_center()
                elif event.key == pg.K_KP_MINUS:
                    self.minify()
                elif event.key == pg.K_KP_PLUS:
                    self.amplify()
                elif event.key == pg.K_f:
                    self.TreeGroup.all_fold()
                elif event.key == pg.K_p:
                    pg.image.save(self.screen, QFileDialog.getSaveFileName(
                        self.window,
                        "保存截图",
                        "未命名.png",
                        "png(*.png)"
                    )[0])
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.minify()
                elif event.button == 4:
                    self.amplify()
            if event.type == pg.VIDEORESIZE:
                self.size = event.size
                self.reset_to_center()

        for tree in self.TreeGroup.contents:
            # 对上下左右按键可以同时处理
            self.mid_ver += int(keys_list[pg.K_UP] - keys_list[pg.K_DOWN]) * self.speed
            tree.center = (tree.center[0] +
                           int(keys_list[pg.K_LEFT] - keys_list[pg.K_RIGHT]) * tree.radius // 6 * self.speed,
                           tree.center[1] +
                           int(keys_list[pg.K_UP] - keys_list[pg.K_DOWN]) * self.speed)
        if keys_list[pg.K_UP] or keys_list[pg.K_DOWN]:
            self.Root.adjustTree(True)
        pg.display.update()

    def draw(self):
        # 绘制图像
        self.screen.fill(self.bg_color)
        self.TreeGroup.draw()

    def reset_to_center(self):
        self.mid_ver = self.size[1] // 2
        self.Root.center = (self.size[0] // 2,
                            self.Root.root.center[1])
        self.Root.adjustTree(True)
        if len(self.TreeGroup.recent_collision) > 0:
            self.TreeGroup.recent_collision[-1].adjustTree(False)
        else:
            self.Root.adjustTree(False)

    def amplify(self):
        for tree in self.TreeGroup.contents:
            if tree.radius < 60:
                tree.radius += 3
        self.Root.adjustTree(True)
        if len(self.TreeGroup.recent_collision) > 0:
            self.TreeGroup.recent_collision[-1].adjustTree(False)
        else:
            self.Root.adjustTree(False)

    def minify(self):
        for tree in self.TreeGroup.contents:
            if tree.radius > 15:
                tree.radius -= 3
        self.Root.adjustTree(True)
        if len(self.TreeGroup.recent_collision) > 0:
            self.TreeGroup.recent_collision[-1].adjustTree(False)
        else:
            self.Root.adjustTree(False)

    def tree_display(self, ls: list):
        if ls[0] != -1:
            self.Root.val = ls[0]
            self.Root.assign(ls, 0)
