# 导入

```python
from PythonTool import *
```

`PythonTool`依赖库：`manim`

***发现任何bug或问题，请反馈到tommy1008@dingtalk.com，谢谢！** 

---

## $\text{Manim}$工具

了解更多详情，请前往[$\text{Manim Community}$](https://www.manim.community)

### 使用

```python
m = ManimTool()
m.func_name()
```

### 公式与图形

```python
# 定义
def ChineseMathTex(*texts, color=WHITE, font="SimSun", font_size=DEFAULT_FONT_SIZE, tex_to_color_map={}):
# 使用
var_name = ChineseMathTex(...)
```

创建中文数学公式，在此函数的公式部分和直接写入中文即可，无需包裹`\text{}`，返回`MathTex()`。

- 其余用法与$\text{Manim}$原版`MathTex()`相同。

```python
# 定义
def YellowCircle(dot1, dot2):
# 使用
var_name = YellowCircle(...)
```

***该函数即将被删除！如果需要请使用`VisDrawArc()`！***

创建以`dot1`为圆心，`dot1`到`dot2`的距离为半径的黄色圆，返回`Circle()`。

- `dot1`和`dot2`均为$\text{Manim}$中的位置`[x,y,z]`。

```python
# 定义
def YellowLine(start, end):
# 使用
var_name = YellowLine(...)
```

创建以`start`开始，到`end`结束的黄色线，返回`Line()`。

- 用法与$\text{Manim}$原版`Line()`相同。

```python
# 定义
def LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1):
# 使用
var_name = LabelDot(...)
```

创建一个带有名字的点，返回带有点和名字的`VGroup()`。

1. `dot_label`：点的名字，字符串。

2. `dot_pos`：点的位置，$\text{Manim}$中的位置`[x,y,z]`。

3. `label_pos`：点的名字相对于点的位置，$\text{Manim}$中的八个方向。

4. `buff`：点的名字与点的间距，数值。

```python
# 定义
def MathTexLine(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
# 使用
var_name = MathTexLine(...)
```

创建以`start`开始，到`end`结束的线，但可以标注文字、公式等，返回带有线和标注内容的`VGroup()`。

1. `start`和`end`用法与$\text{Manim}$原版`Line()`相同。

2. `mathtex`、`color`、`font_size`用法与$\text{Manim}$原版`MathTex()`相同，不过`mathtex`只能是单个字符串。

3. `direction`：标注内容相对于线的位置，$\text{Manim}$中的八个方向。

4. `buff`：标注内容与线的间距，数值。

```python
# 定义
def MathTexBrace(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
# 使用
var_name = MathTexBrace(...)
```

创建一个从`start`开始，`end`结束的大括号，并且可以在大括号上标注文字、公式等，返回带有大括号和标注内容的`VGroup()`。

- 用法与`MathTexLine()`相同。

```python
# 定义
def MathTexDoublearrow(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
# 使用
var_name = MathTexDoublearrow(...)
```

创建一个从`start`开始，`end`结束的双箭头线，并且可以在双箭头上标注文字、公式等，返回带有双箭头线和标注内容的`VGroup()`。

- 用法与`MathTexLine()`相同。

```python
# 定义
def ExtendLine(line: Line, extend_distance: float) -> Line:
# 使用
var_name = ExtendLine(...)
```

将一条线延长`extend_distance`的距离，返回延长后的`Line()`。

1. `line`：$\text{Manim}$中的`Line()`类型。

2. `extend_distance`：要延长的距离，数值。

### 交点

```python
# 定义
def CircleInt(circle1, circle2):
# 使用
var_name = CircleInt(...)
```

寻找两个圆的两个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

`circle1`和`circle2`均为$\text{Manim}$中的`Circle()`类型。

```python
# 定义
def LineCircleInt(line, circle):
# 使用
var_name = LineCircleInt(...)
```

寻找一条线和一个圆的一个或两个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

1. `line`：$\text{Manim}$中的`Line()`类型。

2. `circle`：$\text{Manim}$中的`Circle()`类型。

```python
# 定义
def LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
# 使用
var_name = LineInt(...)
```

寻找两条线的一个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

- `line1`和`line2`均为$\text{Manim}$中的`Line()`类型。

### 动画

```python
# 定义
class VisDrawArc(Animation):
    def __init__(self, p1, p2, angle=PI, axis=OUT, **kwargs):
# 使用
class ...(Scene):
    def construct(self):
        self.play(VisDrawArc(...))
```

 创建可视化的绘弧动画。显示圆心、半径等，返回绘制的`Arc()`，便于之后动画的使用。

1. `self`：绘制动画的场景，**无需设置**。

2. `p1`： 代表圆规的针，绘制时不动的点。

3. `p2`：代表圆规的笔芯，绘制圆弧的点。

4. `angle`：绘制圆弧的角度，默认`PI`，相当于绘制半个圆。

5. `axis`：只有2个值`IN`和`OUT`，分别表示顺时针还是逆时针作弧。

6. `**kwargs`：其余参数，如`run_time`。

## 排序工具

### 使用

```python
s = SortTool()
s.func_name()
```

### 说明

```python
def sort(arr: List[T], key: Callable[[T], T] = lambda x: x, reverse: bool = False) -> None:
```

内省排序`Introsort`，C++中`<algorithm>`使用的排序方法，结合了多种排序算法的优点，以确保在各种情况下都能获得高效的性能，不返回列表。

1. `arr`：待排序的列表。

2. `key`：用于比较的键函数，自定义排序规则，而不必修改原始数据。
   
   ```python
   # 示例代码
   s = SortTool()
   numbers = [-5, 3, -2, 1, 4]
   s.sort(numbers, key=abs)  # 使用内置的 abs 函数作为 key ，即以绝对值大小排序
   print(numbers)
   # 输出
   [1, -2, 3, 4, -5]
   ```

3. `reverse`：是否降序排列，默认为升序。


