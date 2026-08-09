# [206] 反转链表
# Link: https://leetcode.com/problems/reverse-linked-list/
# Difficulty: 1
'''
---
- 算法核心：[如：双指针 / 哈希表 / 动态规划]
- 关键点：
- 时间复杂度：O()
- 空间复杂度：O()

---
'''

# 给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。
# 
#  
#  
#  
#  
#  
# 
#  示例 1： 
#  
#  
# 输入：head = [1,2,3,4,5]
# 输出：[5,4,3,2,1]
#  
# 
#  示例 2： 
#  
#  
# 输入：head = [1,2]
# 输出：[2,1]
#  
# 
#  示例 3： 
# 
#  
# 输入：head = []
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  链表中节点的数目范围是 [0, 5000] 
#  -5000 <= Node.val <= 5000 
#  
# 
#  
# 
#  进阶：链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？ 
# 
#  Related Topics 递归 链表 👍 4175 👎 0


# leetcode submit region begin(Prohibit modify tags)
# leetcode submit region begin(Prohibit modification and deletion)
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        
# leetcode submit region end(Prohibit modification and deletion)

# leetcode submit region end(Prohibit modify tags)

if __name__ == '__main__':
    # 本地调试测试用例 (可以自己修改参数进行测试)
    solution = Solution()
    # print(solution.yourMethodName(arg1, arg2))
    pass