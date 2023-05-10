# Groups all methods related to retrieval or modifications of the tags found in Tenable.io

from .connections import *

class tags:

    @staticmethod
    def get_list():

           
        '''
        Returns a python list of dictionaries with tags info
        '''

        tio = connect_io()
        tags_list = []
        
        for tag in tio.tags.list():
            tags_list.append(tag)
        
        return tags_list
    
    @staticmethod
    def summary():
        
        '''
        Prints in screen an generates a .csv report with a list of all tags avaialble in T.io
        '''

        my_tags = tags()
        tag_list = my_tags.get_list()



        if len(tag_list) == 0:
            print("Any tags are created yet")
        else:
            print("Category\tValue\t\tTag UUID")

            with open('output_files/io_tag_summary.csv', 'w') as file:
            
                file.write("Category,Value,Tag UUID\n")
            
                for tag in tag_list:
                    file.write('{category_name},{value},{uuid}\n'.format(**tag))
                    print('{category_name}\t\t{value}\t\t{uuid}'.format(**tag))

            return "Tags summary report generated"