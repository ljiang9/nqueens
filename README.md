# nqueens

N 皇后求解器与 ASCII 可视化。纯 Python 标准库。

## 玩法

```bash
python -m nqueens            # 解 n=8, 打印第一个解
python -m nqueens --count    # 只计数: n=8 共 92 个解
python -m nqueens --all --n 4  # 打印 n=4 的全部 2 个解
python -m nqueens --n 12     # 解 n=12
```

## 设计取舍

- **位运算回溯**: 列、两条对角线各用一个整数位掩码记录攻击位,
  `available & -available` 取最低可用位, 递归下一行。n=8 毫秒级完成。
- `solve_naive` 是朴素回溯版本, 仅用于交叉验证, CLI 默认用位运算版。
- n 限制在 1–16: 解数随 n 指数增长, `--all` 只允许 n<=8(刷屏保护)。

## 已知局限

- 只输出"皇后各行所在列"的一种表示, 无镜像/旋转去重。
- 计数版不做对称性剪枝, n>12 会明显变慢。
- 纯终端 ASCII 棋盘, 无图形界面。

## 协议

MIT, Copyright (c) 2026 ljiang9
