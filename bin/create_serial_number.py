import datetime

class Create_serial_number:
    @classmethod
    def date_change(self,i):
        now = datetime.datetime.now().strftime("%Y%m%d%H")

        q = i // 60
        mod = i % 60
        
        date_list = [q, mod]
        for a in date_list:
            date_size = len(str(a)) 
            if date_size == 1: 
                a = "0" + str(a)
            now = now + str(a)
        return now