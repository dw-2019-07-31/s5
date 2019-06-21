import math

class Content:
    @classmethod
    def image_name_change(self,image_number,item_code):
        i = 1

        image_list = []
        while i <= int (image_number):
            data_size = int (math.log10(i) + 1)
            if data_size == 1: 
                image_list.append("%s_0%d.jpg" % (item_code, i))
            else:
                image_list.append("%s_%d.jpg" % (item_code, i))
            i += 1
        
        image_value = "`".join(image_list)
        return image_value