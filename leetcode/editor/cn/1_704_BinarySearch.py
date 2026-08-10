# [704] 二分查找
# Link: https://leetcode.com/problems/binary-search/
# Difficulty: 1
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target ，写一个函数搜索 nums 中的 target，如果 target 存在返
# 回下标，否则返回 -1。 
# 
#  你必须编写一个具有 O(log n) 时间复杂度的算法。 
# 
#  示例 1: 
# 
#  
# 输入: nums = [-1,0,3,5,9,12], target = 9
# 输出: 4
# 解释: 9 出现在 nums 中并且下标为 4
#  
# 
#  示例 2: 
# 
#  
# 输入: nums = [-1,0,3,5,9,12], target = 2
# 输出: -1
# 解释: 2 不存在 nums 中因此返回 -1
#  
# 
#  
# 
#  提示： 
# 
#  
#  你可以假设 nums 中的所有元素是不重复的。 
#  n 将在 [1, 10000]之间。 
#  nums 的每个元素都将在 [-9999, 9999]之间。 
#  
# 
#  Related Topics数组 | 二分查找 
# 
#  👍 1901, 👎 0bug 反馈 | 使用指南 | 更多插件 
# 
# 
# 
# 


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left, right = 0, len(nums) - 1

        while left <= right:
            # 使用 left + (right - left) // 2 方式计算 mid，防止大数加法溢出
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid  # 找到目标值，返回对应的索引
            elif nums[mid] < target:
                left = mid + 1  # 目标值在右半部分，缩小左边界
            else:
                right = mid - 1  # 目标值在左半部分，缩小右边界

        return -1  # 数组中未找到目标值，返回 -1
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    # print(solution.yourMethodName(arg1, arg2))
    pass