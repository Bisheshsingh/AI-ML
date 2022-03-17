import pip
from Description import requrements,allImports

class setup:
    def __init__(self):
        self.requrements=requrements
        try:
            allImports()
        except:
            self.Install()
        
    def Installing(self,package):
        if hasattr(pip, 'main'):
           pip.main(['install', package])
        else:
           pip._internal.main(['install', package])

    def Install(self):
        for i in self.requrements:
            self.Installing(i)
        return True

