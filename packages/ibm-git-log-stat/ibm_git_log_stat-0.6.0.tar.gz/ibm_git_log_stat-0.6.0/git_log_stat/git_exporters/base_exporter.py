from abc import ABC, abstractmethod

from git_log_stat.app_logs.logger_service import IBMLogger


class BaseExporter(ABC):

    def __init__(self):
        self.log = IBMLogger("GitExporter").get_logger()

    @abstractmethod
    def export(self, output_file_name, commit_output, pr_output=None):
        """
        Export method to be implemented by each type of exporter.
        :param output_file_name: output file name to be used
        :param commit_output: commit logs to be exported
        :param pr_output: pr logs to be exported. Optional.
        :return: Path where file is exported successfully.
        """
        pass

    @staticmethod
    def export_count(commit_output: str, pr_output: str=None):
        if pr_output:
            return len(commit_output.split("\n")), len(pr_output.split("\n"))
        else:
            return len(commit_output.split("\n"))