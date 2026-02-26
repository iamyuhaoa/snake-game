# 贪吃蛇游戏代码映射文档

> 用于快速定位功能对应的代码文件

## 📋 目录

- [功能到代码映射](#功能到代码映射)
- [代码文件功能说明](#代码文件功能说明)
- [常见需求变更指南](#常见需求变更指南)
- [依赖关系图](#依赖关系图)

---

## 🎯 功能到代码映射

### 游戏核心机制

| 功能需求 | 对应文件 | 关键类/函数 | 行号范围 |
|---------|---------|------------|---------|
| **蛇的移动** | `src/models/snake.py` | `Snake.move()` | 57-77 |
| **蛇的增长** | `src/models/snake.py` | `Snake.grow()` | 79-87 |
| **方向控制** | `src/models/snake.py` | `Snake.change_direction()` | 89-105 |
| **防反向移动** | `src/models/snake.py` | `Snake.change_direction()` | 101-103 |
| **碰撞检测** | `src/engine/collision.py` | `CollisionChecker` | 全文 |
| **墙壁碰撞** | `src/engine/collision.py` | `check_wall_collision()` | 20-29 |
| **自身碰撞** | `src/engine/collision.py` | `check_self_collision()` | 31-40 |
| **食物碰撞** | `src/engine/collision.py` | `check_food_collision()` | 42-52 |

### 游戏状态管理

| 功能需求 | 对应文件 | 关键类/函数 | 行号范围 |
|---------|---------|------------|---------|
| **分数计算** | `src/models/game_state.py` | `GameState.move_snake()` | 60-79 |
| **分数值** | `src/config/settings.py` | `POINTS_PER_FOOD` | 21 |
| **暂停/继续** | `src/models/game_state.py` | `GameState.pause/resume()` | 100-128 |
| **游戏结束** | `src/models/game_state.py` | `GameState.game_over()` | 130-143 |
| **重新开始** | `src/engine/game_loop.py` | `GameLoop.handle_input()` | 38-40 |

### 渲染相关

| 功能需求 | 对应文件 | 关键类/函数 | 行号范围 |
|---------|---------|------------|---------|
| **窗口大小** | `src/config/settings.py` | `WINDOW_SIZE` | 19 |
| **网格大小** | `src/config/settings.py` | `GRID_WIDTH/HEIGHT` | 9-10 |
| **游戏速度** | `src/config/settings.py` | `FPS` | 11 |
| **蛇的颜色** | `src/config/colors.py` | `SNAKE_HEAD/BODY` | 23-25 |
| **食物颜色** | `src/config/colors.py` | `FOOD` | 27 |
| **背景颜色** | `src/config/colors.py` | `BACKGROUND` | 20 |
| **渲染蛇（三角形）** | `src/renderer/renderer.py` | `_draw_snake()` | 65-77 |
| **绘制三角形段** | `src/renderer/renderer.py` | `_draw_triangle_segment()` | 79-104 |
| **绘制连接线** | `src/renderer/renderer.py` | `_draw_snake_connections()` | 106-130 |
| **渲染食物** | `src/renderer/renderer.py` | `_draw_food()` | 144-162 |
| **显示分数** | `src/renderer/renderer.py` | `_draw_score()` | 101-110 |
| **显示游戏结束** | `src/renderer/renderer.py` | `render()` | 52-58 |

### 输入控制

| 功能需求 | 对应文件 | 关键类/函数 | 行号范围 |
|---------|---------|------------|---------|
| **方向键映射** | `src/engine/input_handler.py` | `KEY_MAP` | 31-49 |
| **WASD映射** | `src/engine/input_handler.py` | `KEY_MAP` | 38-41 |
| **空格暂停** | `src/engine/input_handler.py` | `PAUSE action` | 28 |
| **R重启** | `src/engine/input_handler.py` | `RESTART action` | 29-30 |
| **Q/ESC退出** | `src/engine/input_handler.py` | `QUIT action` | 31-34 |
| **按键处理** | `src/engine/game_loop.py` | `handle_input()` | 30-50 |

### 游戏规则

| 功能需求 | 对应文件 | 关键类/函数 | 行号范围 |
|---------|---------|------------|---------|
| **初始蛇长度** | `src/models/snake.py` | `create_default()` | 35-55 |
| **网格尺寸** | `src/config/settings.py` | `GRID_WIDTH/HEIGHT` | 9-10 |
| **食物分数** | `src/config/settings.py` | `POINTS_PER_FOOD` | 21 |
| **蛇的初始位置** | `src/models/snake.py` | `create_default()` | 46-54 |

---

## 📁 代码文件功能说明

### 核心模型层 (`src/models/`)

#### `position.py` - 网格位置
```python
Position(x, y)           # 2D坐标
Position.ZERO            # 原点常量
Position.add()           # 位置相加
Position.is_adjacent()   # 检查相邻
Position.distance_to()   # 曼哈顿距离
Position.is_in_bounds()  # 边界检查
```
**修改场景**: 改变网格坐标系、距离计算方式

#### `direction.py` - 移动方向
```python
Direction.UP/DOWN/LEFT/RIGHT  # 四个方向
Direction.delta              # 方向向量
Direction.opposite           # 相反方向
Direction.to_direction()      # 动作转方向
```
**修改场景**: 添加斜向移动、8方向控制

#### `snake.py` - 蛇实体
```python
Snake.body              # 身体段（元组）
Snake.head              # 头部位置
Snake.direction         # 当前方向
Snake.move()            # 移动逻辑
Snake.grow()            # 增长逻辑
Snake.change_direction() # 改变方向
Snake.collides_with_self() # 自碰撞检测
```
**修改场景**: 改变蛇的行为、添加特殊能力

#### `food.py` - 食物实体
```python
Food.position                # 食物位置
Food.spawn_random()          # 随机生成
```
**修改场景**: 添加不同类型食物、特殊食物效果

#### `game_state.py` - 游戏状态
```python
GameState.snake         # 当前蛇
GameState.food          # 当前食物
GameState.score         # 当前分数
GameState.status        # 游戏状态
GameState.move_snake()  # 移动蛇
GameState.change_direction()
GameState.pause/resume()
GameState.game_over()
```
**修改场景**: 添加新的游戏状态属性

### 引擎层 (`src/engine/`)

#### `collision.py` - 碰撞检测
```python
CollisionChecker(width, height)
  .check_wall_collision()    # 墙壁碰撞
  .check_self_collision()    # 自身碰撞
  .check_food_collision()    # 食物碰撞
  .has_collision()           # 任意碰撞
```
**修改场景**: 添加新的碰撞类型、障碍物

#### `input_handler.py` - 输入处理
```python
InputHandler.KEY_MAP         # 按键映射
InputHandler.handle_key()    # 处理按键
InputAction.to_direction()   # 动作转方向
```
**修改场景**: 添加新的控制键、修改按键映射

#### `game_loop.py` - 游戏循环
```python
GameLoop.__init__()         # 初始化
GameLoop.handle_input()     # 处理输入
GameLoop.update()          # 更新状态
GameLoop.run()             # 主循环
```
**修改场景**: 修改游戏流程、添加游戏阶段

### 渲染层 (`src/renderer/`)

#### `renderer.py` - 渲染器
```python
Renderer.render()                  # 主渲染方法
Renderer._draw_snake()             # 绘制蛇（三角形+连接线）
Renderer._draw_triangle_segment()  # 绘制单个三角形段
Renderer._draw_snake_connections() # 绘制三角形间的连接线
Renderer._get_triangle_center()    # 计算三角形中心点
Renderer._draw_food()              # 绘制食物
Renderer._draw_score()             # 绘制分数
Renderer._draw_text_centered()     # 绘制文本
Renderer._cell_to_rect()           # 网格坐标转像素
```
**修改场景**: 改变视觉效果、添加动画、修改蛇的形状

### 配置层 (`src/config/`)

#### `settings.py` - 游戏设置
```python
Settings.GRID_WIDTH        # 网格宽度
Settings.GRID_HEIGHT       # 网格高度
Settings.FPS               # 游戏速度
Settings.WINDOW_SIZE       # 窗口大小
Settings.POINTS_PER_FOOD   # 每个食物的分数
```
**修改场景**: 调整游戏难度、界面大小

#### `colors.py` - 颜色配置
```python
Colors.BACKGROUND          # 背景色
Colors.SNAKE_HEAD/BODY     # 蛇颜色
Colors.FOOD                # 食物颜色
Colors.TEXT_PRIMARY        # 文字颜色
```
**修改场景**: 更换配色方案

### 主程序 (`src/`)

#### `main.py` - 入口点
```python
main()                       # 主函数
  - 加载设置
  - 创建游戏循环
  - 运行游戏
  - 异常处理
```
**修改场景**: 修改启动流程、添加命令行参数

---

## 🔄 常见需求变更指南

### 需求1: "我想改变游戏速度"

**影响范围**: ⭐ 简单

**修改位置**:
```
src/config/settings.py:11
```

**修改代码**:
```python
FPS: int = 10  # 原来是5，改大更快
```

**相关配置**: 无

---

### 需求2: "我想修改网格大小为30x30"

**影响范围**: ⭐ 中等

**修改位置**:
```
src/config/settings.py:9-10
```

**修改代码**:
```python
GRID_WIDTH: int = 30
GRID_HEIGHT: int = 30
```

**相关配置**:
- 蛇的初始位置会自动调整（`src/models/snake.py:47-54`）

---

### 需求3: "我想每个食物得20分而不是10分"

**影响范围**: ⭐ 简单

**修改位置**:
```
src/config/settings.py:21
src/engine/game_loop.py:76
```

**修改代码**:
```python
# settings.py
POINTS_PER_FOOD: int = 20

# game_loop.py
score=self.state.score + Settings.POINTS_PER_FOOD,  # 或直接写20
```

---

### 需求4: "我想添加障碍物"

**影响范围**: ⭐⭐ 复杂

**需要修改**:

1. **创建障碍物模型**:
   - 新建 `src/models/obstacle.py`

2. **更新碰撞检测**:
   - 修改 `src/engine/collision.py`
   - 添加 `check_obstacle_collision()`

3. **更新食物生成**:
   - 修改 `src/models/food.py:spawn_random()`
   - 避免在障碍物位置生成食物

4. **渲染障碍物**:
   - 修改 `src/renderer/renderer.py`
   - 添加 `_draw_obstacles()`

5. **添加配置**:
   - 修改 `src/config/settings.py`
   - 添加障碍物数量、位置配置

---

### 需求5: "我想添加加速道具"

**影响范围**: ⭐⭐ 复杂

**需要修改**:

1. **创建道具类型**:
   - 新建 `src/models/powerup.py`
   - 定义道具类型（加速、减速、穿墙等）

2. **道具生成逻辑**:
   - 类似 `Food.spawn_random()`

3. **道具效果**:
   - 修改 `src/engine/game_loop.py:update()`
   - 添加道具碰撞检测和效果应用

4. **渲染道具**:
   - 修改 `src/renderer/renderer.py`
   - 不同类型道具不同颜色/图标

---

### 需求6: "我想改游戏配色"

**影响范围**: ⭐ 简单

**修改位置**:
```
src/config/colors.py
```

**修改代码**:
```python
@dataclass(frozen=True)
class Colors:
    BACKGROUND: tuple = (30, 30, 40)      # 改成你喜欢的颜色
    SNAKE_HEAD: tuple = (100, 200, 100)   # RGB格式
    SNAKE_BODY: tuple = (80, 180, 80)
    FOOD: tuple = (255, 100, 100)         # 红色改成其他
    ...
```

---

### 需求7: "我想支持触摸控制"

**影响范围**: ⭐⭐⭐ 非常复杂

**需要修改**:

1. **添加触摸输入处理**:
   - 修改 `src/engine/input_handler.py`
   - 添加 `handle_touch()` 方法

2. **修改游戏循环**:
   - 修改 `src/engine/game_loop.py:run()`
   - 处理 `pygame.FINGERDOWN` 等触摸事件

3. **添加虚拟方向键UI**:
   - 修改 `src/renderer/renderer.py`
   - 绘制触摸按钮

---

### 需求8: "我想添加音效"

**影响范围**: ⭐⭐ 中等

**需要修改**:

1. **音频管理器**:
   - 新建 `src/engine/audio.py`
   - `pygame.mixer` 管理

2. **播放音效**:
   - 修改 `src/engine/game_loop.py`
   - 移动、吃食物、碰撞时播放音效

3. **配置音效**:
   - 修改 `src/config/settings.py`
   - 添加音量、开关配置

---

### 需求9: "我想添加最高分记录"

**影响范围**: ⭐⭐ 中等

**已有文件**: `src/storage/high_score.py` (目前为空)

**需要实现**:
```python
# src/storage/high_score.py
import json
from pathlib import Path

SAVE_FILE = "highscore.json"

def load_high_score() -> int:
    """加载最高分"""
    if Path(SAVE_FILE).exists():
        with open(SAVE_FILE) as f:
            data = json.load(f)
            return data.get("high_score", 0)
    return 0

def save_high_score(score: int) -> None:
    """保存最高分"""
    with open(SAVE_FILE, "w") as f:
        json.dump({"high_score": score}, f)

def is_new_high_score(score: int) -> bool:
    """检查是否是新纪录"""
    return score > load_high_score()
```

**集成位置**:
- `src/engine/game_loop.py:update()` - 游戏结束时检查
- `src/renderer/renderer.py:render()` - 显示最高分

---

### 需求10: "我想添加关卡系统"

**影响范围**: ⭐⭐⭐ 复杂

**需要修改**:

1. **关卡配置**:
   - 新建 `src/config/levels.py`
   - 定义每关的速度、障碍物、目标分数

2. **关卡状态**:
   - 修改 `src/models/game_state.py`
   - 添加 `level` 属性

3. **关卡切换**:
   - 修改 `src/engine/game_loop.py:update()`
   - 达到目标分数后升级关卡

---

## 🔗 依赖关系图

```
main.py
  ↓
GameLoop (game_loop.py)
  ↓
  ├─→ GameState (game_state.py)
  │     ↓
  │     ├─→ Snake (snake.py)
  │     │     ↓
  │     │     └─→ Position (position.py)
  │     │
  │     ├─→ Food (food.py)
  │     │     ↓
  │     │     └─→ Position (position.py)
  │     │
  │     └─→ Direction (direction.py)
  │
  ├─→ CollisionChecker (collision.py)
  │     ├─→ Snake
  │     └─→ Food
  │
  ├─→ InputHandler (input_handler.py)
  │     └─→ Direction
  │
  └─→ Renderer (renderer.py)
        ├─→ GameState
        └─→ Colors (colors.py)

配置层:
Settings (settings.py) → GameLoop, GameState
Colors (colors.py) → Renderer
```

---

## 📊 修改影响评估表

| 修改类型 | 影响文件数 | 复杂度 | 风险等级 |
|---------|-----------|--------|---------|
| 修改配置值（速度、大小） | 1 | ⭐ | 低 |
| 修改颜色 | 1 | ⭐ | 低 |
| 修改分数值 | 2 | ⭐ | 低 |
| 添加新道具 | 5 | ⭐⭐⭐ | 高 |
| 添加障碍物 | 5 | ⭐⭐ | 中 |
| 添加音效 | 3 | ⭐⭐ | 中 |
| 添加最高分 | 3 | ⭐⭐ | 中 |
| 添加关卡系统 | 6+ | ⭐⭐⭐ | 高 |
| 添加触摸控制 | 3 | ⭐⭐⭐ | 高 |

---

## 🎯 快速定位技巧

### 按功能查找

1. **搜索关键词**
   - 蛇移动：搜索 `snake.move` 或 `direction.delta`
   - 碰撞检测：搜索 `collision` 或 `is_over`
   - 渲染：搜索 `draw_` 或 `render`
   - 配置：搜索 `Settings` 或 `Colors`

2. **按文件类型查找**
   - 数据结构：看 `src/models/`
   - 游戏逻辑：看 `src/engine/`
   - 视觉效果：看 `src/renderer/`
   - 配置参数：看 `src/config/`

3. **按测试定位**
   - 查找功能测试：`tests/unit/test_*/test_*.py`
   - 测试文件名通常对应源文件名

### Git 历史查询

```bash
# 查看某个文件的修改历史
git log --oneline -- src/models/snake.py

# 查看某个功能的提交
git log --grep="食物" --oneline

# 查看谁修改了某个函数
git log -p -S "def move" -- src/models/snake.py
```

---

## 📝 代码修改建议

### 修改前检查清单

- [ ] 确定影响范围（查看此文档）
- [ ] 查找相关测试文件
- [ ] 阅读依赖的代码
- [ ] 运行现有测试确保通过
- [ ] 编写/更新测试
- [ ] 修改代码
- [ ] 运行测试验证

### 修改后验证

```bash
# 运行所有测试
pytest tests/

# 运行覆盖率检查
pytest tests/ --cov=src

# 运行特定模块测试
pytest tests/unit/test_models/

# 代码格式化
black src/
```

---

## 📞 快速参考

### 一句话总结各文件职责

| 文件 | 一句话描述 |
|------|-----------|
| `main.py` | 程序入口，启动游戏 |
| `models/position.py` | 网格坐标系统 |
| `models/direction.py` | 方向枚举和转换 |
| `models/snake.py` | 蛇的数据和行为 |
| `models/food.py` | 食物生成逻辑 |
| `models/game_state.py` | 游戏状态管理 |
| `engine/collision.py` | 碰撞检测逻辑 |
| `engine/input_handler.py` | 输入映射到动作 |
| `engine/game_loop.py` | 主循环和更新逻辑 |
| `renderer/renderer.py` | 绘制游戏画面 |
| `config/settings.py` | 游戏配置参数 |
| `config/colors.py` | 颜色定义 |

---

**文档版本**: v1.0
**最后更新**: 2026-02-25
**维护者**: Claude Code
