# 贪吃蛇游戏 - 快速定位指南

> 60秒找到需要修改的代码

## 🎯 需求 → 代码速查表

| 我想改... | 找这个文件 | 找这个位置 |
|---------|-----------|-----------|
| **游戏速度** | `src/config/settings.py` | 第11行 `FPS` |
| **窗口大小** | `src/config/settings.py` | 第19行 `WINDOW_SIZE` |
| **网格大小** | `src/config/settings.py` | 第9-10行 |
| **每个食物分数** | `src/config/settings.py` | 第21行 + `src/engine/game_loop.py` 第76行 |
| **蛇的颜色** | `src/config/colors.py` | 第23-25行 |
| **食物颜色** | `src/config/colors.py` | 第27行 |
| **背景颜色** | `src/config/colors.py` | 第20行 |
| **蛇的初始长度** | `src/models/snake.py` | 第46-54行 |
| **蛇的移动速度** | 见"游戏速度" | 同上 |
| **按键控制** | `src/engine/input_handler.py` | 第31-49行 |
| **碰撞规则** | `src/engine/collision.py` | 全文 |
| **分数显示** | `src/renderer/renderer.py` | 第101-110行 |
| **暂停功能** | `src/models/game_state.py` | 第100-115行 |
| **重新开始** | `src/engine/game_loop.py` | 第38-40行 |

---

## 📂 文件结构一图看懂

```
snake-game/
│
├── 📱 启动游戏
│   └── src/main.py                    ← 唯一的入口文件
│
├── 🎮 游戏逻辑 (怎么玩)
│   ├── src/engine/game_loop.py        ← 主循环，处理输入和更新
│   ├── src/engine/collision.py       ← 碰撞检测（撞墙、撞自己）
│   └── src/engine/input_handler.py   ← 按键映射（方向键、WASD）
│
├── 🐍 数据模型 (游戏里有什么)
│   ├── src/models/snake.py           ← 蛇：移动、增长、方向
│   ├── src/models/food.py            ← 食物：随机生成
│   ├── src/models/position.py        ← 坐标：(x, y) 位置
│   ├── src/models/direction.py       ← 方向：上下左右
│   └── src/models/game_state.py      ← 状态：分数、暂停、结束
│
├── 🎨 画面显示 (长什么样)
│   ├── src/renderer/renderer.py      ← 绘制蛇、食物、文字
│   └── src/config/colors.py          ← 配色方案
│
└── ⚙️ 配置参数 (调参数)
    └── src/config/settings.py         ← 网格大小、速度、分数
```

---

## 🔧 常见修改一键定位

### 场景1: "游戏太快/太慢"

```
打开: src/config/settings.py
找到: FPS: int = 5
修改: FPS: int = 10  # 数字越大越快
```

### 场景2: "窗口太小"

```
打开: src/config/settings.py
找到: WINDOW_SIZE: int = 600
修改: WINDOW_SIZE: int = 800
```

### 场景3: "网格太密/太疏"

```
打开: src/config/settings.py
找到: GRID_WIDTH: int = 20
      GRID_HEIGHT: int = 20
修改: GRID_WIDTH: int = 30  # 改成你想要的大小
```

### 场景4: "想改蛇的颜色"

```
打开: src/config/colors.py
找到: SNAKE_HEAD: tuple = (76, 175, 80)
修改: SNAKE_HEAD: tuple = (255, 0, 0)  # RGB格式，改成红色
```

### 场景5: "想改吃的分数"

```
打开: src/config/settings.py
找到: POINTS_PER_FOOD: int = 10
修改: POINTS_PER_FOOD: int = 20

同时打开: src/engine/game_loop.py
找到: score=self.state.score + 10
修改: score=self.state.score + Settings.POINTS_PER_FOOD
```

### 场景6: "想添加新的控制键"

```
打开: src/engine/input_handler.py
找到: KEY_MAP = {...}
添加: pygame.K_your_key: InputAction.YOUR_ACTION
```

### 场景7: "想修改初始蛇长度"

