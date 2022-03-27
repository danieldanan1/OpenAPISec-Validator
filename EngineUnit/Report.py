from datetime import datetime


class Report:
    """
    the class manage the report sent to the client in the end of program
    the report build from file containing suggestion of fix, should help user to fix his schema
    """
    def __init__(self):
        self.report_text = ""
        self.report_path = r"../Reports"
        self.guide_messagesDir = r"../GuideMessages"

    def __readGuideMessage(self, file_name):
        """
        read file store in self.guide_messagesDir
        :param file_name: str the name of the Guide message
        :return: str the content of the file
        """
        with open(f"{self.guide_messagesDir}/{file_name}.md",'r') as f:
            message = f.read()
        return message

    def addToReport(self, file_name, path_in_schema):
        """
        add to report the selected guide message
        :param file_name: str the name of the guide message
        :param path_in_schema: str the path current in the open api scheme in order to show the location the message point
        :return: void
        """
        self.report_text += f"\n### Loaction: {path_in_schema}\n"
        self.report_text += self.__readGuideMessage(file_name)

    def createReport(self):
        """
        create the report file in the end of the run show the user the result of the validation presses
        :return: void
        """
        date = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        with open(f"{self.report_path}/report.md",'w') as f:
            if self.report_text.strip() == "":
                f.write(self.__readGuideMessage("success"))
            else:
                f.write(self.report_text)
