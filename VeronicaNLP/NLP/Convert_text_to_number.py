#-*-coding:utf8;-*-
import re
from random import choice

class Replace(object):
    """ a simple text to number evaluating class """
    def format_number(self,text,flag=False):
        text = str(text)
        if len(text) <=1:
            text = re.sub(r"1", "01", text)
            text = re.sub(r"2", "02", text)
            text = re.sub(r"3", "03", text)
            text = re.sub(r"4", "04", text)
            text = re.sub(r"5", "05", text)
            text = re.sub(r"6", "06", text)
            text = re.sub(r"7", "07", text)
            text = re.sub(r"8", "08", text)
            text = re.sub(r"9", "09", text)
        elif flag == True:
            text = re.sub(r" 1 ", " 01 ", text)
            text = re.sub(r" 2 ", " 02 ", text)
            text = re.sub(r" 3 ", " 03 ", text)
            text = re.sub(r" 4 ", " 04 ", text)
            text = re.sub(r" 5 ", " 05 ", text)
            text = re.sub(r" 6 ", " 06 ", text)
            text = re.sub(r" 7 ", " 07 ", text)
            text = re.sub(r" 8 ", " 08 ", text)
            text = re.sub(r" 9 ", " 09 ", text)
        else:pass
        return(text)

    def replace_text_date_with_num(self,text):
        text = text.lower()
        months = {"january":"1","febuary":"2","march":"3","april":"4","may":"5","june":"6","july":"7","august":"8","september":"9","october": "10","november": "11","december": "12"}
        tokens = text.lower().split()
        for i, token in enumerate(tokens):
            if token in months:
                tokens[i] = months[token]
        result = re.sub(r"([st,rd,rd,th])", "",' '.join(tokens))
        return(result)
        
        
    def text_to_number(self,text):
        '''convert a number written as text to its real number equivalence'''
        text = text.lower()
        text = re.sub(r"zero", "0", text)
        text = re.sub(r"eleven", "11", text)
        text = re.sub(r"twelve", "12", text)
        text = re.sub(r"thirteen", "13", text)
        text = re.sub(r"fourteen", "14", text)
        text = re.sub(r"fifteen", "15", text)
        text = re.sub(r"sixteen", "16", text)
        text = re.sub(r"seventeen", "17", text)
        text = re.sub(r"eighteen", "18", text)
        text = re.sub(r"nineteen", "19", text)
        
        text = re.sub(r"twenty first", "21st", text)
        text = re.sub(r"twenty second", "22nd", text)
        text = re.sub(r"twenty third", "23rd", text)
        text = re.sub(r"twenty fourth", "24th", text)
        text = re.sub(r"twenty fifth", "25th", text)
        text = re.sub(r"twenty ninth", "29th", text)
        
        text = re.sub(r"twenty one", "21", text)
        text = re.sub(r"twenty two", "22", text)
        text = re.sub(r"twenty three", "23", text)
        text = re.sub(r"twenty four", "24", text)
        text = re.sub(r"twenty five", "25", text)
        text = re.sub(r"twenty six", "26", text)
        text = re.sub(r"twenty seven", "27", text)
        text = re.sub(r"twenty eight", "28", text)
        text = re.sub(r"twenty nine", "29", text)
        text = re.sub(r"twenty", "20", text)


        text = re.sub(r"thirty first", "31st", text)
        text = re.sub(r"thirty second", "32nd", text)
        text = re.sub(r"thirty third", "33rd", text)
        text = re.sub(r"thirty fourth", "34th", text)
        text = re.sub(r"thirty fifth", "35th", text)
        text = re.sub(r"thirty ninth", "39th", text)
        
        text = re.sub(r"thirty one", "31", text)
        text = re.sub(r"thirty two", "32", text)
        text = re.sub(r"thirty three", "33", text)
        text = re.sub(r"thirty four", "34", text)
        text = re.sub(r"thirty five", "35", text)
        text = re.sub(r"thirty six", "36", text)
        text = re.sub(r"thirty seven", "37", text)
        text = re.sub(r"thirty eight", "38", text)
        text = re.sub(r"thirty nine", "39", text)
        text = re.sub(r"thirty", "30", text)

        text = re.sub(r"forty first", "41st", text)
        text = re.sub(r"forty second", "42nd", text)
        text = re.sub(r"forty third", "43rd", text)
        text = re.sub(r"forty fourth", "44th", text)
        text = re.sub(r"forty fifth", "45th", text)
        text = re.sub(r"forty ninth", "49th", text)
        
        text = re.sub(r"forty one", "41", text)
        text = re.sub(r"forty two", "42", text)
        text = re.sub(r"forty three", "43", text)
        text = re.sub(r"forty four", "44", text)
        text = re.sub(r"forty five", "45", text)
        text = re.sub(r"forty six", "46", text)
        text = re.sub(r"forty seven", "47", text)
        text = re.sub(r"forty eight", "48", text)
        text = re.sub(r"forty nine", "49", text)
        text = re.sub(r"forty", "40", text)

        text = re.sub(r"fifty first", "51st", text)
        text = re.sub(r"fifty second", "52nd", text)
        text = re.sub(r"fifty third", "53rd", text)
        text = re.sub(r"fifty fourth", "54th", text)
        text = re.sub(r"fifty fifth", "55th", text)
        text = re.sub(r"fifty ninth", "59th", text)
        
        text = re.sub(r"fifty one", "51", text)
        text = re.sub(r"fifty two", "52", text)
        text = re.sub(r"fifty three", "53", text)
        text = re.sub(r"fifty four", "54", text)
        text = re.sub(r"fifty five", "55", text)
        text = re.sub(r"fifty six", "56", text)
        text = re.sub(r"fifty seven", "57", text)
        text = re.sub(r"fifty eight", "58", text)
        text = re.sub(r"fifty nine", "59", text)
        text = re.sub(r"fifty", "50", text)

        text = re.sub(r"sixty first", "61st", text)
        text = re.sub(r"sixty second", "62nd", text)
        text = re.sub(r"sixty third", "63rd", text)
        text = re.sub(r"sixty fourth", "64th", text)
        text = re.sub(r"sixty fifth", "65th", text)
        text = re.sub(r"sixty ninth", "69th", text)
        
        text = re.sub(r"sixty one", "61", text)
        text = re.sub(r"sixty two", "62", text)
        text = re.sub(r"sixty three", "63", text)
        text = re.sub(r"sixty four", "64", text)
        text = re.sub(r"sixty five", "65", text)
        text = re.sub(r"sixty six", "66", text)
        text = re.sub(r"sixty seven", "67", text)
        text = re.sub(r"sixty eight", "68", text)
        text = re.sub(r"sixty nine", "69", text)
        text = re.sub(r"sixty", "60", text)

        text = re.sub(r"seventy first", "71st", text)
        text = re.sub(r"seventy second", "72nd", text)
        text = re.sub(r"seventy third", "73rd", text)
        text = re.sub(r"seventy fourth", "74th", text)
        text = re.sub(r"seventy fifth", "75th", text)
        text = re.sub(r"seventy ninth", "79th", text)
        
        text = re.sub(r"seventy one", "71", text)
        text = re.sub(r"seventy two", "72", text)
        text = re.sub(r"seventy three", "73", text)
        text = re.sub(r"seventy four", "74", text)
        text = re.sub(r"seventy five", "75", text)
        text = re.sub(r"seventy six", "76", text)
        text = re.sub(r"seventy seven", "77", text)
        text = re.sub(r"seventy eight", "78", text)
        text = re.sub(r"seventy nine", "79", text)
        text = re.sub(r"seventy", "70", text)

        text = re.sub(r"eighty first", "81st", text)
        text = re.sub(r"eighty second", "82nd", text)
        text = re.sub(r"eighty third", "83rd", text)
        text = re.sub(r"eighty fourth", "84th", text)
        text = re.sub(r"eighty fifth", "85th", text)
        text = re.sub(r"eighty ninth", "89th", text)
        
        text = re.sub(r"eighty one", "81", text)
        text = re.sub(r"eighty two", "82", text)
        text = re.sub(r"eighty three", "83", text)
        text = re.sub(r"eighty four", "84", text)
        text = re.sub(r"eighty five", "85", text)
        text = re.sub(r"eighty six", "86", text)
        text = re.sub(r"eighty seven", "87", text)
        text = re.sub(r"eighty eight", "88", text)
        text = re.sub(r"eighty nine", "89", text)
        text = re.sub(r"eighty", "80", text)

        text = re.sub(r"ninety first", "91st", text)
        text = re.sub(r"ninety second", "92nd", text)
        text = re.sub(r"ninety third", "93rd", text)
        text = re.sub(r"ninety fourth", "94th", text)
        text = re.sub(r"ninety fifth", "95th", text)
        text = re.sub(r"ninety ninth", "99th", text)
        
        text = re.sub(r"ninety one", "91", text)
        text = re.sub(r"ninety two", "92", text)
        text = re.sub(r"ninety three", "93", text)
        text = re.sub(r"ninety four", "94", text)
        text = re.sub(r"ninety five", "95", text)
        text = re.sub(r"ninety six", "96", text)
        text = re.sub(r"ninety seven", "97", text)
        text = re.sub(r"ninety eight", "98", text)
        text = re.sub(r"ninety nine", "99", text)
        text = re.sub(r"ninety", "90", text)
        
        text = re.sub(r" one ", " 01 ", text)
        text = re.sub(r" two ", " 02 ", text)
        text = re.sub(r" three ", " 03 ", text)
        text = re.sub(r" four ", " 04 ", text)
        text = re.sub(r" five ", " 05 ", text)
        text = re.sub(r" six ", " 06 ", text)
        text = re.sub(r" seven ", " 07 ", text)
        text = re.sub(r" eight ", " 08 ", text)
        text = re.sub(r" nine ", " 09 ", text)
        text = re.sub(r" ten ", " 10 ", text)

        text = re.sub(r"first", "1st", text)
        text = re.sub(r"second", "2nd", text)
        text = re.sub(r"third", "3rd", text)
        text = re.sub(r"fourth", "4th", text)
        text = re.sub(r"fifth", " 5th ", text)
        text = re.sub(r"sixth", " 6th ", text)
        text = re.sub(r"seventh", " 7th ", text)
        text = re.sub(r"eighth", " 8th ", text)
        text = re.sub(r"ninth", " 9th ", text)
        text = re.sub(r"eleventh", " 11th ", text)
        text = re.sub(r"twelveth", " 12th ", text)
        text = re.sub(r"thirteenth", " 13th ", text)
        text = re.sub(r"fourteenth", " 14th", text)
        text = re.sub(r"fifteenth", " 15th ", text)
        text = re.sub(r"sixteenth", " 16th ", text)
        text = re.sub(r"seventeenth", " 17th ", text)
        text = re.sub(r"eighteenth", " 18th ", text)
        text = re.sub(r"nineteenth", " 19th ", text)
        text = re.sub(r"twentieth", " 20th ", text)
        text = re.sub(r"thirtieth", " 30th ", text)
        
        text = re.sub(r"hundred", "00", text)
        text = re.sub(r"thousand", "000", text)
        text = re.sub(r"million", "000000", text)
        text = re.sub(r"billion", "000000000", text)    
        return(text)
    


