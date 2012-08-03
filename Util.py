'''
Created on Aug 2, 2012

@author: Prashanth
'''

import re

class Util(object):
    '''
    classdocs
    '''


    def _strict_bigger_version(self, a, b):
        a_nums = a.split('.')
        b_nums = b.split('.')
        num_fields = min(len(a_nums), len(b_nums))
        for i in range(0,num_fields):
            if   int(a_nums[i]) > int(b_nums[i]):
                return a
            elif int(a_nums[i]) < int(b_nums[i]):
                return b
        if   len(a_nums) > len(b_nums):
            return a
        elif len(a_nums) < len(b_nums):
            return b
        else:
            return None
    
    
    def bigger_version(self, a, b):
        # We compare versions this way (with examples):
        #   + 0.3 and 0.3.1:
        #     0.3.1 wins: 0.3 == 0.3 and 0.3.1 has another digit
        #   + 0.3-1 and 0.3-2:
        #     0.3-2 wins: 0.3 == 0.3 and 1 < 2
        #   + 0.3.1-1 and 0.3-2:
        #     0.3.1-1 wins: 0.3.1 > 0.3
        a_nums = a.split('-')
        b_nums = b.split('-')
        num_fields = min(len(a_nums), len(b_nums))
        for i in range(0,num_fields):
            bigger = self._strict_bigger_version(a_nums[i], b_nums[i])
            if   bigger == a_nums[i]:
                return a
            elif bigger == b_nums[i]:
                return b
        if len(a_nums) > len(b_nums):
            return a
        else:
            return b
    
    
    def version_gt(self, a, b):
        if a == b:
            return False
    
        bigger = self.bigger_version(a, b)
        return a == bigger
    
    def version_ge(self, a, b):
        if a == b:
            return True
    
        bigger = self.bigger_version(a, b)
        return a == bigger
