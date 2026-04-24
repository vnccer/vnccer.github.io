class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if (complement := target - num) in seen:
                return [seen[complement], i]
            seen[num] = i

# 本地运行的测试代码
if __name__ == "__main__":
    sol = Solution()

    # 测试用例 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(sol.twoSum(nums1, target1))  # 输出: [0, 1]

    # 测试用例 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(sol.twoSum(nums2, target2))  # 输出: [1, 2]

    # 测试用例 3
    nums3 = [3, 3]
    target3 = 6
    print(sol.twoSum(nums3, target3))  # 输出: [0, 1]