class Test:
    def __init__(self,num):
        self.__num=num
    def getnum(self):
        return self.__num
test=Test(10)
print(test.__num)