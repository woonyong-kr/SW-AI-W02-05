#https://leetcode.com/problems/sort-list/?envType=study-plan-v2&envId=top-interview-150
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        if not head or not head.next:
            return head

        mid = self.getMid(head)

        return self.merge(self.sortList(head), self.sortList(mid))
    
    def merge(self, head: Optional[ListNode], mid: Optional[ListNode]):
        dummy = ListNode()
        curr = dummy

        while head and mid:
            if head.val < mid.val:
                curr.next = head
                head = head.next
            else:
                curr.next = mid
                mid = mid.next
            curr = curr.next
        curr.next = head if head else mid
        return dummy.next

    def getMid(self, head: Optional[ListNode]):
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        mid = slow.next
        slow.next = None
        return mid
    