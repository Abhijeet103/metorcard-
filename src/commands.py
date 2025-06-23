from abc import ABC

from  service import MetroService

metroService  =   MetroService()

class CommandHandler(ABC) :
    def check_command(self):
        pass

    def handle_command(self):
        pass

class BalanceHandler(CommandHandler) :
    def check_command(self  ,command ):
        return command ==  "BALANCE"

    def handle_command(self , parts):
        metroService.create_card(parts[0] ,  parts[1])




class CheckInHandler(CommandHandler) :
    def check_command(self  ,command ):
        return command ==  "CHECK_IN"

    def handle_command(self , parts):
        metroService.check_in(parts[0] ,  parts[1] , parts[3])



class PrintSummaryHandler(CommandHandler) :
    def check_command(self  ,command ):
        return command ==  "PRINT_SUMMARY"

    def handle_command(self , parts):
        return  metroService.summary()

