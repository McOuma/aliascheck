def maxArea(height):
        l = 0
        r = len(height) - 1
        area = 0
        
        for i in range(len(height)):
            if height[l] < height[r]:
                area = max(area, height[l] * (r - l))
                l += 1
            else:
                area = max(area, height[r] * (r - l))
                r -= 1
        return area
print(maxArea(height = [1,8,6,2,5,4,8,3,7]))