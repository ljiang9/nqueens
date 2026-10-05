#!/usr/bin/env python3
"""nqueens: N 皇后求解器与可视化。

解法: 位运算回溯。列 / 左下对角线 / 右下对角线各用一个位掩码记录
攻击位, 每次取最低可用位放置皇后, 递归下一行。
"""
import argparse
import sys


def solve_bit(n):
    """位运算回溯, 返回所有解(每解为各行皇后所在列的元组)。"""
    mask = (1 << n) - 1
    solutions = []
    cols = [-1] * n

    def backtrack(row, col_bits, diag1, diag2):
        if row == n:
            solutions.append(tuple(cols))
            return
        available = mask & ~(col_bits | diag1 | diag2)
        while available:
            bit = available & -available  # 取最低可用位
            available -= bit
            c = bit.bit_length() - 1
            cols[row] = c
            backtrack(row + 1, col_bits | bit,
                      (diag1 | bit) << 1, (diag2 | bit) >> 1)
            cols[row] = -1

    backtrack(0, 0, 0, 0)
    return solutions


def solve_naive(n):
    """朴素回溯, 用于交叉验证(不做位运算)。"""
    solutions = []
    cols = [-1] * n

    def safe(row, c):
        for r in range(row):
            if cols[r] == c or abs(cols[r] - c) == row - r:
                return False
        return True

    def backtrack(row):
        if row == n:
            solutions.append(tuple(cols))
            return
        for c in range(n):
            if safe(row, c):
                cols[row] = c
                backtrack(row + 1)
                cols[row] = -1

    backtrack(0)
    return solutions


def is_valid(sol, n):
    """验证一个解确实没有皇后互攻。"""
    if len(sol) != n or set(sol) != set(range(n)):
        return False
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            if abs(sol[r1] - sol[r2]) == r2 - r1:
                return False
    return True


def render(sol, n):
    """ASCII 棋盘渲染。"""
    lines = []
    for r in range(n):
        row = "".join(" Q " if sol[r] == c else " . " for c in range(n))
        lines.append(row)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="N 皇后求解器: 位运算回溯")
    ap.add_argument("--n", type=int, default=8, help="棋盘边长, 默认 8")
    ap.add_argument("--count", action="store_true", help="只计数, 不打印棋盘")
    ap.add_argument("--all", action="store_true", help="打印所有解(只配合小的 --n 用)")
    args = ap.parse_args(argv)

    n = args.n
    if not 1 <= n <= 16:
        print("error: --n 必须在 1 到 16 之间", file=sys.stderr)
        return 2

    solutions = solve_bit(n)
    print(f"n={n}, 共 {len(solutions)} 个解")
    if args.count:
        return 0
    if args.all:
        if n > 8:
            print("error: --all 只支持 n <= 8, 解太多会刷屏", file=sys.stderr)
            return 2
        for i, sol in enumerate(solutions, 1):
            print(f"\n--- 解 {i}/{len(solutions)} ---")
            print(render(sol, n))
    else:
        print("\n第一个解:")
        print(render(solutions[0], n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
