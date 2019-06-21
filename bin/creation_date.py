import datetime

class Date:
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

    @classmethod
    def create_standard(self, name, standard):
        if standard == None:
            value = name
        else:
            value = name + '/' + standard

        return value
            