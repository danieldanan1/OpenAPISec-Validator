from datetime import datetime


class Report:
    def __init__(self):
        self.report_text = ""
        self.report_path = r"../Reports"
        self.guide_messagesDir = r"../GuideMessages"

    def __readGuideMessage(self,file_name):
        with open(f"{self.guide_messagesDir}/{file_name}.md",'r') as f:
            message = f.read()
        return message

    def addToReport(self,file_name,path_in_schema):
        self.report_text += f"\n### Loaction: {path_in_schema}\n"
        self.report_text += self.__readGuideMessage(file_name)

    def createReport(self):
        date = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        with open(f"{self.report_path}/report_{date}.md",'w') as f:
            f.write(self.report_text)
