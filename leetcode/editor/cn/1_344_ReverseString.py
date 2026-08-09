# [344] 反转字符串
# Link: https://leetcode.com/problems/reverse-string/
# Difficulty: 1
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 s 的形式给出。 
# 
#  不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = ["h","e","l","l","o"]
# 输出：["o","l","l","e","h"]
#  
# 
#  示例 2： 
# 
#  
# 输入：s = ["H","a","n","n","a","h"]
# 输出：["h","a","n","n","a","H"] 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 10⁵ 
#  s[i] 都是 ASCII 码表中的可打印字符 
#  
# 
#  Related Topics 双指针 字符串 👍 1011 👎 0


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def reverseString(self, s):
        """
        :type s: List[str]
        :rtype: None Do not return anything, modify s in-place instead.
        """
        
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    # print(solution.yourMethodName(arg1, arg2))
    pass