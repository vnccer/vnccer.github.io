---
title: "1.两数之和"
data: 2026-04-22
draft: false
weight: 1
---

# 一、题目理解
给你一个整数数组 nums 和一个目标数 target，请在数组里找到两个不同的元素，让它们加起来等于 target，并返回这两个元素的下标。

例子：
- 输入 nums = [2,7,11,15], target = 9
- 我们找两个数相加等于 9：2 + 7 = 9，它们的下标是 0 和 1，所以返回 [0,1]。

# 二、解题
```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if (complement := target - num) in seen:
                return [seen[complement], i]
            seen[num] = i
```

|代码|作用|
|---|----|
|def twoSum(self, nums: list[int], target: int) -> list[int]:|定义一个叫 twoSum 的函数；<br />它接收一个整数数组 nums，和一个整数 target；<br />最后返回一个整数数组（两个下标）<br />self是类的函数要带的第一个参数<br />可以理解为def twoSum(nums, target):|
|seen = {}|初始化空字典，存放已遍历过的下标|
|enumerate(nums)|给数组nums里的每个元素，都配上它的位置编号|
|for i, num in enumerate(nums)|在遍历数组的时候，同时拿到下标和对应的值|
|complement := target - num|计算当前数的补数，需要和num相加得到的target的数|
|if (complement := target - num) in seen:|等价于<br />complement = target - num   # 先赋值<br />if complement in seen:      # 再判断<br />检查补数是否已经在字典里|
|return [seen[complement], i]|存在就返回补数的下标和当前下标|
|seen[num] = i|不存在就把当前数和下标存入字典|

# 三、在vscode中运行
```PYTHON
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if (complement := target - num) in seen:
                return [seen[complement], i]
            seen[num] = i


# 下面是本地运行的测试代码
if __name__ == "__main__":
    sol = Solution()
    
    # 测试用例 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"测试用例1结果: {sol.twoSum(nums1, target1)}")  # 预期输出 [0, 1]

    # 测试用例 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"测试用例2结果: {sol.twoSum(nums2, target2)}")  # 预期输出 [1, 2]

    # 测试用例 3
    nums3 = [3, 3]
    target3 = 6
    print(f"测试用例3结果: {sol.twoSum(nums3, target3)}")  # 预期输出 [0, 1]
```