```
打开: src/models/snake.py
找到: create_default() 方法
修改: body 元组中有3个 Position，添加更多
```

---

## 🎯 功能模块快速索引

### 模块1: 蛇的行为

**文件**: `src/models/snake.py`

| 功能 | 行号 |
|------|------|
| 蛇移动 | 57-77 |
| 蛇吃食物增长 | 79-87 |
| 改变方向 | 89-105 |
| 检查自碰撞 | 107-114 |
| 创建默认蛇 | 35-55 |

---

### 模块2: 碰撞检测

**文件**: `src/engine/collision.py`

| 功能 | 行号 |
|------|------|
| 墙壁碰撞 | 20-29 |
| 自身碰撞 | 31-40 |
| 食物碰撞 | 42-52 |
| 任意碰撞 | 54-67 |

---

### 模块3: 渲染

**文件**: `src/renderer/renderer.py`

| 功能 | 行号 |
|------|------|
| 主渲染方法 | 37-63 |
| 绘制蛇（三角形） | 65-77 |
| 绘制三角形段 | 79-104 |
| 绘制连接线 | 106-130 |
| 计算三角形中心 | 132-142 |
| 绘制食物 | 144-162 |
| 绘制分数 | 164-173 |
| 绘制文本 | 175-190 |
| 坐标转换 | 192-200 |

---

### 模块4: 游戏循环

**文件**: `src/engine/game_loop.py`

| 功能 | 行号 |
|------|------|
| 初始化 | 14-28 |
| 处理输入 | 30-50 |
| 更新状态 | 52-84 |
| 运行游戏 | 86-137 |

---

## 📊 修改影响评估矩阵

### 低风险修改 (1个文件)

| 修改内容 | 涉及文件 | 测试文件 |
|---------|---------|---------|
| 修改颜色 | `colors.py` | `test_renderer/` |
| 修改速度/大小 | `settings.py` | `test_config/` |
| 修改分数值 | `settings.py`, `game_loop.py` | `test_engine/` |

### 中等风险修改 (2-3个文件)

| 修改内容 | 涉及文件 | 测试文件 |
|---------|---------|---------|
| 修改碰撞规则 | `collision.py`, `game_loop.py` | `test_engine/` |
| 修改蛇行为 | `snake.py`, `game_state.py` | `test_models/` |
| 添加新功能键 | `input_handler.py`, `game_loop.py` | `test_engine/` |

### 高风险修改 (4+个文件)

| 修改内容 | 涉及文件 | 测试文件 |
|---------|---------|---------|
| 添加道具系统 | 5+ 个文件 | 需新增测试 |
| 添加障碍物 | 5+ 个文件 | 需新增测试 |
| 添加关卡系统 | 6+ 个文件 | 需新增测试 |

---

## 🔍 搜索技巧

### 按功能搜索代码

```bash
# 查找与"分数"相关的代码
grep -r "score" src/ --include="*.py"

# 查找与"碰撞"相关的代码
grep -r "collision" src/ --include="*.py"

# 查找与"绘制"相关的代码
grep -r "def.*draw" src/renderer/ --include="*.py"
```

### 按文件搜索功能

```bash
# 查看 snake.py 中有哪些方法
grep "^    def " src/models/snake.py

# 查看 game_loop.py 的类结构
grep "^class\|^    def " src/engine/game_loop.py
```

---

## 📞 快速帮助

### 不知道改哪个文件？

1. **先看这份文档的"需求 → 代码速查表"**
2. **再看"文件结构一图看懂"**
3. **最后看"常见修改一键定位"**

### 改坏了怎么办？

```bash
# 查看修改了什么
git diff

# 恢复单个文件
git checkout -- src/your_file.py

# 撤销所有修改
git checkout .

# 运行测试检查
pytest tests/
```

### 需要更多帮助？

- 查看完整文档：`CODEMAP.md`
- 查看测试示例：`tests/unit/`
- 查看代码注释：源文件中的 docstring

---

**提示**: 建议先阅读 `CODEMAP.md` 了解完整架构，再用这份文档快速定位！

**版本**: v1.0 | **更新**: 2026-02-25
