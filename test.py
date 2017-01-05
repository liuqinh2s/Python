class Solution(object):
    def countNumbersWithUniqueDigits(self, n):
        """
        :type n: int
        :rtype: int
        """
        nums = [9]
        for x in range(9, 0, -1):
            nums += nums[-1] * x,
        return sum(nums[:n]) + 1
    def feibonaqi(self,n):
        nums = [1,1]
        for x in range(2,n):
            nums = nums[-1] + nums[-2],
        return nums[n]

s=Solution()
s.feibonaqi(10)