#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print("=" * 60)
print("Temu 图片下载工具 - 运行环境测试")
print("=" * 60)
print()

tests_passed = 0
tests_total = 0

def test(name, condition):
    global tests_passed, tests_total
    tests_total += 1
    if condition:
        print(f"✓ {name}")
        tests_passed += 1
        return True
    else:
        print(f"✗ {name}")
        return False

print("1. 检查Python版本...")
test("Python版本 >= 3.8", sys.version_info >= (3, 8))
print(f"   当前版本: {sys.version}")
print()

print("2. 检查必需的模块...")
test("threading模块", end='')
try:
    import threading
    print(" - OK")
    tests_passed += 1
except ImportError:
    print(" - FAILED")
print()

test("urllib模块", end='')
try:
    import urllib.request
    print(" - OK")
    tests_passed += 1
except ImportError:
    print(" - FAILED")
print()

print("3. 检查文件...")
test("主程序文件存在", os.path.exists("temu_downloader.py"))
test("数据文件存在", os.path.exists("temu_data_1778315436173.txt"))
print()

print("4. 测试数据文件格式...")
try:
    with open("temu_data_1778315436173.txt", 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        parts = first_line.split('-----')
        test("数据格式正确（包含3个字段）", len(parts) >= 3)
        test("ID字段非空", len(parts[0].strip()) > 0)
        test("URL字段有效", parts[1].strip().startswith('http'))
        print(f"   示例ID: {parts[0].strip()}")
        print(f"   示例URL: {parts[1].strip()[:50]}...")
except Exception as e:
    print(f"✗ 读取数据文件失败: {e}")
print()

print("=" * 60)
print(f"测试结果: {tests_passed}/{tests_total} 通过")
print("=" * 60)

if tests_passed == tests_total:
    print("\n🎉 所有测试通过！程序应该可以正常运行。\n")
    print("下一步:")
    print("  方式1: 双击运行 '一键打包.bat' 生成exe文件")
    print("  方式2: 双击运行 'run.bat' 直接启动程序")
else:
    print(f"\n⚠️  有 {tests_total - tests_passed} 个测试失败")
    print("请解决上述问题后再试。\n")

sys.exit(0 if tests_passed == tests_total else 1)
