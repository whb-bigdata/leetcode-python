# [20] 有效的括号
# Link: https://leetcode.com/problems/valid-parentheses/
# Difficulty: 1
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。 
# 
#  有效字符串需满足： 
# 
#  
#  左括号必须用相同类型的右括号闭合。 
#  左括号必须以正确的顺序闭合。 
#  每个右括号都有一个对应的相同类型的左括号。 
#  
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：s = "()" 
#  
# 
#  输出：true 
# 
#  示例 2： 
# 
#  
#  输入：s = "()[]{}" 
#  
# 
#  输出：true 
# 
#  示例 3： 
# 
#  
#  输入：s = "(]" 
#  
# 
#  输出：false 
# 
#  示例 4： 
# 
#  
#  输入：s = "([])" 
#  
# 
#  输出：true 
# 
#  示例 5： 
# 
#  
#  输入：s = "([)]" 
#  
# 
#  输出：false 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 10⁴ 
#  s 仅由括号 '()[]{}' 组成 
#  
# 
#  Related Topics栈 | 字符串 | 括号序列 
# 
#  👍 5017, 👎 0bug 反馈 | 使用指南 | 更多插件 
# 
# 
# 
# 


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        for char in s:
            if len(stack) ==0:
                stack.append(char)
            elif stack[-1] =='(' and char == ')':
                stack.pop()
            elif stack[-1] =='{' and char == '}':
                stack.pop()
            elif stack[-1] =='[' and char == ']':
                stack.pop()
            else:
                stack.append(char)
        return len(stack) == 0
        
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    arg1 = "()"
    print(solution.isValid(arg1))
    pass