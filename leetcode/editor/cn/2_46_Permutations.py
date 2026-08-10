# [46] 全排列
# Link: https://leetcode.com/problems/permutations/
# Difficulty: 2
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 给定一个不含重复数字的数组 nums ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,2,3]
# 输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [0,1]
# 输出：[[0,1],[1,0]]
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [1]
# 输出：[[1]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 6 
#  -10 <= nums[i] <= 10 
#  nums 中的所有整数 互不相同 
#  
# 
#  Related Topics 数组 回溯 👍 3365 👎 0


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    # 按照 Java 习惯写成同级方法（注意 Python 要带 self）
    def permute(self, nums: list[int]) -> list[list[int]]:
        res = []
        self._backtrack(nums, [], [False] * len(nums), res)
        return res

    # 类似于 Java 的 private 辅助方法（Python 约定下划线开头表示私有）
    def _backtrack(self, nums, path, used, res):
        if len(path) == len(nums):
            res.append(path.copy())
            return

        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            self._backtrack(nums, path, used, res)
            path.pop()
            used[i] = False
        
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    arg1 = [1, 2, 3]
    print(solution.permute(arg1))
    pass



