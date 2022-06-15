import pygame as pg
import pygame_textinput
import pygame.gfxdraw


class TreeSprite:
    def __init__(self, game, sr: int, sc: int, display):
        pg.init()
        self.game = game
        # 是否仅展示
        self.display = display

        # 初始化字体，如果字体对象为None，打包后运行会出现错误
        self.textinput_font = None
        self.font = None

        # 表示树结点圆的圆心坐标
        self.center = (sr, sc)

        # 初始化结点内包含的元素
        self.text = None
        self.text_rect = None
        self.textinput = None
        self.textinput_rect = None
        self.add_image = pg.image.load('image/add-line.png')
        self.add = None
        self.add_rect = None
        self.arrow_up_left = pg.image.load('image/arrow-up-left.png')
        self.arrow_up_right = pg.image.load('image/arrow-up-right.png')
        self.arrow_down_left = pg.image.load('image/arrow-down-left.png')
        self.arrow_down_right = pg.image.load('image/arrow-down-right.png')
        self.arrow_image_left = self.arrow_down_left
        self.arrow_image_right = self.arrow_down_right
        self.arrow_left = self.arrow_image_left
        self.arrow_right = self.arrow_image_right
        self.arrow_left_rect = self.arrow_image_left.get_rect()
        self.arrow_right_rect = self.arrow_image_right.get_rect()
        self.edit_image = pg.image.load('image/edit.png')
        self.edit = self.edit_image
        self.edit_rect = self.edit_image.get_rect()
        self.delete_image = pg.image.load('image/delete.png')
        self.delete = self.delete_image
        self.delete_rect = self.delete.get_rect()

        # 与树结点相关的一些属性
        self.radius = 30
        self.Line_Color = (0, 0, 0)
        self.level = 1
        self.MaxLevel = 1
        self.root = self
        self.val = None
        self.left = None
        self.father = None
        self.right = None

    def draw(self):
        # 绘制图形
        # 绘制一个抗锯齿的空心圆
        pg.gfxdraw.aacircle(self.game.screen, self.center[0], self.center[1], self.radius, self.Line_Color)
        if self.val is not None:
            if self.left is not None:
                center_dist = (abs(self.center[0] - self.left.center[0]), abs(self.center[1] - self.left.center[1]))
                center_len = (center_dist[0] ** 2 + center_dist[1] ** 2) ** 0.5
                x_len = self.radius * center_dist[0] // center_len
                y_len = self.radius * center_dist[1] // center_len
                pg.draw.line(self.game.screen, self.Line_Color, (self.center[0] - x_len, self.center[1] + y_len),
                             (self.left.center[0] + x_len, self.left.center[1] - y_len), width=2)
            if self.right is not None:
                center_dist = (abs(self.center[0] - self.right.center[0]), abs(self.center[1] - self.right.center[1]))
                center_len = (center_dist[0] ** 2 + center_dist[1] ** 2) ** 0.5
                x_len = self.radius * center_dist[0] // center_len
                y_len = self.radius * center_dist[1] // center_len
                pg.draw.line(self.game.screen, self.Line_Color, (self.center[0] + x_len, self.center[1] + y_len),
                             (self.right.center[0] - x_len, self.right.center[1] - y_len), width=2)
            if self.textinput is not None:
                self.game.cursors.append(pg.SYSTEM_CURSOR_IBEAM)
                self.textinput_rect.center = self.center
                self.game.screen.blit(self.textinput.surface, self.textinput_rect)
            else:
                x, y = pg.mouse.get_pos()
                if not self.display and (self.center[0] - x) ** 2 + (self.center[1] - y) ** 2 <= self.radius ** 2:
                    self.game.cursors.append(pg.SYSTEM_CURSOR_HAND)
                    self.arrow_left = pg.transform.scale(self.arrow_image_left,
                                                         (24 * self.radius // 30, 24 * self.radius // 30))
                    self.arrow_left_rect = self.arrow_left.get_rect()
                    self.arrow_left_rect.center = (self.center[0] - self.radius * 7 // 15,
                                                   self.center[1] + self.radius * 7 // 15)
                    self.arrow_right = pg.transform.scale(self.arrow_image_right,
                                                          (24 * self.radius // 30, 24 * self.radius // 30))
                    self.arrow_right_rect = self.arrow_right.get_rect()
                    self.arrow_right_rect.center = (self.center[0] + self.radius * 7 // 15,
                                                    self.center[1] + self.radius * 7 // 15)
                    self.edit = pg.transform.scale(self.edit_image, (24 * self.radius // 30, 24 * self.radius // 30))
                    self.edit_rect = self.edit.get_rect()
                    self.edit_rect.center = (self.center[0] - self.radius * 7 // 15,
                                             self.center[1] - self.radius // 3)
                    self.delete = pg.transform.scale(self.delete_image,
                                                     (24 * self.radius // 30, 24 * self.radius // 30))
                    self.delete_rect = self.delete.get_rect()
                    self.delete_rect.center = (self.center[0] + self.radius * 7 // 15,
                                               self.center[1] - self.radius // 3)
                    self.game.screen.blit(self.arrow_right, self.arrow_right_rect)
                    self.game.screen.blit(self.arrow_left, self.arrow_left_rect)
                    self.game.screen.blit(self.delete, self.delete_rect)
                    self.game.screen.blit(self.edit, self.edit_rect)
                else:
                    self.font = pg.font.SysFont('MSYH.ttf', self.radius)
                    self.text = self.font.render(self.val, True, 'black')
                    self.text_rect = self.text.get_rect()
                    self.text_rect.center = self.center
                    self.game.screen.blit(self.text, self.text_rect)
        else:
            x, y = pg.mouse.get_pos()
            if self.textinput is not None:
                self.game.cursors.append(pg.SYSTEM_CURSOR_IBEAM)
                self.textinput_rect.center = self.center
                self.game.screen.blit(self.textinput.surface, self.textinput_rect)
            else:
                if (self.center[0] - x) ** 2 + (self.center[1] - y) ** 2 <= self.radius ** 2:
                    self.game.cursors.append(pg.SYSTEM_CURSOR_HAND)
                self.add = pg.transform.scale(self.add_image, (24 * self.radius // 30, 24 * self.radius // 30))
                self.add_rect = self.add.get_rect()
                self.add_rect.center = self.center
                self.game.screen.blit(self.add, self.add_rect)

    def adjustTree(self, mode: bool):
        # 调整树的结构，mode: True-垂直方向调整， False-水平方向调整
        if mode:
            tree_level = self.root.getMaxLevel()
            self.dfs(self.root, tree_level=tree_level)
        else:
            self.dfs(self.root, pause_level=self.level)

    def dfs(self, treenode, tree_level=None, pause_level=None):
        # 深度优先遍历树的所有结点，同时改变当前结点与其子节点之间的位置关系
        if pause_level is None:
            treenode.MaxLevel = tree_level
            treenode.center = (treenode.center[0],
                               treenode.game.mid_ver + 2 * treenode.radius * (2 * treenode.level - tree_level - 1))
            if treenode.left is not None:
                self.dfs(treenode.left, tree_level=tree_level)
            if treenode.right is not None:
                self.dfs(treenode.right, tree_level=tree_level)
        elif tree_level is None:
            if treenode.left is not None:
                if treenode.left.level < pause_level:
                    treenode.left.center = (
                        treenode.center[0] - 4 * treenode.radius * 2**(pause_level - treenode.left.level),
                        treenode.left.center[1])
                else:
                    treenode.left.center = (treenode.center[0] - 4 * treenode.radius,
                                            treenode.left.center[1])
                self.dfs(treenode.left, pause_level=pause_level)
            if treenode.right is not None:
                if treenode.right.level < pause_level:
                    treenode.right.center = (
                        treenode.center[0] + 4 * treenode.radius * 2**(pause_level - treenode.right.level),
                        treenode.right.center[1])
                else:
                    treenode.right.center = (treenode.center[0] + 4 * treenode.radius,
                                             treenode.right.center[1])
                self.dfs(treenode.right, pause_level=pause_level)

    def getMaxLevel(self) -> int:
        # 得到以treenode为根的树的层数
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.getMaxLevel()
        if self.right is not None:
            right = self.right.getMaxLevel()
        return max(left, right) + 1

    def remove(self):
        # 递归移除当前结点和其子树
        self.val = None
        if self.left is not None:
            self.left.remove()
            self.game.TreeGroup.pop(self.left)
            self.left = None
            self.arrow_image_left = self.arrow_down_left
        if self.right is not None:
            self.right.remove()
            self.game.TreeGroup.pop(self.right)
            self.right = None
            self.arrow_image_right = self.arrow_down_right

    def insert(self, direction: bool, val=None):
        # 插入结点，direction：True-left, False-right
        if direction:
            self.left = TreeSprite(self.game, self.center[0] - 4 * self.radius,
                                   self.center[1] + 4 * self.radius, display=self.display)
            self.left.root = self.root
            self.left.val = val
            self.left.radius = self.radius
            self.game.TreeGroup.add(self.left)
            self.left.level = self.level + 1
            if self.left.level > self.MaxLevel:
                self.adjustTree(True)
            if self.game.TreeGroup.collision(self.left):
                self.left.adjustTree(False)
        else:
            self.right = TreeSprite(self.game, self.center[0] + 4 * self.radius,
                                    self.center[1] + 4 * self.radius, display=self.display)
            self.right.root = self.root
            self.right.val = val
            self.right.radius = self.radius
            self.game.TreeGroup.add(self.right)
            self.right.level = self.level + 1
            if self.right.level > self.MaxLevel:
                self.adjustTree(True)
            if self.game.TreeGroup.collision(self.right):
                self.right.adjustTree(False)

    def update(self, events):
        # 接收键盘点击和鼠标事件
        if self.textinput is not None:
            self.textinput.update(events)
        for event in events:
            if self.textinput is not None and event.type == pg.KEYDOWN \
                    and event.key == pg.K_RETURN:
                self.val = self.textinput.value
                self.textinput = None
                self.textinput_rect = None
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.val is None and \
                        (self.center[0] - pos[0]) ** 2 + (self.center[1] - pos[1]) ** 2 <= self.radius ** 2:
                    # 按下plus添加结点
                    self.textinput_font = pg.font.SysFont('MSYH', self.radius)
                    if self.val is None:
                        self.textinput = pygame_textinput.TextInputVisualizer(
                            font_object=self.textinput_font,
                            cursor_width=2
                        )
                        self.textinput_rect = self.textinput.surface.get_rect()

                elif self.val is not None and self.textinput is None:
                    if self.arrow_left_rect.left <= pos[0] <= self.arrow_left_rect.right \
                            and self.arrow_left_rect.top <= pos[1] <= self.arrow_left_rect.bottom:
                        # 按下朝左 向下/向上展开箭头
                        if self.arrow_image_left == self.arrow_down_left:
                            self.arrow_image_left = self.arrow_up_left
                            if self.left is None:
                                self.insert(True)
                        elif self.left.val is None:
                            self.arrow_image_left = self.arrow_down_left
                            self.game.TreeGroup.pop(self.left)
                            self.left = None
                            self.adjustTree(True)

                    elif self.arrow_right_rect.left <= pos[0] <= self.arrow_right_rect.right \
                            and self.arrow_right_rect.top <= pos[1] <= self.arrow_right_rect.bottom:
                        # 按下朝右向下/向上展开箭头
                        if self.arrow_image_right == self.arrow_down_right:
                            self.arrow_image_right = self.arrow_up_right
                            if self.right is None:
                                self.insert(False)
                        elif self.right.val is None:
                            self.arrow_image_right = self.arrow_down_right
                            self.game.TreeGroup.pop(self.right)
                            self.right = None
                            self.adjustTree(True)

                    elif self.delete_rect.left <= pos[0] <= self.delete_rect.right \
                            and self.delete_rect.top <= pos[1] <= self.delete_rect.bottom:
                        # 按下删除键，级联删除
                        self.remove()
                        self.adjustTree(True)

                    elif self.edit_rect.left <= pos[0] <= self.edit_rect.right \
                            and self.edit_rect.top <= pos[1] <= self.edit_rect.bottom:
                        # 重新编辑结点值
                        self.textinput_font = pg.font.SysFont('MSYH', self.radius)
                        self.textinput = pygame_textinput.TextInputVisualizer(
                            font_object=self.textinput_font,
                            cursor_width=2
                        )
                        self.textinput_rect = self.textinput.surface.get_rect()

    def assign(self, ls: list, p: int):
        if 2 * p + 1 < len(ls) and ls[2 * p + 1] != "NA":
            self.insert(True, val=str(ls[2 * p + 1]))
            self.left.assign(ls, 2 * p + 1)
        if 2 * p + 2 < len(ls) and ls[2 * p + 2] != "NA":
            self.insert(False, val=str(ls[2 * p + 2]))
            self.right.assign(ls, 2 * p + 2)



class TreeGroup:
    def __init__(self):
        # 存储树结点的容器：初始化为一个空的列表
        self.contents = []

        # 存储最近发生碰撞的结点，为了能够正确地缩放
        self.recent_collision = []

    def add(self, tree):
        # 添加结点
        self.contents.append(tree)

    def update(self, events):
        # 更新组内的所有结点
        for tree in self.contents:
            tree.update(events)

    def draw(self):
        for tree in self.contents:
            tree.draw()

    def pop(self, tree):
        self.contents.remove(tree)
        if tree in self.recent_collision:
            # 如果该结点也在最近发生碰撞的结点中，那么也需要从此列表中删除该结点
            self.recent_collision.remove(tree)

    def collision(self, tree) -> bool:
        # 碰撞检测
        for t in self.contents:
            if t != tree and t.level == tree.level and abs(t.center[0] - tree.center[0]) <= 2 * tree.radius:
                # recent_collision 的最后一个结点总是最后发生碰撞的
                self.recent_collision.append(tree)
                return True
        return False

    def all_fold(self):
        # 将add全部收回
        for t in self.contents.copy():
            if t.left is not None and t.left.val is None:
                self.pop(t.left)
                t.left = None
                t.arrow_image_left = t.arrow_down_left
            if t.right is not None and t.right.val is None:
                self.pop(t.right)
                t.right = None
                t.arrow_image_right = t.arrow_down_right
        self.contents[0].adjustTree(True)
        if len(self.recent_collision) > 0:
            self.recent_collision[-1].adjustTree(False)
        else:
            self.contents[0].adjustTree(False)