from abc import ABC

from  src.service import MetroService

metroService  =   MetroService()

class CommandHandler(ABC) :
    def handle_command(self):
        pass

class BalanceHandler(CommandHandler) :
    def __init__(self):
        self.name  =  "BALANCE"

    def handle_command(self , parts):
        metroService.create_card(parts[0] ,  parts[1])




class CheckInHandler(CommandHandler) :
    def __init__(self) :
        self.name  = "CHECK_IN"


    def handle_command(self , parts):
        metroService.check_in(parts[0] ,  parts[1] , parts[2])



class PrintSummaryHandler(CommandHandler) :
    def __init__(self):
        self.name  = "PRINT_SUMMARY"

    def handle_command(self , parts):
        print(metroService.summary())

