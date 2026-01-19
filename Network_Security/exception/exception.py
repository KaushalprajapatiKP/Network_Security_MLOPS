import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.linno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name [{0}] line numer [{1}] error message [{2}]".format(self.file_name, self.linno, str(self.error_message))

if __name__ == "__main__":
    try:
        a = 1/0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e