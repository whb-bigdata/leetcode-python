# [217] 存在重复元素
# Link: https://leetcode.com/problems/contains-duplicate/
# Difficulty: 1
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 给你一个整数数组 nums 。如果任一值在数组中出现 至少两次 ，返回 true ；如果数组中每个元素互不相同，返回 false 。
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：nums = [1,2,3,1] 
#  
# 
#  输出：true 
# 
#  解释： 
# 
#  元素 1 在下标 0 和 3 出现。 
# 
#  示例 2： 
# 
#  
#  输入：nums = [1,2,3,4] 
#  
# 
#  输出：false 
# 
#  解释： 
# 
#  所有元素都不同。 
# 
#  示例 3： 
# 
#  
#  输入：nums = [1,1,1,3,3,4,3,2,4,2] 
#  
# 
#  输出：true 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10⁵ 
#  -10⁹ <= nums[i] <= 10⁹ 
#  
# 
#  Related Topics 数组 哈希表 排序 👍 1173 👎 0


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    # print(solution.yourMethodName(arg1, arg2))
    pass